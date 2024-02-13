<?php

namespace Database\Factories;

use App\Models\DecisionMaker;
use Illuminate\Database\Eloquent\Factories\Factory;

class DecisionMakerFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = DecisionMaker::class;

    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'company_id' => $this->faker->randomDigitNotNull,
        'firstName' => $this->faker->word,
        'lastName' => $this->faker->word,
        'profile_url' => $this->faker->word,
        'email' => $this->faker->word,
        'created_at' => $this->faker->date('Y-m-d H:i:s'),
        'updated_at' => $this->faker->date('Y-m-d H:i:s')
        ];
    }
}
