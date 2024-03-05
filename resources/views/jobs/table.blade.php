<div class="table-responsive">
     <table class="table" id="jobs-table">
        <thead>
        <tr>
            <th class="col-2">Company Id</th>
            <th class="col-2">Title</th>
            <th class="col-3">Url</th>
            <th class="col-3">Date</th>
            <th class="col-2" colspan="3">Action</th>
        </tr>
        </thead>
        <tbody>
        @foreach($jobs as $job)
            <tr>
                <td class="col-2">{{ $job->company->name }}</td>
                <td class="col-2" style="word-break: break-word">{{ $job->title }}</td>
                <td class="col-3" style="word-break: break-word"><a href="{{ $job->url }}" target="_blank">{{ $job->url }}</a></td>
                <td class="col-3">{{ $job->date }}</td>
                <td class="col-2">
                    {!! Form::open(['route' => ['jobs.destroy', $job->id], 'method' => 'delete']) !!}
                    <div class='btn-group'>
                        <a href="{{ route('jobs.show', [$job->id]) }}"
                           class='btn btn-default btn-xs'>
                            <i class="far fa-eye"></i>
                        </a>
                        <a href="{{ route('jobs.edit', [$job->id]) }}"
                           class='btn btn-default btn-xs'>
                            <i class="far fa-edit"></i>
                        </a>
                        {!! Form::button('<i class="far fa-trash-alt"></i>', ['type' => 'submit', 'class' => 'btn btn-danger btn-xs', 'onclick' => "return confirm('Are you sure?')"]) !!}
                    </div>
                    {!! Form::close() !!}
                </td>
            </tr>
        @endforeach
        </tbody>
    </table>
</div>
