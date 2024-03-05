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

    protected function checkRelevancy($job)
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
        $companiesToSend = [];
        $newJobs = [];
        $companies = $this->user->companies;

        foreach ($companies as $company){
            $newJobs[$company->id]['today']['all'] = Job::where('company_id', $company->id)
                ->whereDate('created_at', Carbon::today())
                ->get();
            $newJobs[$company->id]['today']['relevant'] = [];
            foreach ($newJobs[$company->id]['today']['all'] as $job){
                if ($this->checkRelevancy($job)) {
                    $newJobs[$company->id]['today']['relevant'][] = $job;
                }
            }
            if (count($newJobs[$company->id]['today']['relevant'])>0) {

                $newJobs[$company->id]['week']['all'] = Job::withTrashed()
                    ->where('company_id', $company->id)
                    ->whereBetween('created_at', [Carbon::now()->startOfWeek(), Carbon::now()->endOfWeek()])
                    ->get();
                foreach ($newJobs[$company->id]['week']['all'] as $job) {
                    if ($this->checkRelevancy($job)) {
                        $newJobs[$company->id]['week']['relevant'][] = $job;
                    }
                }

                $newJobs[$company->id]['month']['all'] = Job::withTrashed()
                    ->where('company_id', $company->id)
                    ->whereMonth('created_at', Carbon::now()->month)
                    ->whereYear('created_at', Carbon::now()->year)
                    ->get();
                foreach ($newJobs[$company->id]['month']['all'] as $job) {
                    if ($this->checkRelevancy($job)) {
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

            $htmlContent = view('emails.email_template', compact('companiesToSend','newJobs'))->render();

            $email = (new \Swift_Message())
                ->setSubject($this->subject)
                ->setFrom('flock@littlebirds.io') // Use the service account email
                ->setTo($this->to)
                ->setBody($htmlContent, 'text/html');

            $message = new \Google\Service\Gmail\Message();
            $encodedMessage = base64_encode($email->toString());
            $message->setRaw(str_replace(['+', '/', '='], ['-', '_', ''], $encodedMessage)); // URL safe base64

            try {
                $service->users_messages->send('me', $message);
                foreach ($companiesToSend as $company){
                    $company->contacted = \Carbon\Carbon::now();
                    $company->save();
                }
            } catch (\Exception $e) {
                print_r("Failed to send email via Gmail: " . $e->getMessage());
            }
        }
    }
}
