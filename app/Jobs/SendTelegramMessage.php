<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Telegram\Bot\Laravel\Facades\Telegram;
use App\Models\Job;
use Carbon\Carbon;

class SendTelegramMessage implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $user;
    protected $chatId;

    public function __construct($user, $chatId)
    {
        $this->user = $user;
        $this->chatId = $chatId;
    }

    protected function checkRelevance($job)
    {
        if ($this->user) {
            $suitableTitles = $this->user->suitableTitles;
            foreach ($suitableTitles as $suitableTitle) {
                if (stripos($job->title, $suitableTitle->title) !== false) {
                    return true;
                }
            }
        }
        return false;
    }


    public function handle()
    {
        set_time_limit(2400);
        $companies = $this->user->companies;

        $leadershipJobs = [];
        $technicalJobs = [];

        foreach ($companies as $company) {
            $jobs = Job::where('company_id', $company->id)
                ->whereDate('created_at', Carbon::today())
                ->get();

            foreach ($jobs as $job) {
                if (!$this->checkRelevance($job)) {
                    continue;
                }

                // Check if the job title contains any of the leadership keywords
                if (preg_match('/Manager|Lead|Director|Owner|Project|Product|HR|Human/i', $job->title)) {
                    $leadershipJobs[] = ['company' => $company->name, 'title' => $job->title, 'url' => $job->url];
                } else {
                    $technicalJobs[] = ['company' => $company->name, 'title' => $job->title, 'url' => $job->url];
                }
            }
        }

        // Chunk the jobs into groups of 5 and send each chunk as a message
        $this->sendMessageInChunks($leadershipJobs, '#Leadership/HR');
        $this->sendMessageInChunks($technicalJobs, '#Technical');
    }

    private function sendMessageInChunks($jobs, $category)
    {
        $chunks = array_chunk($jobs, 5);

        foreach ($chunks as $chunk) {
            $message = $category . "\n";

            $currentCompany = '';
            foreach ($chunk as $job) {
                if ($job['company'] !== $currentCompany) {
                    $currentCompany = $job['company'];
                    $message .= $currentCompany . ":\n";
                }

                $message .= $job['title'] . ' - ' . $job['url'] . "\n";
            }

            if (!empty($message)) {
                Telegram::sendMessage([
                    'chat_id' => $this->chatId,
                    'text' => $message
                ]);
            }
        }
    }
}
