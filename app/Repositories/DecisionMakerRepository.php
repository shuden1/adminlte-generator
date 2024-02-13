<?php

namespace App\Repositories;

use App\Models\DecisionMaker;
use App\Repositories\BaseRepository;

/**
 * Class DecisionMakerRepository
 * @package App\Repositories
 * @version December 9, 2023, 12:51 pm UTC
*/

class DecisionMakerRepository extends BaseRepository
{
    /**
     * @var array
     */
    protected $fieldSearchable = [
        'company_id',
        'firstName',
        'lastName',
        'profile_url',
        'email'
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
        return DecisionMaker::class;
    }

    public function allWithNonDeletedCompanies()
    {
        return DecisionMaker::with('company')
            ->whereHas('company', function ($query) {
                $query->whereNull('deleted_at');
            })
            ->get();
        //    ->paginate(25);
    }

    public function findByCompanyId($companyId)
    {
        // Assuming you have the company_id column in your decision_makers table
        return DecisionMaker::where('company_id', $companyId)
            ->get();
        //    ->paginate(25);
    }


}
