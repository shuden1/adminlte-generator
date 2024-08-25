<?php

namespace App\Jobs;

use App\Models\Company;
use App\Models\Job;
use App\Models\OAuthToken;
use App\Models\SuitableTitle;
use App\Models\User;
use Google\Client;
use Google\Service\Gmail;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Carbon;

class SendEmailViaGmail implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $to;
    protected $subject;
    protected $user;

    public function __construct($to, $subject, $userId)
    {
        $this->to = $to;
        $this->subject = $subject;
        $this->user = User::find($userId);
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
        set_time_limit(5000);

        $companiesToSend = [];
        $newJobs = [];
        $companies = $this->user->companies;

        foreach ($companies as $company){
            // Step 1: Determine the last 'provided_at' date for any job related to the $company
            $lastProvidedAt = Job::where('company_id', $company->id)
                ->join('job_user', 'jobs.id', '=', 'job_user.job_id')
                ->max('job_user.provided_at');

            // Step 2: Modify the existing job query to include the new condition
            $jobs = Job::where('company_id', $company->id)
                ->whereDoesntHave('users', function ($query) {
                    $query->where('user_id', $this->user->id);
                })
                ->when($lastProvidedAt, function ($query) use ($lastProvidedAt) {
                    // Only include jobs created after the last 'provided_at' date
                    return $query->where('created_at', '>', $lastProvidedAt);
                })
                ->get();


            $newJobs[$company->id]['today']['all'] = $jobs;

            $newJobs[$company->id]['today']['relevant'] = [];
            foreach ($newJobs[$company->id]['today']['all'] as $key => $job) {
                if ($this->checkRelevance($job)) {
                    $newJobs[$company->id]['today']['relevant'][] = $job;
                    $this->user->jobs()->attach($job->id, ['provided_at' => Carbon::today()]);
                }
                if (!$job->created_at->isToday()) {
                    unset($newJobs[$company->id]['today']['all'][$key]);
                }

            }
            if (count($newJobs[$company->id]['today']['relevant'])>0) {
                $company->contacted = \Carbon\Carbon::now();
                $company->save();

                $newJobs[$company->id]['week']['relevant'] = [];
                $newJobs[$company->id]['week']['all'] = Job::withTrashed()
                    ->where('company_id', $company->id)
                    ->whereBetween('created_at', [Carbon::now()->startOfWeek(), Carbon::now()->endOfWeek()])
                    ->get();
                foreach ($newJobs[$company->id]['week']['all'] as $job) {
                    if ($this->checkRelevance($job)) {
                        $newJobs[$company->id]['week']['relevant'][] = $job;
                    }
                }
                $newJobs[$company->id]['month']['relevant'] = [];
                $newJobs[$company->id]['month']['all'] = Job::withTrashed()
                    ->where('company_id', $company->id)
                    ->whereMonth('created_at', Carbon::now()->month)
                    ->whereYear('created_at', Carbon::now()->year)
                    ->get();
                foreach ($newJobs[$company->id]['month']['all'] as $job) {
                    if ($this->checkRelevance($job)) {
                        $newJobs[$company->id]['month']['relevant'][] = $job;
                    }
                }
                $companiesToSend[] = $company;
            } else {
                unset($newJobs[$company->id]);
            }
        }
        if (count($newJobs)>0) {
            $tokenData = OAuthToken::first(); // Adjust user_id as necessary

            $client = new Client();
            $client->setAuthConfig([
                'client_id' => env('GOOGLE_CLIENT_ID'),
                'client_secret' => env('GOOGLE_CLIENT_SECRET'),
                'redirect_uri' => env('GOOGLE_REDIRECT_URI')
            ]);
            $client->setAccessToken([
                'access_token' => $tokenData->access_token,
                'refresh_token' => $tokenData->refresh_token,
                'expires_in' => now()->diffInSeconds($tokenData->expires_in),
            ]);
            $client->setAccessType("offline");

            $tokenData = OAuthToken::firstOrFail(); // Retrieve the token data

// Assuming 'expires_in' is a datetime of when the token expires
            $tokenExpired = now()->gte($tokenData->expires_in); // Check if the token has expired
            if ($tokenExpired) {
                // Refresh the token
                $newAccessToken = $client->fetchAccessTokenWithRefreshToken($tokenData->refresh_token);

                // Calculate the new expiration datetime
                $newExpiresIn = now()->addSeconds($newAccessToken['expires_in'])->toDateTimeString();

                // Update the database
                $tokenData->update([
                    'access_token' => $newAccessToken['access_token'],
                    'expires_in' => $newExpiresIn,
                ]);
            }


            $service = new Gmail($client);

            $emails = array_merge([$this->to], $this->user->emails->pluck('email')->toArray());

            $companyChunks = array_chunk($companiesToSend, 5); // Chunk companies by 5

            foreach ($companyChunks as $chunk) {
                $companiesToSend = $chunk;
                $htmlContent = view('emails.email_template', compact('companiesToSend', 'newJobs'))->render();
                $this->sendEmail($service, $htmlContent, $this->subject, $emails);
            }
        }
    }

      function sendEmail($service, $content, $subject, $emails) {
        // Prepare the MIME message with headers and body
        $mimeMessage = "Content-Type: text/html; charset=utf-8\r\n";
        $mimeMessage .= "From: flock@littlebirds.io\r\n";
        $mimeMessage .= "To: " . implode(",", $emails) . "\r\n";
//        $mimeMessage .= "To: " .  "shugaevden@gmail.com\r\n";
        $mimeMessage .= "Subject: =?utf-8?B?" . base64_encode($subject) . "?=\r\n\r\n";
        $mimeMessage .= $content;

        // Base64 encode the entire MIME message
        $base64EncodedEmail = base64_encode($mimeMessage);

        // Make the base64-encoded string URL-safe
        $urlSafeBase64EncodedEmail = str_replace(['+', '/', '='], ['-', '_', ''], $base64EncodedEmail);

        // Create a new Gmail message and set the raw field with the URL-safe, base64-encoded MIME message
        $message = new \Google\Service\Gmail\Message();
        $message->setRaw($urlSafeBase64EncodedEmail);

        try {
            $service->users_messages->send('me', $message);
        } catch (\Exception $e) {
            print_r("Failed to send email part via Gmail: " . $e->getMessage());
        }
    }

}
