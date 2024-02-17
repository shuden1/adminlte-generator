@component('mail::message')
    # New Job Posted

    {{$job->company->name}} posted a new opening: "{{ $job->title }}".

    @component('mail::button', ['url' => $job->url])
        View Job
    @endcomponent

    @component('mail::button', ['url' => $job->company->careerPageUrl])
        All Job Postings
    @endcomponent


    Thanks,<br>
    {{ config('app.name') }}
@endcomponent
