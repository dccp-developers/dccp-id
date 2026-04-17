<script setup lang="ts">
import { Form, Head } from '@inertiajs/vue3';
import Heading from '@/components/Heading.vue';
import InputError from '@/components/InputError.vue';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ref } from 'vue';
import { store as studentsStore } from '@/routes/students';

defineOptions({
    layout: {
        breadcrumbs: [
            { title: 'Students', href: '#' },
            { title: 'Add Student', href: '#' },
        ],
    },
});

const currentTeam = window.location.pathname.split('/')[1] || 'default-team';

const photoPreview = ref<string | null>(null);

function onPhotoChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            photoPreview.value = e.target?.result as string;
        };
        reader.readAsDataURL(file);
    }
}
</script>

<template>
    <Head title="Add Student" />

    <div class="flex flex-col gap-6">
        <Heading
            title="Add Student"
            description="Create a new student ID card"
        />

        <Form
            :action="studentsStore.url({ current_team: currentTeam })"
            method="post"
            class="space-y-6"
            v-slot="{ errors, processing }"
        >
            <Card>
                <CardContent class="pt-6">
                    <div class="grid gap-6">
                        <div class="grid gap-2">
                            <Label for="photo">Photo</Label>
                            <div class="flex items-center gap-4">
                                <div
                                    class="flex h-24 w-24 items-center justify-center overflow-hidden rounded-lg border-2 border-dashed border-muted-foreground/25 bg-muted/50"
                                >
                                    <img
                                        v-if="photoPreview"
                                        :src="photoPreview"
                                        alt="Preview"
                                        class="h-full w-full object-cover"
                                    />
                                    <span
                                        v-else
                                        class="text-xs text-muted-foreground"
                                        >No photo</span
                                    >
                                </div>
                                <Input
                                    id="photo"
                                    type="file"
                                    accept="image/*"
                                    name="photo"
                                    class="cursor-pointer"
                                    @change="onPhotoChange"
                                />
                            </div>
                            <InputError :message="errors.photo" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="name">Full Name</Label>
                            <Input
                                id="name"
                                name="name"
                                type="text"
                                required
                                placeholder="Enter student's full name"
                            />
                            <InputError :message="errors.name" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="course">Course</Label>
                            <Input
                                id="course"
                                name="course"
                                type="text"
                                required
                                placeholder="e.g. BSIT, BSCS, BSN"
                            />
                            <InputError :message="errors.course" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="contact_number">Contact Number</Label>
                            <Input
                                id="contact_number"
                                name="contact_number"
                                type="text"
                                required
                                placeholder="Student's contact number"
                            />
                            <InputError :message="errors.contact_number" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="guardian_contact_person"
                                >Guardian / Contact Person</Label
                            >
                            <Input
                                id="guardian_contact_person"
                                name="guardian_contact_person"
                                type="text"
                                required
                                placeholder="Guardian's name and contact number"
                            />
                            <InputError
                                :message="errors.guardian_contact_person"
                            />
                        </div>
                    </div>
                </CardContent>
            </Card>

            <div class="flex items-center gap-4">
                <Button :disabled="processing" type="submit"
                    >Create Student</Button
                >
            </div>
        </Form>
    </div>
</template>
