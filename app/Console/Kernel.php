<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{
    /**
     * Define the application's command schedule.
     *
     * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
     * @return void
     */
    protected function schedule(Schedule $schedule)
    {
        //crontab -e
        //cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
        $schedule->exec('python ' . env('SCRIPTS_PATH') . DIRECTORY_SEPARATOR .'chrome_profile_cleaner.py')
            ->everyTwentyMinutes();
        $schedule->command('send:daily-emails')
            ->dailyAt('16:00');

    }

    protected $commands = [
        Commands\RenameCompanyScript::class,
    ];

    /**
     * Register the commands for the application.
     *
     * @return void
     */
    protected function commands()
    {
        $this->load(__DIR__.'/Commands');

        require base_path('routes/console.php');
    }
}
