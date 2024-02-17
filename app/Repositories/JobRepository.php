<?php

namespace App\Repositories;

use App\Models\Job;
use App\Repositories\BaseRepository;
use Illuminate\Support\Facades\Auth;

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
        if (!Auth::check()) {
            // Handle the case for unauthenticated users appropriately
            return []; // Or however you wish to handle this scenario
        }

        $userId = Auth::id(); // Get the current authenticated user's ID

        $jobs = Job::with('company')
            ->whereHas('company', function ($query) use ($userId) {
                $query->whereNull('deleted_at') // Ensure the company is not soft-deleted
                ->whereHas('users', function ($subQuery) use ($userId) {
                    $subQuery->where('users.id', $userId); // Filter companies by the current user
                });
            })
            ->get(); // Or ->paginate(25) if you want pagination

        return $jobs;
    }

    public function findByCompanyId($companyId)
    {
        // Assuming you have the company_id column in your decision_makers table
        return Job::where('company_id', $companyId)
            ->get();
    //        ->paginate(25);
    }

}
