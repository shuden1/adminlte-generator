<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Jobs\ProcessCompany;
use App\Models\Company;

class DispatchProcessCompany extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'company:process {company_id?}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Dispatch a job for every company where scripted is not true or for a specific company if company_id is provided';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $companyId = $this->argument('company_id');

        if ($companyId) {
            $company = Company::find($companyId);
            if ($company) {
                ProcessCompany::dispatch($company);
                $this->info("Job dispatched for company with id: {$companyId}.");
            } else {
                $this->error("No company found with id: {$companyId}.");
            }
        } else {
            // Get all companies where scripted is not true
            $companies = Company::where('sauroned', 1)
                ->where(function ($query) {
                    $query->where('scripted', '0')
                        ->orWhereNull('scripted');
                })
                ->get();

            // Dispatch a job for each company
            foreach ($companies as $company) {
                ProcessCompany::dispatch($company);
            }

            $this->info('Jobs dispatched for all companies where scripted is not true.');
        }

        return 0;
    }
}
