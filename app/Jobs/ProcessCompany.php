<?php

namespace App\Jobs;

use App\Events\JobStatusUpdated;
use App\Models\Company;
use App\Models\DomainFolder;
use App\Models\JobStatus;
use Carbon\Carbon;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;
use OpenAI;
use OpenAI\Exceptions\ErrorException;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;

// php artisan queue:work --queue=ScriptGenerationQueue
// pm2 start ecosystem.config.js
/*

List all processes: pm2 list
Monitor processes: pm2 monit
Stop a process: pm2 stop <id|name>
Restart a process: pm2 restart <id|name>
Delete a process: pm2 delete <id|name>
 */

class ProcessCompany implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $company;
    protected $forced;
    protected $hasJobs;

    public $tries = 3;
    public $timeout = 1200;

    /**
     * Create a new job instance.
     *
     * @return void
     */
    public function __construct(Company $company, $forced = 0, $hasJobs = 1)
    {
        $this->company = $company;
        $this->forced = $forced;
        $this->hasJobs = $hasJobs;
        $this->queue = 'ScriptGenerationQueue';
    }

    public function failed(Exception $exception)
    {
        // Send user notification of failure, etc...
        Log::error("Job failed. Exception: {$exception->getMessage()}");
    }

    public function getCleanHTML($inputFile, $outputFile, $careerPageURL)
    {
        $pythonPath = "C:\\Users\\shuga\\AppData\\Local\\Programs\\Python\\Python312";

        $command = $pythonPath."\\python.exe"." D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\html_fetch_iframes.py \"".$careerPageURL."\" \"".$inputFile."\"";
        exec($command, $output1, $returnStatus1);


        // Call sculpting.py
        $command2 = $pythonPath."\\python.exe D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\sculpting.py \"" . $inputFile . "\" \"" . $outputFile . "\"";

// Execute the second script and wait for it to finish
        exec($command2, $output2, $returnStatus2);

        if ($returnStatus2 !==0 ) {
            throw new \Exception($returnStatus2);
        }

        $filesizeKB = filesize($outputFile) / 1024;
        if ($filesizeKB<3){
            $command = $pythonPath."\\python.exe"." D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\html_fetch_iframes.py \"".$careerPageURL."\" \"".$inputFile."\"";
            exec($command, $output1, $returnStatus1);

            // Call sculpting.py
            $command2 = $pythonPath."\\python.exe D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\sculpting.py \"" . $inputFile . "\" \"" . $outputFile . "\"";

            // Execute the second script and wait for it to finish
            exec($command2, $output2, $returnStatus2);

            if ($returnStatus2 !==0 ) {
                throw new \Exception($returnStatus2);
            }


        }

    }

    public function extractPythonScript($text): string
    {
        $startPhrase = "```python";
        $endPhrase = "```";

        // Find the start and end indices of the Python script
        $startIdx = strpos($text, $startPhrase);
        if ($startIdx !== false){
            $endIdx = strpos($text, $endPhrase, $startIdx + 1);
        } else $endIdx = false;

        // Extract and return the script
        if ($startIdx !== false && $endIdx !== false) {
            $startIdx += strlen($startPhrase); // Move start index to end of startPhrase
            return trim(substr($text, $startIdx, $endIdx - $startIdx));
        } else {
            return $text;
        }
    }

    public function runPythonScriptAndCheckJson($scriptPath, $target): array
    {
        $base_url  = parse_url($this->company->careerPageUrl, PHP_URL_SCHEME) . '://' . parse_url($this->company->careerPageUrl, PHP_URL_HOST);

        // Run the Python script
        $output = shell_exec('python ' . escapeshellarg($scriptPath).' '.escapeshellarg($target).' 2>&1');
        // Check if the output is valid JSON
        $json_out = json_decode($output, true);
        if (json_last_error() === JSON_ERROR_NONE) {
            return [
                'isValidJson' => true,
                'jsonData' => $json_out
            ];
        } else {
            return [
                'isValidJson' => false,
                'error' => $output
            ];
        }
    }

    private function getGptResponse($client, $threadId, $runId){

        $statusCheck = $client->threads()->runs()->retrieve($threadId,$runId);
        $counter = 0;
        while (($statusCheck->status != "completed") && ($counter < 20)){
            $counter++;
            sleep(3);
            $statusCheck = $client->threads()->runs()->retrieve($threadId,$runId);
        }

        $messageList = $client->threads()->messages()->list($threadId, [
            'limit' => 10,
        ]);
        $message = $client->threads()->messages()->retrieve($threadId,$messageList->firstId);
        return ($message->content[0]->text->value);
    }

    function uploadFileWithRetry($client, $input_file, $maxRetries = 5) {
        $currentAttempt = 0;
        while ($currentAttempt < $maxRetries) {
            try {
                // Attempt to upload the file
                // If upload is successful, return the response
                return $client->files()->upload([
                    'purpose' => 'assistants',
                    'file' => fopen($input_file, 'r'),
                ]);
            } catch (ErrorException $e) {
                // Increment the attempt counter
                $currentAttempt++;

                sleep(2); // Wait for 1 second before retrying (if needed)
            }
        }

        // All attempts failed, throw an exception or return an error
        var_dump("Failed to upload file"); return false;
    }

    public function getScriptFromGPT(){


    }

    public function generateScript($input_file, $output_file, $careerPage)
    {
        $apiKey = env('OPENAI_KEY');
        Log::info('OPENAI_KEY : '.$apiKey);
        Log::info('APP_KEY : '.env('APP_KEY'));

        $client = OpenAI::client($apiKey);

        try {
            $response = $this->uploadFileWithRetry($client, $input_file);
            // Continue with your logic
        } catch (Exception $e) {
            var_dump($e->getMessage());
            return false;
        }

        if (!is_bool($response)) {
            $fileId = $response->id;
        } else return false;


        $response = $client->threads()->createAndRun(
            [
                'assistant_id' => 'asst_TXBXdt73opAxuoAxMAQ9dCFC',
                'thread' => [
                    'messages' =>
                        [
                            [
                            'role' => 'user',
                            'content' => "Analyze the HTML file attached. STEP 1: Use BeautifulSoup to identify the EXACT HTML CLASS OR ONLY IF THERE IS NO CLASS - SOME NON-ID!! PARAMETERS selectors including classes representing the blocks representing Job Openings. NEVER reference to the selector's ID. Within these blocks identify the EXACT selectors for job titles and their associated URLs. Few tips: Sometimes Job opening blocks are a part of a <ul> list. Sometimes Job opening blocks are <div> blocks with a repetitive class and relevant content inside, such as Job title, URL, optional department, optional location, and optional salary. Sometimes Job Titles might be located in <h> tag inside <a> tag, representing an associated URL. Sometimes Job Title is the text inside the <a> tag that represents an associated URL. Sometimes Job Title is the text inside the <p> tag. You need to figure out what exactly is a job title. Pay attention to the labels such as \"Jobs\", \"Careers\", \"Openings\", etc. Provide the selectors and a few examples. Ensure you have found job postings, but not some other information about the company before proceeding to the next step. The selectors you defined are going to be used in STEP 2!",
                            'attachments'=> [
                                [
                                    "file_id"=> $fileId,
                                    "tools" => [
                                        ["type"=> "code_interpreter"]
                                    ]
                                ],
                            ],
                            ],
                        ],
                    ],
                ]
        );
        $runId = $response->id;
        $threadId = $response->threadId;

        $lastMessage = $this->getGptResponse($client, $threadId, $runId);
        $timer = 0;
        while (($timer<20)&&($lastMessage == "Analyze the HTML file attached. STEP 1: Use BeautifulSoup to identify the EXACT HTML selectors including classes representing the blocks representing Job Openings. NEVER reference to the selector's ID. ALWAYS reference to the selector's class. Within these blocks identify the EXACT selectors for job titles and their associated URLs. Few tips: Sometimes Job opening blocks are a part of a <ul> list. Sometimes Job opening blocks are <div> blocks with a repetitive class and relevant content inside, such as Job title, URL, optional department, optional location, and optional salary. Sometimes Job Titles might be located in <h> tag inside <a> tag, representing an associated URL. Sometimes Job Title is the text inside the <a> tag that represents an associated URL. Pay attention to the labels such as \"Jobs\", \"Careers\", \"Openings\", etc - words like this are a sign that the list of jobs is beneath. The selectors you defined are going to be used in STEP 2!")){
            $lastMessage = $this->getGptResponse($client, $threadId, $runId);
            $timer ++;
            sleep(3);
        }
        var_dump($lastMessage);

        $client->threads()->messages()->create($threadId, [
            'role' => 'user',
            'content' => "STEP 2: Create a Python + Selenium script using the latest best practices for ChromeDriver 120.0.6099.109.
            1. This script will be launched externally in a settled-up environment, DO NOT TEST THIS SCRIPT, CREATE IT:
            THE TARGET HTML FILE NAME SHOULD BE AN ARGUMENT SENT FROM AN EXTERNAL SOURCE THROUGH THE CONSOLE COMMAND AS THE SINGLE INPUT PARAMETER. DO NOT PUT ANY PLACEHOLDERS OR EXAMPLES!
            2. Initialise a headless webdriver, with this profile path, do not forget to create a relevant folder: profile_folder_path=\"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\"+str(threading.get_ident()) use this service:
            service=service(executable_path=r\"C:\\Python3\\chromedriver.exe\") add these options: options.add_argument(f\"user-data-dir={profile_folder_path}\") options.add_argument(\"--headless\") options.add_argument(\"--disable-gpu\") options.add_argument(\"--no-sandbox\")
            3. USE THE SELECTORS DEFINED IN STEP 1!!! and scrape all job listings. REMEMBER!!!! instead of an old find_elements_by_css_selector, you should use the find_elements method with By.CSS_SELECTOR
            4. NEVER IMPLEMENT EXAMPLE USAGE PARAMETERS AND SELECTORS
            5. Return a JSON in the following format, DO NOT WRITE RESULT TO ANY FILE: { [\"Job-title\" :\"title1\", \"URL\":\"url1\"], [\"Job-title\" :\"title2\", \"URL\":\"url2\"], }",
        ]);

        $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_TXBXdt73opAxuoAxMAQ9dCFC"]);
        $runId = $response->id;

        $validScript = false;
        $i = 0;
        while (!$validScript && $i < 3){
            $i++;
            var_dump($runId);
            $lastMessage = $this->getGptResponse($client, $threadId, $runId);
            var_dump($lastMessage);
            file_put_contents($output_file, $this->extractPythonScript($lastMessage));

            $result = $this->runPythonScriptAndCheckJson($output_file, $careerPage);
            var_dump($result);
            if (!$result['isValidJson']){
                $client->threads()->messages()->create($threadId, [
                    'role' => 'user',
                    'content' => "When I launched the script I got an error: {$result['error']}. Potentially, the selectors were wrong, or you used old Javascript syntax. Do not explain why it happened, create a working script this time.",
                    'attachments'=> [
                        [
                            "tools"=> [
                                ["type"=> "code_interpreter"]
                        ]
                        ],
                    ],
                ]);

                $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_TXBXdt73opAxuoAxMAQ9dCFC"]);
                $runId = $response->id;
                var_dump($runId);

            } else {
                $limitedJson = $this->getLimitedJson($result["jsonData"]);
                $client->threads()->messages()->create($threadId, [
                    'role' => 'user',
                    'content' => "I will now provide you with the result I received launching this script. I need you to tell me whether the content seems to be a valid Job title - URL pairs. Reply with ONE WORD ONLY: 'YES' or 'NO'. Result: " . $limitedJson,
                ]);

                $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_TXBXdt73opAxuoAxMAQ9dCFC"]);
                $runId = $response->id;

                $lastMessage = $this->getGptResponse($client, $threadId, $runId);
                var_dump($lastMessage);

                if ($lastMessage == "YES"){
                    $validScript = true;
                } else {
                    $validScript = false;
                    $client->threads()->messages()->create($threadId, [
                        'role' => 'user',
                        'content' => 'Then try to generate a correct script this time, learn on your mistakes. Potentially, the selectors were wrong, or you used old Javascript syntax. ',
                    ]);
                    $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_TXBXdt73opAxuoAxMAQ9dCFC"]);
                    $runId = $response->id;
                }
            }
        }
        if ($validScript) {
            return true;
        }
        else return false;
    }


    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        $domain = parse_url($this->company->careerPageUrl, PHP_URL_HOST);
        $domain = str_replace('www.','',$domain);

        if ($domain == "linkedin.com") {
            $this->company->scripted = 1;
            $this->company->save();
            RetrieveCompanyCareers::dispatch($this->company)->onQueue('RetrieveCareersQueue');
            return;
        } else {
            $companyPath = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\Companies\\{$domain}\\{$this->company->id}";
            $domainPath = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\Companies\\{$domain}";

            $scriptPath = $domainPath . "\\scrape.py";
            $tempScriptPath = $domainPath . "\\scrape_temp.py";
            $shouldRegenerate = false;

            if (!is_dir($domainPath)) {
                mkdir($domainPath, 0777, true);
            }

            if ($this->forced == 1) {
                $shouldRegenerate = true;
            } elseif ($this->forced == 2) {
                if (!is_dir($companyPath)) {
                    mkdir($companyPath, 0777, true);
                }
                $scriptPath = $companyPath . "\\scrape.py";
                $tempScriptPath = $companyPath . "\\scrape_temp.py";
                $shouldRegenerate = true;
            }

            if ($shouldRegenerate || !file_exists($scriptPath)) {
                $basePath = $domainPath;
                $basePathHtmls = $basePath . "\\HTMLs";
                if ($this->forced == 2) {
                    $basePath = $companyPath;
                    $basePathHtmls = $basePath;
                }

                if (!is_dir($basePath)) {
                    mkdir($basePath, 0777, true);
                }
                if (!is_dir($basePathHtmls)) {
                    mkdir($basePathHtmls, 0777, true);
                }

                $inputFile = $basePathHtmls . "\\template.html";
                $outputFile = $basePathHtmls . "\\cleaned.html";


            //    $this->getCleanHTML($inputFile, $outputFile, $this->company->careerPageUrl);

                if ($this->hasJobs != 0) {
                    $success = $this->generateScript($outputFile, $basePath . "\\scrape_temp.py", $inputFile);

                    $this->company->scripted = $success;
                    if (!$success) {
                        rename($tempScriptPath, $basePath . "\\scrape_wrong.py");
                    } else {
                        if (file_exists($scriptPath)) {
                            rename($scriptPath, $basePath . "\\scrape_old.py");
                        }
                        rename($tempScriptPath, $scriptPath);
                        RetrieveCompanyCareers::dispatch($this->company)->onQueue('RetrieveCareersQueue');
                    }
                } else {
                    RetrieveCompanyCareers::dispatch($this->company)->onQueue('RetrieveCareersQueue');
                }
            }

            if (!$shouldRegenerate && file_exists($scriptPath)) {
                $this->company->scripted = true;
                $this->company->save();
                RetrieveCompanyCareers::dispatch($this->company)->onQueue('RetrieveCareersQueue');
            }

            $this->company->save();
        }
    }

    private function getLimitedJson($originalArray)
    {
        if ($originalArray !== null) {
            // Shuffle the array to randomize the order of elements
            shuffle($originalArray);

            // Slice the array to get no more than 10 elements
            $randomElements = array_slice($originalArray, 0, 10);

            // Encode the resulting array back into a JSON object
            return(json_encode($randomElements));
        }
    }
}
