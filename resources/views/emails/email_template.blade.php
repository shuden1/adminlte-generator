<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LittleBirds.io Job Updates</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #ffffff; color: #333; }
        .email-container { background-color: #e8f4f8; padding: 20px; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .company-block { background-color: #ffffff; padding: 15px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .company-header { color: #327ab7; font-size: 20px; font-weight: bold; margin-bottom: 15px; }
        .jobs-table { width: 100%; }
        .jobs-table th, .jobs-table td { padding: 8px; text-align: left; border-bottom: 1px solid #eee; }
        .job-link { color: #327ab7; text-decoration: none; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #777; }
        a { color: #327ab7; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
<div class="container email-container">
    <h2 style="color: #327ab7;">Latest Chirps from LittleBirds.io!</h2>
    <p>New opportunities waiting for you to seize them:</p>
    @foreach($companiesToSend as $company)
    <!-- Example Block for a Company -->
        <div class="company-block">
            <div class="company-header">{{$company->name}}</div>
            <div>Last time we emailed you about CompanyName {{$company->contacted->format('m-d-Y')}}</div>
            <table class="jobs-table">
                <thead>
                <tr>
                    <th></th>
                    <th scope="col">Relevant Jobs</th>
                    <th scope="col">All Jobs</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>Today</td>
                    <td>{{count($newJobs[$company->id]['today']['relevant'])}}</td>
                    <td>{{count($newJobs[$company->id]['today']['all'])}}</td>
                </tr>
                <tr>
                    <td>This week</td>
                    <td>{{count($newJobs[$company->id]['week']['relevant'])}}</td>
                    <td>{{count($newJobs[$company->id]['week']['relevant'])}}</td>
                </tr>
                <tr>
                    <td>This month</td>
                    <td>{{count($newJobs[$company->id]['month']['relevant'])}}</td>
                    <td>{{count($newJobs[$company->id]['month']['relevant'])}}</td>
                </tr>
                </tbody>
            </table>
            <ul>
                @foreach($newJobs[$company->id]['today']['relevant'] as $job)
                <li><a href="{{$job->url}}" target="_blank" class="job-link">{{$job->title}}</a></li>
                @endforeach
            </ul>
        </div>
        <!-- End of Company Block -->
    @endforeach
<!-- Repeat the company block for each company with new job openings -->

    <div class="footer">
        <p>Thank you for using LittleBirds.io.</p>
    </div>
</div>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
