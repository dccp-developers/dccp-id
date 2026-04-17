<?php

namespace App\Http\Controllers;

use App\Http\Requests\Students\StoreStudentRequest;
use App\Http\Requests\Students\UpdateStudentRequest;
use App\Models\Student;
use Barryvdh\DomPDF\Facade\Pdf;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Inertia\Inertia;
use Inertia\Response;

class StudentController extends Controller
{
    public function index(Request $request, string $currentTeam): Response
    {
        $search = $request->query('search', '');

        $students = Student::query()
            ->when($search, fn ($q) => $q->where('name', 'like', "%{$search}%")->orWhere('student_id_number', 'like', "%{$search}%")->orWhere('course', 'like', "%{$search}%"))
            ->orderBy('id', 'desc')
            ->paginate(12)
            ->withQueryString();

        return Inertia::render('students/Index', [
            'students' => $students,
            'filters' => ['search' => $search],
        ]);
    }

    public function create(string $currentTeam): Response
    {
        return Inertia::render('students/Create');
    }

    public function store(StoreStudentRequest $request, string $currentTeam): RedirectResponse
    {
        $validated = $request->validated();

        if ($request->hasFile('photo')) {
            $validated['photo_path'] = $request->file('photo')->store('photos', 'public');
        }

        unset($validated['photo']);

        Student::create($validated);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Student created successfully.']);

        return to_route('students.index', ['current_team' => $currentTeam]);
    }

    public function show(string $currentTeam, Student $student): Response
    {
        return Inertia::render('students/Show', [
            'student' => $student,
        ]);
    }

    public function edit(string $currentTeam, Student $student): Response
    {
        return Inertia::render('students/Edit', [
            'student' => $student,
        ]);
    }

    public function update(UpdateStudentRequest $request, string $currentTeam, Student $student): RedirectResponse
    {
        $validated = $request->validated();

        if ($request->hasFile('photo')) {
            if ($student->photo_path) {
                Storage::disk('public')->delete($student->photo_path);
            }
            $validated['photo_path'] = $request->file('photo')->store('photos', 'public');
        }

        unset($validated['photo']);

        $student->update($validated);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Student updated successfully.']);

        return to_route('students.index', ['current_team' => $currentTeam]);
    }

    public function destroy(string $currentTeam, Student $student): RedirectResponse
    {
        if ($student->photo_path) {
            Storage::disk('public')->delete($student->photo_path);
        }

        $student->delete();

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Student deleted successfully.']);

        return to_route('students.index', ['current_team' => $currentTeam]);
    }

    public function exportPdf(string $currentTeam, Student $student)
    {
        $photoBase64 = null;
        if ($student->photo_path && Storage::disk('public')->exists($student->photo_path)) {
            $photoBase64 = base64_encode(Storage::disk('public')->get($student->photo_path));
            $mimeType = Storage::disk('public')->mimeType($student->photo_path);
            $photoBase64 = "data:{$mimeType};base64,{$photoBase64}";
        }

        $pdf = Pdf::loadView('pdf.student-id', [
            'student' => $student,
            'photoBase64' => $photoBase64,
        ]);

        $pdf->setPaper([0, 0, 612, 792]);

        return $pdf->stream("student-id-{$student->student_id_number}.pdf");
    }
}
