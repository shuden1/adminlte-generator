<div class="table-responsive">
    <table class="table" id="decisionMakers-table">
        <thead>
        <tr>
            <th>Company Id</th>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Profile Url</th>
        <th>Email</th>
            <th colspan="3">Action</th>
        </tr>
        </thead>
        <tbody>
        @foreach($decisionMakers as $decisionMaker)
            <tr>
                <td>{{ $decisionMaker->company->name}}</td>
            <td>{{ $decisionMaker->firstName }}</td>
            <td>{{ $decisionMaker->lastName }}</td>
            <td>{{ $decisionMaker->profile_url }}</td>
            <td>{{ $decisionMaker->email }}</td>
                <td width="120">
                    {!! Form::open(['route' => ['decisionMakers.destroy', $decisionMaker->id], 'method' => 'delete']) !!}
                    <div class='btn-group'>
                        <a href="{{ route('decisionMakers.show', [$decisionMaker->id]) }}"
                           class='btn btn-default btn-xs'>
                            <i class="far fa-eye"></i>
                        </a>
                        <a href="{{ route('decisionMakers.edit', [$decisionMaker->id]) }}"
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
