<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class JobStatus extends Model
{
    use HasFactory;
    protected $fillable = ['company_id', 'job_id', 'status'];

    public function company()
    {
        return $this->belongsTo(Company::class);
    }
}
