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

    public $tries = 2;
    public $timeout = 2000;

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
        $this->queue = 'ScriptGenerationQueue'.rand(1, env("SCRIPT_GENERATION_QUEUE_COUNT"));
    }

    public function failed(Exception $exception)
    {
        // Send user notification of failure, etc...
        Log::error("Job failed. Exception: {$exception->getMessage()}");
    }

    public function getCleanHTML($inputFile, $outputFile, $careerPageURL, $domain)
    {
        $pythonPath = env('PYTHON_PATH');

        if (preg_match('/^hh\.[a-z]+$/', $domain)) {
            $fetchScriptPath = env("HH_FETCH_SCRIPT_PATH");
        } else
            $fetchScriptPath = env("FETCH_SCRIPT_PATH");

        if ($this->company->proxy_country){
            $command = $pythonPath." ".$fetchScriptPath." \"".$careerPageURL."\" \"".$inputFile."\" \"".$this->company->proxy_country."\"";
        } else
        $command = $pythonPath." ".$fetchScriptPath." \"".$careerPageURL."\" \"".$inputFile."\"";

        exec($command, $output1, $returnStatus1);


        // Call sculpting.py
        $command2 = $pythonPath." ".env("SCULPTING_SCRIPT_PATH")." \"" . $inputFile . "\" \"" . $outputFile . "\"";

// Execute the second script and wait for it to finish
        exec($command2, $output2, $returnStatus2);

        if ($returnStatus2 !==0 ) {
            throw new \Exception($returnStatus2);
        }

        $filesizeKB = filesize($outputFile) / 1024;
        if ($filesizeKB<3){
            $command = $pythonPath." ".$fetchScriptPath." \"".$careerPageURL."\" \"".$inputFile."\"";
            exec($command, $output1, $returnStatus1);

            // Call sculpting.py
            $command2 = $pythonPath." ".env("SCULPTING_SCRIPT_PATH")." \"" . $inputFile . "\" \"" . $outputFile . "\"";

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
        while (($statusCheck->status != "completed") && ($counter < 30)){
            $counter++;
            sleep(3);
            $statusCheck = $client->threads()->runs()->retrieve($threadId,$runId);
        }
        var_dump("Step took ".$statusCheck->usage->totalTokens." tokens");

        $messageList = $client->threads()->messages()->list($threadId, [
            'limit' => 1,
        ]);
        $message = $client->threads()->messages()->retrieve($threadId,$messageList->firstId);
        return ($message->content[0]->text->value);
    }

    function uploadFileWithRetry($client, $input_file, $maxRetries = 8) {
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

        $step_1_message = "First, find Job Openings posted on this HTML. Respond only with maximum three Job titles PRESENTED ON THIS HTML. \n
            If you cannot find any Job Openings, respond with 'No Job Openings Found'";


        $response = $client->threads()->createAndRun(
            [
                'assistant_id' => 'asst_TXBXdt73opAxuoAxMAQ9dCFC',
                'thread' => [
                    'messages' =>
                        [
                            [
                            'role' => 'user',
                            'content' => $step_1_message,
                            'attachments'=> [
                                [
                                    "file_id"=> $fileId,
                                    "tools" => [
                                        ["type"=> "file_search"]
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
        var_dump("Step 1");
        $lastMessage = $this->getGptResponse($client, $threadId, $runId);

        if ($lastMessage == $step_1_message){
            $lastMessage = $this->getGptResponse($client, $threadId, $runId);
        }
        var_dump($lastMessage);

        if ($lastMessage == "No Job Openings Found"){
            return false;
        }

        $step_2_message = "Now having the Job Opening titles, find them in this HTML. THEY ARE IN THE HTML YOU HAVE ALREADY FOUND THEM PREVIOUSLY.\n
            Next, analyze the HTML elements that contains those titles and define common JavaScript selectors for All Job Postings presented in this HTML. \n
            Respond in the following format: \n
            Job Opening elements - {HTML TAG WITH DEFINED CLASSES AND ATTRIBUTES IF REQUIRED !!!FROM THE HTML PROVIDED!!!} \n
            Job title elements - {HTML TAG WITH DEFINED CLASSES AND ATTRIBUTES IF REQUIRED !!!FROM THE HTML PROVIDED!!! } \n
            Job URL elements - {HTML TAG WITH DEFINED CLASSES AND ATTRIBUTES IF REQUIRED !!!FROM THE HTML PROVIDED!!! }";

        $client->threads()->messages()->create($threadId, [
            'role' => 'user',
            'content' => $step_2_message,
            'attachments'=> [
                [
                    "file_id"=> $fileId,
                    "tools" => [
                        ["type"=> "code_interpreter"]
                    ]
                ],
            ],
        ]);

        $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_TXBXdt73opAxuoAxMAQ9dCFC"]);
        $runId = $response->id;
        var_dump("Step 2");
        $lastMessage = $this->getGptResponse($client, $threadId, $runId);

        if ($lastMessage == $step_2_message){
            $lastMessage = $this->getGptResponse($client, $threadId, $runId);
        }

        var_dump($lastMessage);

        $client->threads()->messages()->create($threadId, [
            'role' => 'user',
            'content' => "Now create a Python + Selenium script using the latest best practices for ChromeDriver 120.0.6099.109 \n
            1. This script will be launched externally in a settled-up environment, DO NOT TEST THIS SCRIPT, CREATE IT: \n
            THE TARGET HTML FILE NAME SHOULD BE AN ARGUMENT SENT FROM AN EXTERNAL SOURCE THROUGH THE CONSOLE COMMAND AS THE SINGLE INPUT PARAMETER. DO NOT PUT ANY PLACEHOLDERS OR EXAMPLES! \n
            2. Use from selenium.common.exceptions import NoSuchElementException to add a proper exception handling and avoid failing the script if the elements do not exist. import os, import dotenv and use load_dotenv() to get access to the .env parameters.\n
            3. Initialise a headless webdriver, with this profile path, do not forget to create a relevant folder: profile_folder_path=os.getenv(\"CHROME_PROFILE_PATH\") + os.path.sep + str(threading.get_ident()). Use this service:
            service=service(executable_path=os.getenv(\"CHROME_DRIVER_PATH\")). Add these options: options.add_argument(f\"user-data-dir={profile_folder_path}\") options.add_argument(\"--headless\") options.add_argument(\"--disable-gpu\") options.add_argument(\"--no-sandbox\") \n
            4. USE THE SELECTORS AND CODE EXAMPLES YOU PREVIOUSLY DEFINED!!! and scrape all job listings. REMEMBER!!!! instead of an old find_elements_by_css_selector, you should use the find_elements method with By.CSS_SELECTOR. \n
            5. To extract Job Titles try to use get_attribute('textContent').strip() first, but if it's empty - use .get_attribute('innerHTML').strip() \n
            6. In case there is no Job Opening URL defined in the HTML - use a \"#\", BUT ONLY IF THERE IS NO URL DEFINED WITHIN THE JOB POSTING ELEMENT \n
            7. NEVER IMPLEMENT EXAMPLE USAGE PARAMETERS AND SELECTORS, ONLY THE ONES EXISTING IN THE HTML \n
            8. Return a JSON with all job postings in the following format, DO NOT WRITE RESULT TO ANY FILE: { [\"Job-title\" :\"title1\", \"URL\":\"url1\"], [\"Job-title\" :\"title2\", \"URL\":\"url2\"], }",
        ]);

        $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_TXBXdt73opAxuoAxMAQ9dCFC"]);
        $runId = $response->id;
        $validScript = false;
        $i = 3;
        $i++;
        var_dump("Step ".$i);
        $lastMessage = $this->getGptResponse($client, $threadId, $runId);
        var_dump($lastMessage);
        file_put_contents($output_file, $this->extractPythonScript($lastMessage));
        $result = $this->runPythonScriptAndCheckJson($output_file, $careerPage);
        var_dump($result);
        if (!$result['isValidJson']){
            $client->threads()->messages()->create($threadId, [
                'role' => 'user',
                'content' => "When I launched the script I got an error. /n Potentially, you used old Javascript syntax or tried to do something with the selectors that does not exist. Do not explain why it happened, create a working script this time.",
            ]);
            $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_TXBXdt73opAxuoAxMAQ9dCFC"]);
            $runId = $response->id;
            var_dump($runId);
            }
        else {
            $limitedJson = $this->getLimitedJson($result["jsonData"]);
            $client->threads()->messages()->create($threadId, [
                'role' => 'user',
                'content' => "I will now provide you with the result I received launching this script. I need you to tell me whether the content seems to be a valid Job title - URL pairs. Reply with ONE WORD ONLY: 'YES' or 'NO'. Result: " . $limitedJson,
            ]);

            $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_TXBXdt73opAxuoAxMAQ9dCFC"]);
            $runId = $response->id;

            var_dump("Step ".$i.". Response check");

            $lastMessage = $this->getGptResponse($client, $threadId, $runId);
            var_dump($lastMessage);

            if ($lastMessage == "YES"){
                $validScript = true;
            } else {
                $validScript = false;
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
            RetrieveCompanyCareers::dispatch($this->company);
            return;
        } else {
            $companyPath = env("COMPANIES_BASE_PATH").DIRECTORY_SEPARATOR.$domain.DIRECTORY_SEPARATOR.$this->company->id;
            $domainPath = env("COMPANIES_BASE_PATH").DIRECTORY_SEPARATOR.$domain;

            $scriptPath = $domainPath . DIRECTORY_SEPARATOR. "scrape.py";
            $tempScriptPath = $domainPath . DIRECTORY_SEPARATOR. "scrape_temp.py";
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
                $scriptPath = $companyPath . DIRECTORY_SEPARATOR. "scrape.py";
                $tempScriptPath = $companyPath . DIRECTORY_SEPARATOR. "scrape_temp.py";
                $shouldRegenerate = true;
            }

            if ($shouldRegenerate || !file_exists($scriptPath)) {
                $basePath = $domainPath;
                $basePathHtmls = $basePath . DIRECTORY_SEPARATOR. "HTMLs";
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

                $inputFile = $basePathHtmls . DIRECTORY_SEPARATOR. "template.html";
                $outputFile = $basePathHtmls . DIRECTORY_SEPARATOR. "cleaned.html";
                $tempScriptPath = $basePath . DIRECTORY_SEPARATOR. "scrape_temp.py";


                $this->getCleanHTML($inputFile, $outputFile, $this->company->careerPageUrl, $domain);

                if ($this->hasJobs != 0) {
                    $attempt = 1;
                    $success = false;
                    while (($attempt<3)&&(!$success)){
//                        $success = $this->generateScript($outputFile, $tempScriptPath, $inputFile);
                        $attempt++;
                    }

                    $this->company->scripted = $success;
                    if (!$success) {
                        if (file_exists($tempScriptPath) && is_readable($tempScriptPath)) {
                            rename($tempScriptPath, $basePath . DIRECTORY_SEPARATOR. "scrape_wrong.py");
                        } else {
                            echo "File does not exist or is not readable: " . $tempScriptPath;
                        }
                    } else {
                        if (file_exists($scriptPath)) {
                            rename($scriptPath, $basePath . DIRECTORY_SEPARATOR. "scrape_old.py");
                        }

                        if (file_exists($tempScriptPath) && is_readable($tempScriptPath)) {
                            rename($tempScriptPath, $scriptPath);
                        } else {
                            echo "File does not exist or is not readable: " . $tempScriptPath;
                        }
//                        RetrieveCompanyCareers::dispatch($this->company);
                    }
                } else {
                    RetrieveCompanyCareers::dispatch($this->company);
                }
            }
            var_dump($scriptPath);

            if (file_exists($scriptPath)) {
                $this->company->scripted = true;
                $this->company->save();
                RetrieveCompanyCareers::dispatch($this->company);
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
            $randomElements = array_slice($originalArray, 0, 4);

            // Encode the resulting array back into a JSON object
            return(json_encode($randomElements));
        }
    }
}
