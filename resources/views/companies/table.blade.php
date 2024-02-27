<div class="table-responsive">
    {{ $companies->links() }}
    <table class="table" id="companies-table">
        <thead>
        <tr>
            <th>Name</th>
            <th>Careerpageurl</th>
            <th>Contacted</th>
            <th>Sauroned</th>
            <th>Scripted</th>
            <th colspan="3">Action</th>
        </tr>
        </thead>
        <tbody>
        @foreach($companies as $company)
            <tr id="company-row-{{ $company->id }}" style="{{ !$company->scripted ? 'background-color: #e57373' : ($company->jobs()->exists() ? 'background-color: #97d5a3' : 'background-color: #ece287') }}">
                <td>{{ $company->name }}</td>
                <td class="col-5">{{ $company->careerPageUrl }}</td>
                <td>{{ $company->contacted }}</td>
                <td>{{ $company->sauroned }}</td>
                <td>{{ $company->scripted }} </td>
                <td width="120">
                    <div class='btn-group'>
                        <a href="{{ route('companies.show', [$company->id]) }}"
                           class='btn btn-default btn-xs'>
                            <i class="far fa-eye"></i>
                        </a>
                        <a href="{{ route('companies.edit', [$company->id]) }}"
                           class='btn btn-default btn-xs'>
                            <i class="far fa-edit"></i>
                        </a>
                        {!! Form::open(['route' => ['companies.regenerate', $company->id], 'method' => 'post']) !!}
                        {!! Form::button('<i class="fas fa-magic"></i>', ['type' => 'submit', 'class' => 'btn btn-warning btn-xs', 'onclick' => "return confirm('Do you really want to generate another script for this domain?')"]) !!}
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



