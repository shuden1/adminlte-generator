<?php

namespace App\Services;

use Google\Client;
use Google\Service\Gmail;

class GmailService
{
    protected $client;

    public function __construct()
    {
        $this->client = new Client();
        $this->client->setClientId(env('GOOGLE_CLIENT_ID'));
        $this->client->setClientSecret(env('GOOGLE_CLIENT_SECRET'));
        $this->client->setRedirectUri(env('GOOGLE_REDIRECT_URI'));
        $this->client->addScope(Gmail::GMAIL_SEND);
        $this->client->setAccessType('offline');
    }

    public function sendEmail($to, $subject, $body)
    {
        // Here you would use the Google token you've stored after authentication
        // For this example, let's assume you've stored the token in the session
        $this->client->setAccessToken(session('google_token'));

        $service = new Gmail($this->client);
        $user = 'me';

        $strRawMessage = "From: Your Name <your-email@gmail.com>\r\n";
        $strRawMessage .= "To: {$to}\r\n";
        $strRawMessage .= 'Subject: ' . $subject . "\r\n";
        $strRawMessage .= "MIME-Version: 1.0\r\n";
        $strRawMessage .= "Content-Type: text/html; charset=utf-8\r\n";
        $strRawMessage .= 'Content-Transfer-Encoding: quoted-printable' . "\r\n\r\n";
        $strRawMessage .= $body . "\r\n";

        $mime = rtrim(strtr(base64_encode($strRawMessage), '+/', '-_'), '=');
        $message = new \Google\Service\Gmail\Message();
        $message->setRaw($mime);

        try {
            $service->users_messages->send($user, $message);
        } catch (\Exception $e) {
            // Handle error
            throw $e;
        }
    }
}
