<?php

namespace App\Repositories;

use App\Models\SuitableTitle;
use App\Repositories\BaseRepository;

/**
 * Class SuitableTitleRepository
 * @package App\Repositories
 * @version December 10, 2023, 9:14 am UTC
*/

class SuitableTitleRepository extends BaseRepository
{
    /**
     * @var array
     */
    protected $fieldSearchable = [
        'title',
        'location'
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
        return SuitableTitle::class;
    }
}
