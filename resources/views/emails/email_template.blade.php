<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LittleBirds.io Job Updates</title>
</head>
<body style="font-family: 'Arial', sans-serif; background-color: #ffffff; color: #333;">
<div style="background-color: #e8f4f8; padding: 20px; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 600px;">
    <h2 style="color: #327ab7;">Latest Chirps from LittleBirds.io!</h2>
    <p>New opportunities waiting for you to seize them:</p>
@foreach($companiesToSend as $company)
    <!-- Example Block for a Company -->
        <div style="background-color: #ffffff; padding: 15px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="color: #327ab7; font-size: 20px; font-weight: bold; margin-bottom: 15px;">{{$company->name}}</div>
            <div>Last time we emailed you about {{$company->name}} {{$company->contacted->format('m-d-Y')}}</div>
            <table style="width: 100%;">
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
                    <td>{{count($newJobs[$company->id]['week']['all'])}}</td>
                </tr>
                <tr>
                    <td>This month</td>
                    <td>{{count($newJobs[$company->id]['month']['relevant'])}}</td>
                    <td>{{count($newJobs[$company->id]['month']['all'])}}</td>
                </tr>
                </tbody>
            </table>
            <ul>
                @foreach($newJobs[$company->id]['today']['relevant'] as $job)
                    <li><a href="{{$job->url}}" target="_blank" style="color: #327ab7; text-decoration: none;">{{$job->title}}</a></li>
                @endforeach
            </ul>
        </div>
        <!-- End of Company Block -->
@endforeach
<!-- Repeat the company block for each company with new job openings -->

    <div style="text-align: center; margin-top: 20px; font-size: 12px; color: #777;">
        <p>Thank you for using LittleBirds.io.</p>
    </div>
</div>
</body>
</html>
