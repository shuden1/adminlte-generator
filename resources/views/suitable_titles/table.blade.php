<div class="table-responsive">
    <table class="table" id="suitableTitles-table">
        <thead>
        <tr>
            <th>Title</th>
        <th>Location</th>
            <th colspan="3">Action</th>
        </tr>
        </thead>
        <tbody>
        @foreach($suitableTitles as $suitableTitle)
            <tr>
                <td>{{ $suitableTitle->title }}</td>
            <td>{{ $suitableTitle->location }}</td>
                <td width="120">
                    {!! Form::open(['route' => ['suitableTitles.destroy', $suitableTitle->id], 'method' => 'delete']) !!}
                    <div class='btn-group'>
                        <a href="{{ route('suitableTitles.show', [$suitableTitle->id]) }}"
                           class='btn btn-default btn-xs'>
                            <i class="far fa-eye"></i>
                        </a>
                        <a href="{{ route('suitableTitles.edit', [$suitableTitle->id]) }}"
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
