<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;
use League\Csv\Writer;

class ExportJobs extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'export:jobs {date} {user_id}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Export jobs related to a user before a certain date';

    protected function checkRelevance($job)
    {
        $userId = $this->argument('user_id');

        $suitableTitles = DB::table('suitable_title_user')
            ->join('suitable_titles', 'suitable_titles.id', '=', 'suitable_title_user.suitable_title_id')
            ->where('suitable_title_user.user_id', $userId)
            ->select('suitable_titles.title')  // Ensure the title column is selected
            ->get();

        if ($suitableTitles->isEmpty()) {
            return true;
        } else {
            foreach ($suitableTitles as $suitableTitle) {
                if (stripos($job->title, $suitableTitle->title) !== false) {
                    return true;
                }
            }
        }

        return false;
    }


        /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $date = Carbon::createFromFormat('d-m-y', $this->argument('date'));
        $userId = $this->argument('user_id');

        $jobs = DB::table('jobs')
            ->join('companies', 'jobs.company_id', '=', 'companies.id')
            ->join('company_user', 'companies.id', '=', 'company_user.company_id')
            ->where('company_user.user_id', $userId)
            ->whereNull('jobs.deleted_at')
            ->where('jobs.created_at', '<', $date)
            ->select('companies.name as company_name', 'companies.website as company_website', 'jobs.title as title', 'jobs.url as url')
            ->get();

        $csv = Writer::createFromString('');
        $csv->insertOne(['Company Name', 'Website', 'Job Title', 'Job URL']);

        $groupedJobs = $jobs->groupBy('company_name');

        foreach ($groupedJobs as $companyName => $jobs) {
            $relevantJobs = $jobs->filter(function ($job) {
                return $this->checkRelevance($job);
            });

            if ($relevantJobs->isEmpty()) {
                continue;
            }

            foreach ($relevantJobs as $job) {
                $csv->insertOne([$companyName, $job->company_website, $job->title, $job->url]);
            }
        }

        file_put_contents('Agency-LeadsJobs_08-26-24.csv', $csv->getContent());
    }
}
