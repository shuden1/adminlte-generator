<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OAuthToken extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id', 'access_token', 'refresh_token', 'expires_in'
    ];

    // If you're using a different name for the tokens table, specify it here
    protected $table = 'o_auth_tokens';
}
