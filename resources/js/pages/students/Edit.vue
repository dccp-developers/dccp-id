<script setup lang="ts">
import { Form, Head, Link } from '@inertiajs/vue3';
import Heading from '@/components/Heading.vue';
import InputError from '@/components/InputError.vue';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { computed, ref } from 'vue';
import {
    index as studentsIndex,
    update as studentsUpdate,
} from '@/routes/students';

type Student = {
    id: number;
    student_id_number: string;
    name: string;
    course: string;
    contact_number: string;
    guardian_contact_person: string;
    photo_path: string | null;
};

const props = defineProps<{
    student: Student;
}>();

defineOptions({
    layout: {
        breadcrumbs: [
            { title: 'Students', href: '#' },
            { title: 'Edit Student', href: '#' },
        ],
    },
});

const currentTeam = computed(
    () => window.location.pathname.split('/')[1] || 'default-team',
);

const photoPreview = ref<string | null>(
    props.student.photo_path ? `/storage/${props.student.photo_path}` : null,
);

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
    <Head title="Edit Student" />

    <div class="flex flex-col gap-6">
        <Heading
            title="Edit Student"
            description="Update student information"
        />

        <Form
            :action="
                studentsUpdate.url({
                    current_team: currentTeam,
                    student: student.id,
                })
            "
            method="put"
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
                                :default-value="student.name"
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
                                :default-value="student.course"
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
                                :default-value="student.contact_number"
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
                                :default-value="student.guardian_contact_person"
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
                    >Update Student</Button
                >
                <Link :href="studentsIndex.url({ current_team: currentTeam })">
                    <Button variant="outline" type="button">Cancel</Button>
                </Link>
            </div>
        </Form>
    </div>
</template>
