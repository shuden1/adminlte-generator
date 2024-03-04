<?php

namespace App\Http\Controllers;

use App\Models\OAuthToken;
use Google\Client;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Support\Facades\Session;

class EmailController extends Controller
{
    public function redirectToGoogle()
    {
        $client = new Client();
        $client->setClientId(env('GOOGLE_CLIENT_ID'));
        $client->setClientSecret(env('GOOGLE_CLIENT_SECRET'));
        $client->setRedirectUri(env('GOOGLE_REDIRECT_URI'));
        $client->addScope("https://www.googleapis.com/auth/gmail.send");
        $client->setAccessType("offline");
        $authUrl = $client->createAuthUrl();

        return Redirect::to($authUrl);
    }

    public function handleGoogleCallback(Request $request)
    {
        $client = new Client();
        $client->setClientId(env('GOOGLE_CLIENT_ID'));
        $client->setClientSecret(env('GOOGLE_CLIENT_SECRET'));
        $client->setRedirectUri(env('GOOGLE_REDIRECT_URI'));
        $token = $client->fetchAccessTokenWithAuthCode($request->code);
        $client->setAccessType("offline");

        $updateData = [
            'access_token' => $token['access_token'],
            'expires_in' => now()->addSeconds($token['expires_in']),
        ];

        // Only add refresh_token to the update array if it's present
        if (!empty($token['refresh_token'])) {
            $updateData['refresh_token'] = $token['refresh_token'];
        }

        OAuthToken::updateOrCreate(
            $updateData
        );
        return redirect('/'); // Or to a route of your choice
    }
}
