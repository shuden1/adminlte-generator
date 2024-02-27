<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Company;
use App\Jobs\RetrieveCompanyCareers;
use Illuminate\Support\Facades\DB;

class RetrieveCompanyCareersCommand extends Command
{
    protected $signature = 'company:retrieve-careers {company_id=all}';
    protected $description = 'Dispatch jobs for companies based on company ID or all companies with certain conditions';

    public function __construct()
    {
        parent::__construct();
    }

    public function handle()
    {
        $companyId = $this->argument('company_id');
        $queuedCompanyIds = $this->getQueuedCompanyIds();

        if ($companyId !== 'all') {
            if (!in_array($companyId, $queuedCompanyIds)) {
                $company = Company::find($companyId);
                if ($company) {
                    RetrieveCompanyCareers::dispatch($company)->onQueue('RetrieveCareersQueue');
                    $this->info("Job dispatched for company ID: {$companyId}");
                } else {
                    $this->error("No company found with ID: {$companyId}");
                }
            } else {
                $this->info("Company ID: {$companyId} already has a job in the queue.");
            }
        } else {
            $companies = Company::where('scripted', 1)->where('sauroned', 1)->get();
            foreach ($companies as $company) {
                if (!in_array($company->id, $queuedCompanyIds)) {
                    RetrieveCompanyCareers::dispatch($company)->onQueue('RetrieveCareersQueue');
                    $this->info("Job dispatched for company ID: {$company->id}");
                } else {
                    $this->info("Company ID: {$company->id} already has a job in the queue.");
                }
            }
        }
    }

    protected function getQueuedCompanyIds()
    {
        // Assuming your jobs are stored in a table named 'jobs' and payload containing the company ID
        $jobs = DB::table('queue_jobs')->get();
        $companyIds = [];
        foreach ($jobs as $job) {
            $payload = json_decode($job->payload, true);
            $command = unserialize($payload['data']['command']);
            if (property_exists($command, 'company')) {
                $companyIds[] = $command->company->id;
            }
        }
        return array_unique($companyIds);
    }
}
