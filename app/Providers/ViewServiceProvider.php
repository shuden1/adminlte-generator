<?php

namespace App\Providers;
use App\Models\Company;

use Illuminate\Support\ServiceProvider;
use View;

class ViewServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        View::composer(['decision_makers.fields'], function ($view) {
            $companyItems = Company::pluck('name','id')->toArray();
            $view->with('companyItems', $companyItems);
        });
        View::composer(['jobs.fields'], function ($view) {
            $companyItems = Company::pluck('name','id')->toArray();
            $view->with('companyItems', $companyItems);
        });
        //
    }
}