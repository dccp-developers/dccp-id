<?php

namespace App\Http\Requests\Students;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class UpdateStudentRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    /**
     * @return array<string, ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'course' => ['required', 'string', 'max:255'],
            'contact_number' => ['required', 'string', 'max:255'],
            'guardian_contact_person' => ['required', 'string', 'max:255'],
            'photo' => ['nullable', 'image', 'max:2048'],
            'signature' => ['nullable', 'string'],
            'template' => ['nullable', 'string'],
            'template_config' => ['nullable', 'array'],
            'template_config.front' => ['nullable', 'array'],
            'template_config.back' => ['nullable', 'array'],
        ];
    }
}
