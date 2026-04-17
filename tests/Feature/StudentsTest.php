<?php

use App\Models\Student;
use App\Models\Team;
use App\Models\User;

use function Pest\Laravel\actingAs;

beforeEach(function () {
    $user = User::factory()->create();
    $team = Team::factory()->create(['is_personal' => false]);
    $team->members()->attach($user, ['role' => 'owner']);
    $user->update(['current_team_id' => $team->id]);
    $user->email_verified_at = now();
    $user->save();

    $this->user = $user;
    $this->team = $team;
});

test('can view students index', function () {
    Student::factory()->count(3)->create();

    $response = actingAs($this->user)
        ->get("/{$this->team->slug}/students");

    $response->assertSuccessful();
    $response->assertInertia(fn ($page) => $page->has('students.data', 3));
});

test('can view create student page', function () {
    $response = actingAs($this->user)
        ->get("/{$this->team->slug}/students/create");

    $response->assertSuccessful();
});

test('can create a student', function () {
    $response = actingAs($this->user)
        ->post("/{$this->team->slug}/students", [
            'name' => 'John Doe',
            'course' => 'BSIT',
            'contact_number' => '09123456789',
            'guardian_contact_person' => 'Jane Doe - 09123456780',
        ]);

    $response->assertRedirect("/{$this->team->slug}/students");

    $this->assertDatabaseHas('students', [
        'name' => 'John Doe',
        'course' => 'BSIT',
        'contact_number' => '09123456789',
        'guardian_contact_person' => 'Jane Doe - 09123456780',
    ]);

    $student = Student::first();
    expect($student->student_id_number)->not->toBeEmpty();
});

test('student id is auto generated', function () {
    config(['students.id_starting_number' => 1000]);

    actingAs($this->user)
        ->post("/{$this->team->slug}/students", [
            'name' => 'First Student',
            'course' => 'BSIT',
            'contact_number' => '09123456789',
            'guardian_contact_person' => 'Guardian',
        ]);

    $first = Student::first();
    expect($first->student_id_number)->toBe('1000');

    actingAs($this->user)
        ->post("/{$this->team->slug}/students", [
            'name' => 'Second Student',
            'course' => 'BSCS',
            'contact_number' => '09123456788',
            'guardian_contact_person' => 'Guardian 2',
        ]);

    $second = Student::orderBy('id', 'desc')->first();
    expect($second->student_id_number)->toBe('1001');
});

test('can view a student', function () {
    $student = Student::factory()->create();

    $response = actingAs($this->user)
        ->get("/{$this->team->slug}/students/{$student->id}");

    $response->assertSuccessful();
});

test('can view edit student page', function () {
    $student = Student::factory()->create();

    $response = actingAs($this->user)
        ->get("/{$this->team->slug}/students/{$student->id}/edit");

    $response->assertSuccessful();
});

test('can update a student', function () {
    $student = Student::factory()->create();

    $response = actingAs($this->user)
        ->put("/{$this->team->slug}/students/{$student->id}", [
            'name' => 'Updated Name',
            'course' => 'BSCS',
            'contact_number' => '09999999999',
            'guardian_contact_person' => 'Updated Guardian',
        ]);

    $response->assertRedirect("/{$this->team->slug}/students");

    $this->assertDatabaseHas('students', [
        'id' => $student->id,
        'name' => 'Updated Name',
    ]);
});

test('can delete a student', function () {
    $student = Student::factory()->create();

    $response = actingAs($this->user)
        ->delete("/{$this->team->slug}/students/{$student->id}");

    $response->assertRedirect("/{$this->team->slug}/students");

    $this->assertDatabaseMissing('students', ['id' => $student->id]);
});

test('can export student pdf', function () {
    $student = Student::factory()->create();

    $response = actingAs($this->user)
        ->get("/{$this->team->slug}/students/{$student->id}/pdf");

    $response->assertSuccessful();
    $response->assertHeader('content-type', 'application/pdf');
});

test('store validates required fields', function () {
    $response = actingAs($this->user)
        ->post("/{$this->team->slug}/students", []);

    $response->assertSessionHasErrors(['name', 'course', 'contact_number', 'guardian_contact_person']);
});

test('search filters students', function () {
    Student::factory()->create(['name' => 'Alice']);
    Student::factory()->create(['name' => 'Bob']);

    $response = actingAs($this->user)
        ->get("/{$this->team->slug}/students?search=Alice");

    $response->assertSuccessful();
    $response->assertInertia(fn ($page) => $page->has('students.data', 1));
});
