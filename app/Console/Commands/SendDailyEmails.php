<?php

namespace App\Console\Commands;

use App\Jobs\SendTelegramMessage;
use Illuminate\Console\Command;
use App\Models\User; // Make sure to use your actual User model
use App\Jobs\SendEmailViaGmail;

class SendDailyEmails extends Command
{
    protected $signature = 'send:daily-emails {user?}';

    protected $description = 'Sends an email to all users about new job openings';

    public function handle()
    {
        $userId = $this->argument('user');

        if ($userId) {
            $users = User::where('id', $userId)->get();
        } else {
            $users = User::where('is_active', true)->get();  // Fetch all active users
        }

        foreach ($users as $user) {
            // Dispatch the job for each user
            if (isset($user->telegram_chat_id)){
                SendTelegramMessage::dispatch($user, $user->telegram_chat_id);

            } else {
                SendEmailViaGmail::dispatch($user->email, 'New Job Openings Collected by LittleBirds.io', $user->id);
            }
            // Optional: Output a message to the console
            $this->info('Dispatched email to: ' . $user->email);
        }
    }
}
