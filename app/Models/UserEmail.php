<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class UserEmail extends Model
{
    protected $table = 'user_email';

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
