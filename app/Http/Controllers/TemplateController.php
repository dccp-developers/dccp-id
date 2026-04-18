<?php

namespace App\Http\Controllers;

use App\Models\Template;
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Inertia\Inertia;
use Inertia\Response;

class TemplateController extends Controller
{
    public function index(Request $request, string $currentTeam): Response
    {
        $templates = Template::orderBy('id', 'desc')->get();

        return Inertia::render('templates/Index', [
            'templates' => $templates,
        ]);
    }

    public function create(string $currentTeam): Response
    {
        return Inertia::render('templates/Create');
    }

    public function store(Request $request, string $currentTeam): RedirectResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'config' => 'required|array',
        ]);

        Template::create($validated);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Template created successfully.']);

        return to_route('templates.index', ['current_team' => $currentTeam]);
    }

    public function edit(string $currentTeam, Template $template): Response
    {
        return Inertia::render('templates/Edit', [
            'template' => $template,
        ]);
    }

    public function update(Request $request, string $currentTeam, Template $template): RedirectResponse
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'config' => 'required|array',
        ]);

        $template->update($validated);

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Template updated successfully.']);

        return to_route('templates.index', ['current_team' => $currentTeam]);
    }

    public function destroy(string $currentTeam, Template $template): RedirectResponse
    {
        $template->delete();

        Inertia::flash('toast', ['type' => 'success', 'message' => 'Template deleted successfully.']);

        return to_route('templates.index', ['current_team' => $currentTeam]);
    }
}
