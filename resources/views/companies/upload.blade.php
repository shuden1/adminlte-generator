@extends('layouts.app')

@section('content')
    <section class="content-header">
        <div class="container-fluid">
            <div class="row mb-2">
                <div class="col-sm-12">
                    <h1>Upload CSV file</h1>
                </div>
            </div>
        </div>
    </section>


    <div class="content px-3">
    <form action="{{ route('companies.import') }}" method="POST" enctype="multipart/form-data">
        @csrf
        <input type="file" name="file" required>
        <button type="submit">Import CSV</button>
    </form>
    </div>
@endsection
