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
                ->whereDoesntHave('users', function ($query) {
                    $query->where('user_id', $this->user->id);
                })
                ->get();

            foreach ($jobs as $job) {
                if (!$this->checkRelevance($job)) {
                    continue;
                }

                $this->user->jobs()->attach($job->id, ['provided_at' => Carbon::today()]);

                // Check if the job title contains any of the leadership keywords
                if (preg_match('/Manager|Lead|Director|Owner|Project|Product|HR|Human|Marketing|Менеджер|Лид|Директор|Проект|Продукт|Рекрут|Персон|Руководитель|Начальник|Маркет/i', $job->title)) {
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
                try {
                    Telegram::sendMessage([
                        'chat_id' => $this->chatId,
                        'text' => $message
                    ]);
                } catch (\Telegram\Bot\Exceptions\TelegramResponseException $e) {
                    $errorData = $e->getResponseData();

                    if ($errorData['ok'] === false) {
                        $errorCode = $errorData['error_code'];
                        $description = $errorData['description'];

                        if ($errorCode === 429) {
                            $parameters = $errorData['parameters'];
                            sleep($parameters['retry_after']);
                        } else {
                            // Handle other exceptions if needed
                            // For example, you can log the error code and description
                            error_log("Telegram API error: {$errorCode} - {$description}");
                        }
                    }
                }
            }
        }
    }
}
