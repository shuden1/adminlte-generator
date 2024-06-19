<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Company;
use App\Jobs\RetrieveCompanyCareers;
use Illuminate\Support\Facades\DB;
use ReflectionObject;

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
        $queuedCompanies = $this->getQueuedCompanyIds();
        if ($companyId !== 'all') {
            if (!array_key_exists($companyId, $queuedCompanies)) {
                $company = Company::find($companyId);
                if ($company) {
                    $job = RetrieveCompanyCareers::dispatch($company)->onQueue('RetrieveCareersQueue');
                    $this->info("Job dispatched for company ID: {$companyId}");
                } else {
                    $this->error("No company found with ID: {$companyId}");
                }
            } else {
                $jobId = $queuedCompanies[$companyId];
                $this->info("Company ID: {$companyId} already has a job in the queue. Job ID: {$jobId[0]}");
            }
        } else {
            $companies = Company::where('scripted', 1)->where('sauroned', 1)->get();
            foreach ($companies as $company) {
                if (!array_key_exists($company->id, $queuedCompanies)) {
                    $job = RetrieveCompanyCareers::dispatch($company)->onQueue('RetrieveCareersQueue');
                    $this->info("Job dispatched for company ID: {$company->id}");
                } else {
                    $jobId = $queuedCompanies[$company->id];
                    $this->info("Company ID: {$company->id} already has a job in the queue. Job ID: {$jobId[0]}");
                }
            }
        }
    }

    protected function getQueuedCompanyIds()
    {
        $jobs = DB::table('queue_jobs')
            ->where('queue', 'RetrieveCareersQueue')
            ->get(['id', 'payload']); // Fetch job ID and payload
        $companyJobs = [];
        foreach ($jobs as $job) {
            $payload = json_decode($job->payload, true);
            $commandSerialized = $payload['data']['command'];
            try {
                $command = unserialize($commandSerialized);
                $reflectionObject = new ReflectionObject($command);
                if ($reflectionObject->hasProperty('company')) {
                    $companyProperty = $reflectionObject->getProperty('company');
                    $companyProperty->setAccessible(true);
                    $company = $companyProperty->getValue($command);
                    $companyJobs[$company['id']][] = $job->id; // Store job ID alongside company ID
//                      $companyJobs[$company['id']] = $job->id; // Store job ID alongside company ID
                }
            } catch (Exception $e) {
                error_log('Error accessing company ID: ' . $e->getMessage());
            }
        }

        $temp_results = [];
        foreach ($companyJobs as $key => $companyJob){
            if (count($companyJob)>1){
                $temp_results[$key] = $companyJob;
            }
        }

        foreach ($temp_results as $tr){
            foreach ($tr as $k => $v){
                if ($k>0){
                    DB::table('queue_jobs')->where('id', $v)->delete();
                }
            }
        }
        return $companyJobs; // Return associative array of company IDs and their job IDs
    }

}
