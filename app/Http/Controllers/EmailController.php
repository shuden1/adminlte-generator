<?php

namespace App\Http\Controllers;

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

        Session::put('google_token', $token);

        return redirect('/'); // Or to any route you prefer
    }
}
