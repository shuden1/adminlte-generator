<!-- Company Id Field -->
<div class="form-group col-sm-6">
    {!! Form::label('company_id', 'Company Id:') !!}
    {!! Form::select('company_id', $companyItems, null, ['class' => 'form-control custom-select']) !!}
</div>


<!-- Firstname Field -->
<div class="form-group col-sm-6">
    {!! Form::label('firstName', 'Firstname:') !!}
    {!! Form::text('firstName', null, ['class' => 'form-control']) !!}
</div>

<!-- Lastname Field -->
<div class="form-group col-sm-6">
    {!! Form::label('lastName', 'Lastname:') !!}
    {!! Form::text('lastName', null, ['class' => 'form-control']) !!}
</div>

<!-- Profile Url Field -->
<div class="form-group col-sm-6">
    {!! Form::label('profile_url', 'Profile Url:') !!}
    {!! Form::text('profile_url', null, ['class' => 'form-control']) !!}
</div>

<!-- Email Field -->
<div class="form-group col-sm-6">
    {!! Form::label('email', 'Email:') !!}
    {!! Form::text('email', null, ['class' => 'form-control']) !!}
</div>