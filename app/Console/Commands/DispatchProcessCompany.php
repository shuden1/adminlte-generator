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
    protected $signature = 'company:process';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Dispatch a job for every company where scripted is not true';

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        // Get all companies where scripted is not true
        $companies = Company::where('scripted', false)
            ->orWhereNull('scripted')
            ->Where('id', '>', '171')
            ->get();

        // Dispatch a job for each company
        foreach ($companies as $company) {
            ProcessCompany::dispatch($company);
        }

        $this->info('Jobs dispatched for all companies where scripted is not true.');

        return 0;
    }
}
