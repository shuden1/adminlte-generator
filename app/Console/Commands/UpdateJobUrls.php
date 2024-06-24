<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Job;

class UpdateJobUrls extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'jobs:update-urls';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Update job URLs that match a specific pattern';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        // Fetch all jobs
        $jobs = Job::all();

        foreach ($jobs as $job) {
            // Check if the URL contains '20-06-24.html' or '21-06-24.html'
            if (strpos($job->url, '20-06-24.html') !== false || strpos($job->url, '21-06-24.html') !== false) {
                // Remove it from the URL
                $job->url = str_replace(['20-06-24.html', '21-06-24.html'], '', $job->url);

                // Save the updated job
                $job->save();
                $this->info('company->'.$job->company->id);
            }

            // Check if the URL ends with a '#'
            if (substr($job->url, -1) === '#') {
                // Replace it with the company's careerPageUrl
                $job->url = $job->company->careerPageUrl;

                // Save the updated job
                $job->save();
            }
        }

        $this->info('Job URLs updated successfully.');

        return 0;
    }
}
