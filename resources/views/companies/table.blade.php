<div class="table-responsive">
    {{ $companies->links() }}
    <table class="table table-fixed" id="companies-table">
        <thead>
        <tr>
            <th class="col-2"><a href="{{ route('companies.index', ['sort' => 'name', 'direction' => $direction == 'asc' ? 'desc' : 'asc']) }}">Name</a></th>
            <th class="col-2"><a href="{{ route('companies.index', ['sort' => 'website', 'direction' => $direction == 'asc' ? 'desc' : 'asc']) }}">Website</a></th>
            <th class="col-3"><a href="{{ route('companies.index', ['sort' => 'careerPageUrl', 'direction' => $direction == 'asc' ? 'desc' : 'asc']) }}">Careerpageurl</a></th>
            <th class="col-2"><a href="{{ route('companies.index', ['sort' => 'contacted', 'direction' => $direction == 'asc' ? 'desc' : 'asc']) }}">Sent</a></th>
            <th class="col-1" colspan="1"><a href="{{ route('companies.index', ['sort' => 'sauroned', 'direction' => $direction == 'asc' ? 'desc' : 'asc']) }}">Sauroned</a></th>
            <th class="col-1" colspan="1"><a href="{{ route('companies.index', ['sort' => 'scripted', 'direction' => $direction == 'asc' ? 'desc' : 'asc']) }}">Scripted</a></th>
            <th class="col-2" colspan="3">Action</th>

        </tr>
        </thead>
        <tbody>
        @foreach($companies as $company)
            <tr id="company-row-{{ $company->id }}" style="{{ !$company->scripted ? 'background-color: #e57373' : ($company->jobs()->exists() ? 'background-color: #97d5a3' : 'background-color: #ece287') }}">
                <td class="col-2">{{ $company->name }}</td>
                <td class="col-2">{{ $company->website }}</td>
                <td class="col-4" style="word-break: break-word">
                    <a href="{{ $company->careerPageUrl }}" target="_blank">{{ $company->careerPageUrl }}</a></td>
                <td class="col-2">{{ $company->contacted }}</td>
                <td class="col-1">{{ $company->sauroned }}</td>
                <td class="col-1">{{ $company->scripted }} </td>
                <td  class="col-2">
                    <div class='btn-group'>
                        <a href="{{ route('companies.show', [$company->id]) }}"
                           class='btn btn-default btn-xs'>
                            <i class="far fa-eye"></i>
                        </a>
                        <a href="{{ route('companies.edit', [$company->id]) }}"
                           class='btn btn-default btn-xs'>
                            <i class="far fa-edit"></i>
                        </a>
                        {!! Form::open(['route' => ['companies.regenerate', $company->id, 1], 'method' => 'post']) !!}
                        {!! Form::button('<i class="fas fa-magic"></i>', ['type' => 'submit', 'class' => 'btn btn-warning btn-xs', 'onclick' => "return confirm('Do you really want to generate another script for this domain?')"]) !!}
                        {!! Form::close() !!}

                        {!! Form::open(['route' => ['companies.regenerate', $company->id, 2], 'method' => 'post']) !!}
                        {!! Form::button('<i class="fa fa-solid fa-dog"></i>', ['type' => 'submit', 'class' => 'btn btn-warning btn-xs', 'onclick' => "return confirm('Do you really want to generate another script for this domain?')"]) !!}
                        {!! Form::close() !!}


                        {!! Form::open(['route' => ['companies.destroy', $company->id], 'method' => 'delete']) !!}
                        {!! Form::button('<i class="far fa-trash-alt"></i>', ['type' => 'submit', 'class' => 'btn btn-danger btn-xs', 'onclick' => "return confirm('Are you sure?')"]) !!}
                        {!! Form::close() !!}
                    </div>
                </td>
            </tr>
        @endforeach
        </tbody>
    </table>
</div>

<script>

 /*
    window.Echo = new Echo({
        broadcaster: 'pusher',
        host: window.location.hostname + ':6001' // Your WebSocket server address
    });

    window.Echo.channel('job-status')
        .listen('JobStatusUpdated', (e) => {
            console.log('Event received:', e);
            const row = document.querySelector(`#company-row-${e.companyId}`);
            if (row) {
                if (e.status === 'completed') {
                    // Fetch the updated company data
                    fetch(`/companies/get/${e.companyId}`)
                        .then(response => response.json())
                        .then(data => {
                            row.style.backgroundColor = data.scripted ? '#97d5a3' : '#e57373'; // Green if scripted is true, red if false
                        });
                } else {
                    row.style.backgroundColor = '#ece287'; // Yellow for pending
                }
            }
        });
    */
</script>



