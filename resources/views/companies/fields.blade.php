<!-- Name Field -->
<div class="form-group col-sm-6">
    {!! Form::label('name', 'Name:') !!}
    {!! Form::text('name', null, ['class' => 'form-control']) !!}
</div>

<div class="form-group col-sm-6">
    {!! Form::label('website', 'Website:') !!}
    {!! Form::text('website', null, ['class' => 'form-control']) !!}
</div>

<!-- Careerpageurl Field -->
<div class="form-group col-sm-6">
    {!! Form::label('careerPageUrl', 'Careerpageurl:') !!}
    {!! Form::text('careerPageUrl', null, ['class' => 'form-control']) !!}
</div>

<!-- Contacted Field -->
<div class="form-group col-sm-6">
    {!! Form::label('contacted', 'Contacted:') !!}
    {!! Form::text('contacted', null, ['class' => 'form-control','id'=>'contacted']) !!}
</div>

<div class="form-group col-sm-6">
    {!! Form::label('proxy_country', 'Proxy Country:') !!}
    {!! Form::text('proxy_country', null, ['class' => 'form-control']) !!}
</div>

@push('page_scripts')
    <script type="text/javascript">
        $('#contacted').datetimepicker({
            format: 'YYYY-MM-DD HH:mm:ss',
            useCurrent: true,
            sideBySide: true
        })
    </script>
@endpush

<!-- Sauroned Field -->
<div class="form-group col-sm-6">
    <div class="form-check">
        {!! Form::hidden('sauroned', 0, ['class' => 'form-check-input']) !!}
        {!! Form::checkbox('sauroned', '1', null, ['class' => 'form-check-input']) !!}
        {!! Form::label('sauroned', 'Sauroned', ['class' => 'form-check-label']) !!}
    </div>
</div>
