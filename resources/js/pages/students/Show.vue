<script setup lang="ts">
import { Head, Link, router } from '@inertiajs/vue3';
import { computed, ref } from 'vue';
import Heading from '@/components/Heading.vue';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Pencil, Download, Trash2 } from 'lucide-vue-next';
import {
    index as studentsIndex,
    edit as studentsEdit,
    pdf as studentsPdf,
    destroy as studentsDestroy,
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
            { title: 'Student Details', href: '#' },
        ],
    },
});

const currentTeam = computed(
    () => window.location.pathname.split('/')[1] || 'default-team',
);

const deleteDialogOpen = ref(false);

function deleteStudent() {
    router.delete(
        studentsDestroy.url({
            current_team: currentTeam.value,
            student: props.student.id,
        }),
        {
            onSuccess: () => {
                deleteDialogOpen.value = false;
            },
        },
    );
}
</script>

<template>
    <Head title="Student Details" />

    <div class="flex flex-col gap-6">
        <div class="flex items-center justify-between">
            <Heading title="Student Details" />
            <div class="flex items-center gap-2">
                <Link
                    :href="
                        studentsEdit.url({
                            current_team: currentTeam,
                            student: student.id,
                        })
                    "
                >
                    <Button variant="outline" size="sm"
                        ><Pencil class="size-4" /> Edit</Button
                    >
                </Link>
                <a
                    :href="
                        studentsPdf.url({
                            current_team: currentTeam,
                            student: student.id,
                        })
                    "
                    target="_blank"
                >
                    <Button variant="outline" size="sm"
                        ><Download class="size-4" /> Export PDF</Button
                    >
                </a>
                <Button
                    variant="destructive"
                    size="sm"
                    @click="deleteDialogOpen = true"
                    ><Trash2 class="size-4" /> Delete</Button
                >
            </div>
        </div>

        <div class="grid gap-6 lg:grid-cols-2">
            <Card>
                <CardHeader>
                    <CardTitle class="text-sm text-muted-foreground"
                        >FRONT - Public Information</CardTitle
                    >
                </CardHeader>
                <CardContent>
                    <div class="flex flex-col items-center gap-4">
                        <div
                            v-if="student.photo_path"
                            class="h-32 w-32 overflow-hidden rounded-lg"
                        >
                            <img
                                :src="`/storage/${student.photo_path}`"
                                :alt="student.name"
                                class="h-full w-full object-cover"
                            />
                        </div>
                        <div
                            v-else
                            class="flex h-32 w-32 items-center justify-center rounded-lg border-2 border-dashed border-muted-foreground/25 bg-muted/50"
                        >
                            <span class="text-sm text-muted-foreground"
                                >No Photo</span
                            >
                        </div>
                        <div class="text-center">
                            <h3 class="text-lg font-semibold">
                                {{ student.name }}
                            </h3>
                            <p class="text-sm text-muted-foreground">
                                {{ student.course }}
                            </p>
                            <p
                                class="mt-1 inline-block rounded bg-muted px-3 py-1 text-sm font-bold"
                            >
                                {{ student.student_id_number }}
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle class="text-sm text-muted-foreground"
                        >BACK - Emergency Contact</CardTitle
                    >
                </CardHeader>
                <CardContent>
                    <div class="space-y-4">
                        <div>
                            <p
                                class="text-xs font-medium tracking-wider text-muted-foreground uppercase"
                            >
                                Contact Number
                            </p>
                            <p class="mt-1 text-sm font-semibold">
                                {{ student.contact_number }}
                            </p>
                        </div>
                        <div>
                            <p
                                class="text-xs font-medium tracking-wider text-muted-foreground uppercase"
                            >
                                Guardian / Contact Person
                            </p>
                            <p class="mt-1 text-sm font-semibold">
                                {{ student.guardian_contact_person }}
                            </p>
                        </div>
                        <div class="border-t pt-4">
                            <p
                                class="text-xs font-medium tracking-wider text-muted-foreground uppercase"
                            >
                                Student ID
                            </p>
                            <p class="mt-1 font-mono text-sm">
                                {{ student.student_id_number }}
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>

    <Dialog :open="deleteDialogOpen" @update:open="deleteDialogOpen = $event">
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Delete Student</DialogTitle>
                <DialogDescription>
                    Are you sure you want to delete
                    <strong>{{ student.name }}</strong
                    >? This action cannot be undone.
                </DialogDescription>
            </DialogHeader>
            <DialogFooter>
                <Button variant="outline" @click="deleteDialogOpen = false"
                    >Cancel</Button
                >
                <Button variant="destructive" @click="deleteStudent"
                    >Delete</Button
                >
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
