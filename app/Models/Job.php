<?php

namespace App\Models;

use Eloquent as Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Factories\HasFactory;

/**
 * Class Job
 * @package App\Models
 * @version December 9, 2023, 12:45 pm UTC
 *
 * @property integer $company_id
 * @property string $title
 * @property string $url
 * @property string $date
 */
class Job extends Model
{
    use SoftDeletes;

    use HasFactory;

    public $table = 'jobs';


    protected $dates = ['deleted_at'];



    public $fillable = [
        'company_id',
        'title',
        'url',
        'date'
    ];

    /**
     * The attributes that should be casted to native types.
     *
     * @var array
     */
    protected $casts = [
        'company_id' => 'integer',
        'title' => 'string',
        'url' => 'string',
        'date' => 'date'
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

    public function users()
    {
        return $this->belongsToMany(User::class)->withPivot('provided_at');
    }


}
