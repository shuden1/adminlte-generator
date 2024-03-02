<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use Google\Client;
use Google\Service\Gmail;

class JobPostedNotification extends Mailable
{
    use Queueable, SerializesModels;

    private $job;

    /**
     * Create a new message instance.
     *
     * @return void
     */
    public function __construct($job)
    {
        $this->job = $job;
    }

    public function build()
    {
        return $this->subject('Brand new Job Posting! How cool is that?! ')
            ->markdown('emails.jobs.posted', [
            'job' => $this->job,
        ]);
    }

}
