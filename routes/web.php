<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\EmailController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Auth::routes();

Route::get('/home', [App\Http\Controllers\HomeController::class, 'index'])->name('home');

// In your web.php or api.php
Route::get('/companies/get/{id}', 'CompanyController@getCompanyData');


Route::get('companies/upload', [App\Http\Controllers\CompanyController::class, 'upload'])->name('companies.upload');

Route::post('companies/import', [App\Http\Controllers\CompanyController::class, 'import'])->name('companies.import');

Route::post('companies/regenerate/{id}/{unique}', [App\Http\Controllers\CompanyController::class, 'regenerate'])->name('companies.regenerate');

Route::resource('companies', App\Http\Controllers\CompanyController::class);


Route::resource('jobs', App\Http\Controllers\JobController::class);


Route::resource('decisionMakers', App\Http\Controllers\DecisionMakerController::class);

Route::resource('suitableTitles', App\Http\Controllers\SuitableTitleController::class);

Route::get('/auth/google', [EmailController::class, 'redirectToGoogle']);
Route::get('/auth/google/callback', [EmailController::class, 'handleGoogleCallback']);
