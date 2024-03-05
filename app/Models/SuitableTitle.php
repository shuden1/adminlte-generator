<?php

namespace App\Models;

use Eloquent as Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Factories\HasFactory;

/**
 * Class SuitableTitle
 * @package App\Models
 * @version December 10, 2023, 9:14 am UTC
 *
 * @property string $title
 * @property string $location
 */
class SuitableTitle extends Model
{
    use SoftDeletes;

    use HasFactory;

    public $table = 'suitable_titles';


    protected $dates = ['deleted_at'];



    public $fillable = [
        'title',
        'location'
    ];

    /**
     * The attributes that should be casted to native types.
     *
     * @var array
     */
    protected $casts = [
        'title' => 'string',
        'location' => 'string'
    ];

    /**
     * Validation rules
     *
     * @var array
     */
    public static $rules = [
        'title' => 'required'
    ];

    public function users()
    {
        return $this->belongsToMany(User::class, 'suitable_title_user', 'suitable_title_id', 'user_id');
    }

}
