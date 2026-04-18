<?php

namespace App\Http\Controllers;

use App\Http\Requests\Students\StoreStudentRequest;
use App\Http\Requests\Students\UpdateStudentRequest;
use App\Models\Student;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Inertia\Inertia;
use Inertia\Response;
use Spatie\LaravelPdf\Enums\Unit;
use Spatie\LaravelPdf\Facades\Pdf;

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
            'templates' => array_merge(\App\Models\Student::availableTemplates(), \App\Models\Template::all()->map(fn($t) => ['value' => 'db_' . $t->id, 'label' => $t->name, 'config' => $t->config])->toArray()),
        ]);
    }

    public function create(string $currentTeam): Response
    {
        return Inertia::render('students/Create', [
            'templates' => array_merge(\App\Models\Student::availableTemplates(), \App\Models\Template::all()->map(fn($t) => ['value' => 'db_' . $t->id, 'label' => $t->name, 'config' => $t->config])->toArray()),
        ]);
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
            'templates' => array_merge(\App\Models\Student::availableTemplates(), \App\Models\Template::all()->map(fn($t) => ['value' => 'db_' . $t->id, 'label' => $t->name, 'config' => $t->config])->toArray()),
        ]);
    }

    public function edit(string $currentTeam, Student $student): Response
    {
        return Inertia::render('students/Edit', [
            'student' => $student,
            'templates' => array_merge(\App\Models\Student::availableTemplates(), \App\Models\Template::all()->map(fn($t) => ['value' => 'db_' . $t->id, 'label' => $t->name, 'config' => $t->config])->toArray()),
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

        $template = $student->template ?? 'classic';

        if (str_starts_with($template, 'db_')) {
            $templateId = str_replace('db_', '', $template);
            $dbTemplate = \App\Models\Template::find($templateId);
            if ($dbTemplate) {
                $view = 'pdf.student-id-custom';
                $viewData = [
                    'student' => $student,
                    'photoBase64' => $photoBase64,
                    'config' => $dbTemplate->config,
                ];
            } else {
                $template = 'classic';
            }
        } elseif ($template === 'custom' && $student->template_config) {
            $view = 'pdf.student-id-custom';
            $viewData = [
                'student' => $student,
                'photoBase64' => $photoBase64,
                'config' => $student->template_config,
            ];
        }
        
        if (!isset($view)) {
            $view = "pdf.student-id-{$template}";

            if (! view()->exists($view)) {
                $view = 'pdf.student-id-classic';
            }

            $viewData = [
                'student' => $student,
                'photoBase64' => $photoBase64,
            ];
        }

        return Pdf::view($view, $viewData)
            ->paperSize(53.98, 85.6, Unit::Millimeter)
            ->inline("student-id-{$student->student_id_number}.pdf");
    }
}
