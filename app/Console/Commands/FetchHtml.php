<?php



namespace App\Console\Commands;

use Illuminate\Console\Command;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class FetchHtml extends Command
{

    protected $signature = 'fetch:html {url} {outputFile}';
    protected $description = 'Fetch HTML from a dynamic website';

    public function handle()
    {
        $url = $this->argument('url');
        $outputFile = $this->argument('outputFile');

        $phpScriptPath = base_path('ParkerScripts/IsolatedScripts/html_fetch.php'); // Adjust the path

        $process = new Process(['C:\xampp\php\php.exe', $phpScriptPath, $url, $outputFile]);
        $process->run();

        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        $this->info('HTML fetched successfully.');
    }
}

