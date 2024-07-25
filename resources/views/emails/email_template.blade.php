<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LittleBirds.io Job Updates</title>
</head>
<body style="font-family: 'Arial', sans-serif; background-color: #ffffff; color: #333;">
<div style="background-color: #e8f4f8; padding: 20px; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 1200px;">
    <h2 style="color: #327ab7;">Latest Chirps from LittleBirds.io!</h2>
    <p>New opportunities waiting for you to seize them:</p>
@foreach($companiesToSend as $company)
    <!-- Example Block for a Company -->
        <div style="background-color: #ffffff; padding: 15px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <span>
            <div style="color: #327ab7; font-size: 20px; font-weight: bold; margin-bottom: 15px;">{{$company->name}}</div>
            @if ($company->contacted)
            <div>Last time we emailed you about {{$company->name}} {{$company->contacted->format('m-d-Y')}}</div>
            @else
                <div></div>
            @endif
                <table style="width: 100%; border-collapse: collapse;">
                <thead>
                <tr>
                    <th style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;"></th>
                    <th scope="col" style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">Relevant Jobs</th>
                    <th scope="col" style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">All Jobs</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">Today</td>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">{{count($newJobs[$company->id]['today']['relevant'])}}</td>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">{{count($newJobs[$company->id]['today']['all'])}}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">This week</td>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">{{count($newJobs[$company->id]['week']['relevant'])}}</td>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">{{count($newJobs[$company->id]['week']['all'])}}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">This month</td>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">{{count($newJobs[$company->id]['month']['relevant'])}}</td>
                    <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">{{count($newJobs[$company->id]['month']['all'])}}</td>
                </tr>
                </tbody>
            </table>
            <ul>
                @foreach($newJobs[$company->id]['today']['relevant'] as $job)
                    <li><a href="{{$job->url}}" target="_blank" style="color: #327ab7; text-decoration: none;">{{$job->title}}</a></li>
                @endforeach
            </ul>
            </span>
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
