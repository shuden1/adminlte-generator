<?php

require 'D:\Mind\CRA\AI_Experiments\Job_Crawlers\Peter\adminlte-generator\vendor\autoload.php';

$app = require_once 'D:\Mind\CRA\AI_Experiments\Job_Crawlers\Peter\adminlte-generator\bootstrap\app.php';

$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();

use App\Jobs\SendTelegramMessage;
use App\Models\User;

$user = User::find(2);
$chatId = '-1002178752602';
SendTelegramMessage::dispatch($user, $chatId);
