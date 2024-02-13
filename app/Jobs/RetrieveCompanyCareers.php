<?php

namespace App\Jobs;

use App\Models\Company;
use App\Models\DecisionMaker;
use App\Models\Job;
use App\Models\SuitableTitle;
use Carbon\Carbon;
use DateTime;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Http;

// php artisan queue:work --queue=RetrieveCareersQueue

class RetrieveCompanyCareers implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $company;

    /**
     * Create a new job instance.
     *
     * @return void
     */
    public function __construct(Company $company)
    {
        $this->company = $company;
        $this->queue = 'RetrieveCareersQueue';
    }

    public function getLatestFile($directoryPath)
    {
// Scan the directory for files
        $files = scandir($directoryPath);

// Filter out non-HTML files and '.' and '..'
        $htmlFiles = array_filter($files, function ($file) {
            return strpos($file, '.html') !== false;
        });

        $latestFile = '';
        $latestDate = DateTime::createFromFormat('d-m-y', '01-01-70'); // Starting from a base date

        foreach ($htmlFiles as $file) {
            // Extract the date from the filename
            $dateString = substr($file, 0, strpos($file, '.html'));
            $today = new DateTime();
            $today->setTime(0, 0, 0);
            try {
                $date = DateTime::createFromFormat('d-m-y', $dateString);
                // Check if this file is more recent
                if ($date && $date > $latestDate && $date->format('d-m-y') !== $today->format('d-m-y')) {
                    $latestDate = $date;
                    $latestFile = $file;
                }
            } catch (Exception $e) {
                // Handle exception if the date format is incorrect
                continue;
            }
        }

        if ($latestFile) {
            return $latestFile;
        } else {
            return false;
        }

    }

    public function handle()
    {
        $company = $this->company;
        $domain = parse_url($company->careerPageUrl, PHP_URL_HOST);
        $domain = str_replace('www.','',$domain);
        // Creating a recent page image
        $basePathHtmls = "D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/".$domain."/HTMLs/".$company->id;


        if (!is_dir($basePathHtmls)) {
            mkdir($basePathHtmls, 0777, true); // The 0777 specifies the permissions, and true enables recursive creation
        }

        $latestFile = $this->getLatestFile($basePathHtmls);

        $pythonExecutable = "C:/Python3/python.exe";
        $scriptPath = "D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/html_fetch_iframes.py";
        $careerPageUrl = escapeshellarg($company->careerPageUrl);
        $filePath = escapeshellarg($basePathHtmls."/".date("d-m-y").".html");

        $command = "{$pythonExecutable} {$scriptPath} {$careerPageUrl} {$filePath}";

        shell_exec($command);

        $scriptPath = base_path("/ParkerScripts/Companies/".$domain."/scrape.py");


        if ($latestFile){
            $html1 = file_get_contents($basePathHtmls."/".$latestFile);
            $html2 = file_get_contents($basePathHtmls."/".date("d-m-y").".html");

            if ($html1 === $html2) {
                $updateTrigger = false;
            } else {
                $updateTrigger = true;
            }
        } else {
            $updateTrigger = true;
        }
        if (file_exists($scriptPath) && ($updateTrigger)) {
            $process = shell_exec('python ' . escapeshellarg($scriptPath) . ' "' . escapeshellarg($basePathHtmls . "/" . date("d-m-y") . '.html"'));
            $jsonData = json_decode($process, true);
                /*
                 * ZERO POSTINGS CHECK

                                if ($jsonData === null && json_last_error() !== JSON_ERROR_NONE) {
                                    ProcessCompany::dispatch($company, false);
                                    break;
                                } else {
                                    // Check if the result is empty
                                    if (empty($jsonData)) {
                                        ProcessCompany::dispatch($company, false);
                                        break;
                                    }
                                }
                */
            $scheme = parse_url($company->careerPageUrl, PHP_URL_SCHEME);
            $domain = parse_url($company->careerPageUrl, PHP_URL_HOST);

                // Concatenate them to form the base URL
            $baseUrl = $scheme . '://' . $domain;

            print_r($baseUrl);
            if ($jsonData) {
                foreach ($jsonData as $jobData) {
                    var_dump($jobData);


                    if (strpos($jobData['URL'], "file:///".$basePathHtmls) !== false) {
                        $jobData['URL'] = str_replace("file:///".$basePathHtmls, $baseUrl, $jobData['URL']);
                    }
                    elseif (strpos($jobData['URL'], "file:///D:") !== false) {
                        $jobData['URL'] = str_replace("file:///D:", $baseUrl, $jobData['URL']);
                    }
                    elseif (strpos($jobData['URL'], 'http://') === false && strpos($jobData['URL'], 'https://') === false) {
                        $jobData['URL'] = rtrim($baseUrl, '/') . '/' . ltrim($jobData['URL'], '/');
                    }
                    $existingJob = Job::where('url', $jobData['URL'])
                        ->where('title', $jobData['Job-title'])
                        ->first();
                    if (!$existingJob) {
                        var_dump($jobData);
                        $newJob = Job::create([
                            'company_id' => $company->id,
                            'title' => $jobData['Job-title'],
                            'url' => $jobData['URL'],
                            'date' => Carbon::now(),
                        ]);

                        if (is_null($company->contacted) || $company->contacted->lessThan(Carbon::now()->subMonths(3))) {
                            //                   $this->checkAndTrigger($company, $newJob);
                        }
                    } else {
                        $existingJob->touch();
                    }
                }
            }
            $yesterday = Carbon::yesterday();
            $jobsToDelete = $company->jobs()
                ->whereDate('updated_at', '<=', $yesterday)
                ->get();

                // Loop through the jobs and safely delete each one
            foreach ($jobsToDelete as $job) {
                $job->delete(); // This will soft delete if SoftDeletes trait is used in Job model
            }

        } else {
            if (!file_exists($scriptPath)){
                $this->error("Script for {$company->name} not found.");
            } else {
                unlink($basePathHtmls."/".date("d-m-y").".html");
                $this->info("No updates on the webpage");
            }
        }
        $when = Carbon::now()->addDay();
        RetrieveCompanyCareers::dispatch($company)->onQueue('RetrieveCareersQueue')->delay($when);
    }

    protected function checkAndTrigger($company, $job)
    {
        $suitableTitles = SuitableTitle::all();
        foreach ($suitableTitles as $suitableTitle) {
            if (stripos($job->title, $suitableTitle->title) !== false) {
                $this->triggered($company, $job);
                break; // Break the loop if a match is found
            }
        }
    }

    protected function triggered($company, $job)
    {
        $decisionMaker = DecisionMaker::where('company_id', $company->id)->first();
        $previousJob = Job::where('date', '<', $job->date)
            ->orderBy('date', 'desc')
            ->first();

        $payload = [
            'profile_link'   => $decisionMaker->profile_url ?? '',
            'first_name'     => $decisionMaker->firstName ?? '',
            'company_name'   => $company->name ?? '',
            'job_title'      => $job->title ?? '',
            'previous_title' => $previousJob->title ?? '',
        ];

        $this->sendWebhook($payload);

        $company->contacted = Carbon::now();
        $company->save();
    }

    protected function sendWebhook($payload)
    {
        $url = 'https://api.liaufa.com/api/v1/open-api/campaign-instance/443302/assign/?key=bef4338e-9a61-438d-a07f-86830e6e30c6&secret=a465b1f1-742d-4a0d-aaac-a450496bc12d';

        try {
            $response = Http::post($url, $payload);

            if ($response->successful()) {
                $this->info('Webhook sent successfully.');
            } else {
                $this->error('Failed to send webhook. Response: ' . $response->body());
            }
        } catch (\Exception $e) {
            $this->error('Error sending webhook: ' . $e->getMessage());
        }
    }
}
