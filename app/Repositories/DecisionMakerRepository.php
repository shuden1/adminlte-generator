<?php

namespace App\Repositories;

use App\Models\DecisionMaker;
use App\Repositories\BaseRepository;
use Illuminate\Support\Facades\Auth;

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
        if (!Auth::check()) {
            // Handle unauthenticated user case, possibly redirect or throw an exception
            return redirect()->route('login')->with('error', 'You must be logged in to access this data.');
        }

        $userId = Auth::id(); // Get the current authenticated user's ID

        return DecisionMaker::with('company')
            ->whereHas('company', function ($query) use ($userId) {
                // Filter to include only companies that are not soft deleted
                $query->whereNull('deleted_at')
                    // Further filter to include only companies associated with the current user
                    ->whereHas('users', function ($query) use ($userId) {
                        $query->where('users.id', $userId);
                    });
            })
            ->get();
        // ->paginate(25); // Uncomment to paginate results
    }

    public function findByCompanyId($companyId)
    {
        // Assuming you have the company_id column in your decision_makers table
        return DecisionMaker::where('company_id', $companyId)
            ->get();
        //    ->paginate(25);
    }


}
