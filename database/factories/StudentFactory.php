<?php

namespace Database\Factories;

use App\Models\Student;
use Illuminate\Database\Eloquent\Factories\Factory;

/** @extends Factory<Student> */
class StudentFactory extends Factory
{
    protected $model = Student::class;

    public function definition(): array
    {
        return [
            'student_id_number' => (string) ($this->faker->unique()->numberBetween(1000, 9999)),
            'name' => $this->faker->name(),
            'course' => $this->faker->randomElement(['BSIT', 'BSCS', 'BSIS', 'BSCPE', 'BSECE', 'BSME', 'BSEE', 'BSCE', 'BSA', 'BSBA']),
            'contact_number' => $this->faker->phoneNumber(),
            'guardian_contact_person' => $this->faker->name(),
            'photo_path' => null,
            'template' => $this->faker->randomElement(['classic', 'modern', 'minimal', 'gradient', 'professional']),
        ];
    }
}
