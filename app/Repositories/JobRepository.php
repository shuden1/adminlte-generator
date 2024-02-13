<?php

namespace App\Repositories;

use App\Models\Job;
use App\Repositories\BaseRepository;

/**
 * Class JobRepository
 * @package App\Repositories
 * @version December 9, 2023, 12:45 pm UTC
*/

class JobRepository extends BaseRepository
{
    /**
     * @var array
     */
    protected $fieldSearchable = [
        'company_id',
        'title',
        'url',
        'date'
    ];

    /**
     * Return searchable fields
     *
     * @return array
     */
    public function getFieldsSearchable()
    {
        return $this->fieldSearchable;
    }

    /**
     * Configure the Model
     **/
    public function model()
    {
        return Job::class;
    }


    public function allWithNonDeletedCompanies()
    {
        return Job::with('company')
            ->whereHas('company', function ($query) {
                $query->whereNull('deleted_at');
            })
        ->get();
  //          ->paginate(25);
    }

    public function findByCompanyId($companyId)
    {
        // Assuming you have the company_id column in your decision_makers table
        return Job::where('company_id', $companyId)
            ->get();
    //        ->paginate(25);
    }

}
