<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\Company; // Replace with the correct namespace if different
use Illuminate\Support\Facades\File;

class RenameCompanyScript extends Command
{
    protected $signature = 'company:rename-script';

    protected $description = 'Renames scripts for companies where scripted is 0';

    public function __construct()
    {
        parent::__construct();
    }

    public function handle()
    {
        $companies = Company::where('scripted', 0)->get();

        foreach ($companies as $company) {
            if (empty($company->careerPageUrl)) {
                continue;
            }

            $domain = parse_url($company->careerPageUrl, PHP_URL_HOST);
            $domain = str_replace('www.', '', $domain);

            $filePath = "D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape.py";
            $newFilePath = "D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape_wrong.py";

            if (File::exists($filePath)) {
                File::move($filePath, $newFilePath);
                $this->info("Renamed script for domain: {$domain}");
            }
        }

        $this->info('Completed renaming scripts.');
    }
}
