@echo off
cd /d D:\Mind\CRA\AI_Experiments\Job_Crawlers\Peter\adminlte-generator
php artisan queue:work --queue=ScriptGenerationQueue
