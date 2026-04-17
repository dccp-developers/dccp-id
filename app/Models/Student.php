<?php

namespace App\Models;

use Database\Factories\StudentFactory;
use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Storage;

#[Fillable(['student_id_number', 'name', 'course', 'contact_number', 'guardian_contact_person', 'photo_path'])]
class Student extends Model
{
    /** @use HasFactory<StudentFactory> */
    use HasFactory;

    protected static function boot(): void
    {
        parent::boot();

        static::creating(function (Student $student) {
            if (empty($student->student_id_number)) {
                $student->student_id_number = static::generateStudentIdNumber();
            }
        });
    }

    public static function generateStudentIdNumber(): string
    {
        $lastStudent = static::query()->orderBy('id', 'desc')->first();

        if ($lastStudent) {
            $lastNumber = (int) $lastStudent->student_id_number;

            return (string) ($lastNumber + 1);
        }

        return (string) ((int) config('students.id_starting_number', 1000));
    }

    public function photoUrl(): string
    {
        return $this->photo_path
            ? Storage::disk('public')->url($this->photo_path)
            : '';
    }

    protected function casts(): array
    {
        return [];
    }
}
