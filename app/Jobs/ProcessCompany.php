<?php

namespace App\Jobs;

use App\Events\JobStatusUpdated;
use App\Models\Company;
use App\Models\DomainFolder;
use App\Models\JobStatus;
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

class ProcessCompany implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $company;
    protected $forced;

    public $timeout = 1200;

    /**
     * Create a new job instance.
     *
     * @return void
     */
    public function __construct(Company $company, $forced = false)
    {
        $this->company = $company;
        $this->forced = $forced;
        $this->queue = 'ScriptGenerationQueue';
    }


    public function getCleanHTML($inputFile, $outputFile, $careerPageURL)
    {
        $command = "C:\\Python3\\python.exe"." D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\html_fetch_iframes.py \"".$careerPageURL."\" \"".$inputFile."\"";
        exec($command, $output1, $returnStatus1);


        // Call sculpting.py
        $command2 = "C:\\Python3\\python.exe D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\sculpting.py \"" . $inputFile . "\" \"" . $outputFile . "\"";

// Execute the second script and wait for it to finish
        exec($command2, $output2, $returnStatus2);

        if ($returnStatus2 !==0 ) {
            throw new \Exception($returnStatus2);
        }

        $filesizeKB = filesize($outputFile) / 1024;
        if ($filesizeKB<3){
            $command = "C:\\Python3\\python.exe"." D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\html_fetch_iframes.py \"".$careerPageURL."\" \"".$inputFile."\"";
            exec($command, $output1, $returnStatus1);

            // Call sculpting.py
            $command2 = "C:\\Python3\\python.exe D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\sculpting.py \"" . $inputFile . "\" \"" . $outputFile . "\"";

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
                'assistant_id' => 'asst_oeImsIdj5jJkDOH5WBhxBagT',
                'thread' => [
                    'messages' =>
                        [
                            [
                                'role' => 'user',
                                'content' => 'Use this file, you can retrieve it and follow your instructions.',
                                'file_ids' => [$fileId]
                            ],
                        ],
                ],
            ],
        );
        $runId = $response->id;
        $threadId = $response->threadId;

        $validScript = false;
        $i = 0;
        while (!$validScript && $i < 5){
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
                    'content' => "When I launched the script I got an error: {$result['error']}. Do not explain why it happened, just create another working script.",
                    'file_ids' => [$fileId]
                ]);

                $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_oeImsIdj5jJkDOH5WBhxBagT"]);
                $runId = $response->id;
                var_dump($runId);

            } else {
                $limitedJson = $this->getLimitedJson($result["jsonData"]);
                $client->threads()->messages()->create($threadId, [
                    'role' => 'user',
                    'content' => "I will now provide you with the result I received launching this script. I need you to tell me whether the content seems to be a valid Job title - URL pairs. Reply with ONE WORD ONLY: 'YES' or 'NO'. Result: " . $limitedJson,
                ]);

                $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_oeImsIdj5jJkDOH5WBhxBagT"]);
                $runId = $response->id;

                $lastMessage = $this->getGptResponse($client, $threadId, $runId);
                var_dump($lastMessage);

                if ($lastMessage == "YES"){
                    $validScript = true;
                } else {
                    $validScript = false;
                    $client->threads()->messages()->create($threadId, [
                        'role' => 'user',
                        'content' => ' Then try to generate a correct script this time, learn on your mistakes.',
                        'file_ids' => [$fileId]
                    ]);
                    $response = $client->threads()->runs()->create($threadId,['assistant_id' =>"asst_oeImsIdj5jJkDOH5WBhxBagT"]);
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
/*
         $jobStatus = JobStatus::create([
            'company_id' => $this->company->id,
            'job_id' => $this->job->getJobId(),
            'status' => 'processing',
        ]);
*/

        $domain = parse_url($this->company->careerPageUrl, PHP_URL_HOST);
        $domain = str_replace('www.','',$domain);


        if ((!file_exists("D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape.py"))||($this->forced)) {

            if (file_exists("D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape.py")) {
                rename("D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape.py", "D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape_old.py");
            }

            $basePath = "D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}";
            $basePathHtmls = "D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/HTMLs";

            if (!is_dir($basePath)) {
                mkdir($basePath, 0777, true); // The 0777 specifies the permissions, and true enables recursive creation
            }
            if (!is_dir($basePathHtmls)) {
                mkdir($basePathHtmls, 0777, true); // The 0777 specifies the permissions, and true enables recursive creation
            }

            //     Call fetch_html.py
            $inputFile = $basePathHtmls . "/template.html";
            $outputFile = $basePathHtmls . "/cleaned.html";
            $this->getCleanHTML($inputFile, $outputFile, $this->company->careerPageUrl);
            //     Call GenerateScripts


            $success = $this->generateScript($outputFile, $basePath . "/scrape.py", $inputFile);

            $this->company->scripted = $success;
            if (!$success){
                rename("D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape.py", "D:/Mind/CRA/AI_Experiments/Job_Crawlers/Peter/adminlte-generator/ParkerScripts/Companies/{$domain}/scrape_wrong.py");
            } else {
                RetrieveCompanyCareers::dispatch($this->company)->onQueue('RetrieveCareersQueue');

            }

            //      sleep(10);
            //      $jobStatus->update(['status' => 'completed']);
            //      JobStatusUpdated::dispatch($this->company->id, "completed");

        } else{
            $this->company->scripted = 1;
            RetrieveCompanyCareers::dispatch($this->company)->onQueue('RetrieveCareersQueue');
        }
        $this->company->save();
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
