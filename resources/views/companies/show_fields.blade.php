<!-- Name Field -->
<div class="col-sm-4">
    {!! Form::label('name', 'Name:') !!}
    <p>{{ $company->name }}</p>
</div>

<div class="col-sm-4">
    {!! Form::label('website', 'Website:') !!}
    <p>{{ $company->website }}</p>
</div>

<!-- Careerpageurl Field -->
<div class="col-sm-10">
    {!! Form::label('careerPageUrl', 'Careerpageurl:') !!}
    <p><a href="{{ $company->careerPageUrl }}" target="_blank">{{ $company->careerPageUrl }}</a></p>
</div>

<!-- Sauroned Field -->
<div class="col-sm-4">
    {!! Form::label('sauroned', 'Sauroned:') !!}
    <p>{{ $company->sauroned }}</p>
</div>

<div class="col-sm-8">
    {!! Form::label('Scripted', 'Scripted:') !!}
    <p>{{ $company->scripted }}</p>
</div>

<!-- Created At Field -->
<div class="col-sm-4">
    {!! Form::label('created_at', 'Created At:') !!}
    <p>{{ $company->created_at }}</p>
</div>

<!-- Updated At Field -->
<div class="col-sm-4">
    {!! Form::label('updated_at', 'Updated At:') !!}
    <p>{{ $company->updated_at }}</p>
</div>

<!-- Contacted Field -->
<div class="col-sm-4">
    {!! Form::label('contacted', 'Contacted:') !!}
    <p>{{ $company->contacted }}</p>
</div>

