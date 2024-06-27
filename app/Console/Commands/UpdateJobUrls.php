<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Job;
use Illuminate\Support\Facades\DB;

class UpdateJobUrls extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'update:job-urls';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Update job URLs and remove duplicates';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        // Get all jobs where URL contains 'linkedin.com'
        $jobs = Job::where('url', 'like', '%linkedin.com%')->get();

        DB::beginTransaction();

        try {
            foreach ($jobs as $job) {
                $url = $job->url;
                $parsedUrl = parse_url($url);
                $newUrl = $parsedUrl['scheme'] . '://' . $parsedUrl['host'] . $parsedUrl['path'];

                // Update the job URL
                $job->url = $newUrl;
                $job->save();
            }

            // Remove duplicates
            DB::statement('
                DELETE j1 FROM jobs j1
                INNER JOIN jobs j2
                WHERE j1.id < j2.id AND j1.title = j2.title AND j1.url = j2.url
            ');

            DB::commit();

            $this->info('Job URLs updated and duplicates removed successfully.');

        } catch (\Exception $e) {
            DB::rollback();

            $this->error('An error occurred while updating job URLs and removing duplicates: ' . $e->getMessage());
        }

        return 0;
    }
}
