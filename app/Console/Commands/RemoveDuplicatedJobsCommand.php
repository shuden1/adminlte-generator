<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Company;
use App\Jobs\RetrieveCompanyCareers;
use Illuminate\Support\Facades\DB;
use ReflectionObject;

class RemoveDuplicatedJobsCommand extends Command
{
    protected $signature = 'company:remove-careers {company_id}';
    protected $description = 'Remove duplicated jobs from the queue';

    public function __construct()
    {
        parent::__construct();
    }

    public function handle()
    {
        $companyId = $this->argument('company_id');
        $queuedCompanies = $this->getQueuedCompanyIds();
        dei();
        if ($companyId !== 'all') {
            if (!array_key_exists($companyId, $queuedCompanies)) {
                $company = Company::find($companyId);
                if ($company) {
                    RetrieveCompanyCareers::dispatch($company)->onQueue('RetrieveCareersQueue');
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
                if ((!array_key_exists($company->id, $queuedCompanies))&&($company->id >= 172)) {
                    RetrieveCompanyCareers::dispatch($company)->onQueue('RetrieveCareersQueue');
                    $this->info("Job dispatched for company ID: {$company->id}");
                } else {
                    if (isset($queuedCompanies[$company->id])) {
                        $jobId = $queuedCompanies[$company->id];
                        $this->info("Company ID: {$company->id} already has a job in the queue. Job ID: {$jobId[0]}");
                    }
                }
            }
        }
    }


    protected function getQueuedCompanyIds_remove_less172()
    {
        $jobs = DB::table('queue_jobs')
            ->where('queue', 'RetrieveCareersQueue')
            ->get(['id', 'payload']); // Fetch job ID and payload

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
                    if ($company['id'] < 172) {
                        DB::table('queue_jobs')->where('id', $job->id)->delete();
                    }
                }
            } catch (Exception $e) {
                error_log('Error accessing company ID: ' . $e->getMessage());
            }
        }
    }

    protected function getQueuedCompanyIds_count()
    {
        $jobs = DB::table('queue_jobs')
            ->where('queue', 'RetrieveCareersQueue')
            ->get(['id', 'payload']); // Fetch job ID and payload

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
                    if ($company['scripted'] <> 1) {
                        $this->info("Company ID: {$company->id} already is not scripted.");
                    }
                }
            } catch (Exception $e) {
                error_log('Error accessing company ID: ' . $e->getMessage());
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
        var_dump($companyJobs);die();
    }

}
