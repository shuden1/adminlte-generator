<!-- Company Id Field -->
<div class="col-sm-12">
    {!! Form::label('company_id', 'Company Id:') !!}
    <p>{{ $decisionMaker->company_id }}</p>
</div>

<!-- Firstname Field -->
<div class="col-sm-12">
    {!! Form::label('firstName', 'Firstname:') !!}
    <p>{{ $decisionMaker->firstName }}</p>
</div>

<!-- Lastname Field -->
<div class="col-sm-12">
    {!! Form::label('lastName', 'Lastname:') !!}
    <p>{{ $decisionMaker->lastName }}</p>
</div>

<!-- Profile Url Field -->
<div class="col-sm-12">
    {!! Form::label('profile_url', 'Profile Url:') !!}
    <p>{{ $decisionMaker->profile_url }}</p>
</div>

<!-- Email Field -->
<div class="col-sm-12">
    {!! Form::label('email', 'Email:') !!}
    <p>{{ $decisionMaker->email }}</p>
</div>

<!-- Created At Field -->
<div class="col-sm-12">
    {!! Form::label('created_at', 'Created At:') !!}
    <p>{{ $decisionMaker->created_at }}</p>
</div>

<!-- Updated At Field -->
<div class="col-sm-12">
    {!! Form::label('updated_at', 'Updated At:') !!}
    <p>{{ $decisionMaker->updated_at }}</p>
</div>

