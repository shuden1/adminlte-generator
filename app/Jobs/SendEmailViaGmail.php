<?php

namespace App\Jobs;

use App\Models\Job;
use App\Models\OAuthToken;
use Google\Client;
use Google\Service\Gmail;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class SendEmailViaGmail implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $to;
    protected $subject;
    protected $jobId;

    public function __construct($to, $subject, $jobId)
    {
        $this->to = $to;
        $this->subject = $subject;
        $this->jobId = $jobId;
    }

    public function handle()
    {
        $job = Job::find($this->jobId);
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

        $email = (new \Swift_Message())
            ->setSubject($this->subject)
            ->setFrom('flock@littlebirds.io') // Use the service account email
            ->setTo($this->to)
            ->setBody("{$job->company->name} posted a new opening! \r\n {$job->title}", 'text/html');

        $message = new \Google\Service\Gmail\Message();
        $encodedMessage = base64_encode($email->toString());
        $message->setRaw(str_replace(['+', '/', '='], ['-', '_', ''], $encodedMessage)); // URL safe base64

        try {
            $service->users_messages->send('me', $message);
        } catch (\Exception $e) {
            print_r("Failed to send email via Gmail: " . $e->getMessage());
        }
    }
}
