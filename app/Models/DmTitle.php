<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class DmTitle extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
    ];

    public function users()
    {
        return $this->belongsToMany(User::class, 'user_dm_title', 'dm_title_id', 'user_id');
    }
}
