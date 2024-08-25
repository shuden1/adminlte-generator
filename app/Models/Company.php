<?php

namespace App\Models;

use Eloquent as Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Factories\HasFactory;

/**
 * Class Company
 * @package App\Models
 * @version December 9, 2023, 12:22 pm UTC
 *
 * @property string $name
 * @property string $website
 * @property string $careerPageUrl
 * @property string $contacted
 * @property boolean $sauroned
 * @property string $proxy_country
 */
class Company extends Model
{
    use SoftDeletes;

    use HasFactory;

    public $table = 'companies';


    protected $dates = ['deleted_at'];



    public $fillable = [
        'name',
        'website',
        'careerPageUrl',
        'linkedin_id',
        'contacted',
        'sauroned',
        'scripted',
        'proxy_country'
    ];

    /**
     * The attributes that should be casted to native types.
     *
     * @var array
     */
    protected $casts = [
        'name' => 'string',
        'website' => 'string',
        'careerPageUrl' => 'string',
        'linkedin_id' => 'string',
        'contacted' => 'date',
        'sauroned' => 'boolean',
        'scripted' => 'boolean',
        'proxy_country' => 'string'
    ];

    /**
     * Validation rules
     *
     * @var array
     */
    public static $rules = [
        'name' => 'required',
        'careerPageUrl' => 'required'
    ];

    public function decisionMakers()
    {
        return $this->hasMany(DecisionMaker::class);
    }

    public function jobs()
    {
        return $this->hasMany(Job::class);
    }

    public function jobStatuses()
    {
        return $this->hasMany(JobStatus::class);
    }

    public function users()
    {
        return $this->belongsToMany(User::class);
    }

}
