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
        var_dump($this->user);
        var_dump($this->chatId);
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
        set_time_limit(1200);
        $companies = $this->user->companies;

        foreach ($companies as $company) {
            $jobs = Job::where('company_id', $company->id)
                ->whereDate('created_at', Carbon::today())
                ->get();

            foreach ($jobs as $job) {
                if (!$this->checkRelevance($job)) {
                    $jobs = $jobs->reject(function ($value, $key) use ($job) {
                        return $value->id == $job->id;
                    });
                }
            }

            if (!$jobs->isEmpty()) {
                $jobs = $jobs->chunk(5); // Split the jobs into chunks of 5

                foreach ($jobs as $chunk) {
                    $message = '';
                    $message .= $company->name . ":\n";

                    foreach ($chunk as $job) {
                        $message .= $job->title . ' - '. $job->url. "\n";
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
    }}
