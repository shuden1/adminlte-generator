<?php

namespace App\Models;

use Eloquent as Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Factories\HasFactory;

/**
 * Class DecisionMaker
 * @package App\Models
 * @version December 9, 2023, 12:51 pm UTC
 *
 * @property integer $company_id
 * @property string $firstName
 * @property string $lastName
 * @property string $profile_url
 * @property string $email
 */
class DecisionMaker extends Model
{
    use SoftDeletes;

    use HasFactory;

    public $table = 'decision_makers';


    protected $dates = ['deleted_at'];



    public $fillable = [
        'company_id',
        'firstName',
        'lastName',
        'profile_url',
        'email'
    ];

    /**
     * The attributes that should be casted to native types.
     *
     * @var array
     */
    protected $casts = [
        'company_id' => 'integer',
        'firstName' => 'string',
        'lastName' => 'string',
        'profile_url' => 'string',
        'email' => 'string'
    ];

    /**
     * Validation rules
     *
     * @var array
     */
    public static $rules = [

    ];

    public function company()
    {
        return $this->belongsTo(Company::class);
    }

}
