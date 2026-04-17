<script setup lang="ts">
import { Head, Link, router, usePage } from '@inertiajs/vue3';
import { computed, ref } from 'vue';
import Heading from '@/components/Heading.vue';
import IdCardPreview from '@/components/IdCardPreview.vue';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Separator } from '@/components/ui/separator';
import {
    Pencil,
    Plus,
    Search,
    Trash2,
    Download,
    Eye,
    Users,
    IdCard,
    GraduationCap,
} from 'lucide-vue-next';
import {
    index as studentsIndex,
    create as studentsCreate,
    show as studentsShow,
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
    template: string;
    template_config: any;
};

type PaginatedStudents = {
    data: Student[];
    current_page: number;
    last_page: number;
    per_page: number;
    total: number;
    prev_page_url: string | null;
    next_page_url: string | null;
};

type Template = { value: string; label: string };

const props = defineProps<{
    students: PaginatedStudents;
    filters: { search: string };
    templates: Template[];
}>();

const page = usePage();
const currentTeam = computed(() => (page.props.currentTeam as any)?.slug ?? '');

const search = ref(props.filters.search);
const deleteDialogOpen = ref(false);
const studentToDelete = ref<Student | null>(null);

const templateLabels: Record<string, string> = {
    classic: 'Classic Blue',
    modern: 'Modern Dark',
    minimal: 'Minimal White',
    gradient: 'Gradient Purple',
    professional: 'Professional Green',
    custom: 'Custom',
};

const uniqueCourses = computed(() => {
    const courses = new Set(props.students.data.map((s) => s.course));
    return courses.size;
});

let searchTimeout: ReturnType<typeof setTimeout> | null = null;

function onSearchInput() {
    if (searchTimeout) clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        router.get(
            studentsIndex.url({ current_team: currentTeam.value }),
            { search: search.value },
            { preserveState: true, replace: true },
        );
    }, 300);
}

function confirmDelete(student: Student) {
    studentToDelete.value = student;
    deleteDialogOpen.value = true;
}

function deleteStudent() {
    if (!studentToDelete.value) return;
    router.delete(
        studentsDestroy.url({
            current_team: currentTeam.value,
            student: studentToDelete.value.id,
        }),
        {
            onSuccess: () => {
                deleteDialogOpen.value = false;
                studentToDelete.value = null;
            },
        },
    );
}

function getPreviewData(student: Student) {
    return {
        name: student.name,
        course: student.course,
        studentIdNumber: student.student_id_number,
        contactNumber: student.contact_number,
        guardianContactPerson: student.guardian_contact_person,
        photoUrl: student.photo_path ? `/storage/${student.photo_path}` : null,
        schoolName: 'DCCP',
    };
}
</script>

<template>
    <Head title="Students" />

    <div class="space-y-6">
        <div
            class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
        >
            <div>
                <h1 class="text-2xl font-bold tracking-tight">Students</h1>
                <p class="text-sm text-muted-foreground">
                    Manage student ID cards and templates
                </p>
            </div>
            <Link :href="studentsCreate.url({ current_team: currentTeam })">
                <Button><Plus class="mr-2 size-4" />Add Student</Button></Link
            >
        </div>

        <div class="grid gap-4 sm:grid-cols-3">
            <Card class="border-l-4 border-l-blue-500">
                <CardContent class="flex items-center gap-4 p-4">
                    <div
                        class="flex size-10 shrink-0 items-center justify-center rounded-full bg-blue-100 text-blue-700"
                    >
                        <Users class="size-5" />
                    </div>
                    <div>
                        <p class="text-2xl font-bold">{{ students.total }}</p>
                        <p class="text-xs text-muted-foreground">
                            Total Students
                        </p>
                    </div>
                </CardContent>
            </Card>
            <Card class="border-l-4 border-l-emerald-500">
                <CardContent class="flex items-center gap-4 p-4">
                    <div
                        class="flex size-10 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-700"
                    >
                        <GraduationCap class="size-5" />
                    </div>
                    <div>
                        <p class="text-2xl font-bold">{{ uniqueCourses }}</p>
                        <p class="text-xs text-muted-foreground">Courses</p>
                    </div>
                </CardContent>
            </Card>
            <Card class="border-l-4 border-l-violet-500">
                <CardContent class="flex items-center gap-4 p-4">
                    <div
                        class="flex size-10 shrink-0 items-center justify-center rounded-full bg-violet-100 text-violet-700"
                    >
                        <IdCard class="size-5" />
                    </div>
                    <div>
                        <p class="text-2xl font-bold">
                            {{ students.data.length }}
                        </p>
                        <p class="text-xs text-muted-foreground">This Page</p>
                    </div>
                </CardContent>
            </Card>
        </div>

        <div class="flex items-center gap-3">
            <div class="relative max-w-sm flex-1">
                <Search
                    class="absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground"
                />
                <Input
                    v-model="search"
                    placeholder="Search by name, ID, or course..."
                    class="pl-9"
                    @input="onSearchInput"
                />
            </div>
        </div>

        <div
            v-if="students.data.length === 0"
            class="flex flex-col items-center gap-4 rounded-lg border border-dashed py-16"
        >
            <div
                class="flex size-16 items-center justify-center rounded-full bg-muted"
            >
                <Users class="size-8 text-muted-foreground" />
            </div>
            <div class="text-center">
                <p class="font-medium" v-if="filters.search">
                    No students found matching "{{ filters.search }}"
                </p>
                <p class="font-medium" v-else>No students yet</p>
                <p class="text-sm text-muted-foreground" v-if="!filters.search">
                    Click "Add Student" to create your first ID card.
                </p>
            </div>
        </div>

        <div v-else class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
            <Card
                v-for="student in students.data"
                :key="student.id"
                class="group overflow-hidden transition-shadow hover:shadow-md"
            >
                <div
                    class="cursor-pointer bg-muted/30 p-4"
                    @click="
                        router.visit(
                            studentsShow.url({
                                current_team: currentTeam,
                                student: student.id,
                            }),
                        )
                    "
                >
                    <div class="flex justify-center">
                        <IdCardPreview
                            :template="student.template || 'classic'"
                            side="front"
                            :data="getPreviewData(student)"
                            :config="student.template_config"
                            :scale="0.82"
                        />
                    </div>
                </div>
                <CardContent class="p-4">
                    <div class="flex items-start justify-between gap-3">
                        <div class="min-w-0 flex-1">
                            <h3 class="truncate leading-tight font-semibold">
                                {{ student.name }}
                            </h3>
                            <p class="text-sm text-muted-foreground">
                                {{ student.course }}
                            </p>
                            <div class="mt-1.5 flex items-center gap-2">
                                <Badge
                                    variant="secondary"
                                    class="font-mono text-[10px]"
                                    >{{ student.student_id_number }}</Badge
                                >
                            </div>
                        </div>
                        <div class="flex shrink-0 items-center gap-1">
                            <a
                                :href="
                                    studentsPdf.url({
                                        current_team: currentTeam,
                                        student: student.id,
                                    })
                                "
                                target="_blank"
                            >
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-8"
                                    title="Download PDF"
                                >
                                    <Download class="size-3.5" />
                                </Button>
                            </a>
                            <Link
                                :href="
                                    studentsEdit.url({
                                        current_team: currentTeam,
                                        student: student.id,
                                    })
                                "
                            >
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-8"
                                    title="Edit"
                                >
                                    <Pencil class="size-3.5" />
                                </Button>
                            </Link>
                            <Button
                                variant="ghost"
                                size="icon"
                                class="size-8 text-destructive"
                                title="Delete"
                                @click="confirmDelete(student)"
                            >
                                <Trash2 class="size-3.5" />
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>

        <div
            v-if="students.last_page > 1"
            class="flex items-center justify-between"
        >
            <p class="text-sm text-muted-foreground">
                Showing page {{ students.current_page }} of
                {{ students.last_page }} &middot; {{ students.total }} total
            </p>
            <div class="flex items-center gap-2">
                <Link
                    v-if="students.prev_page_url"
                    :href="students.prev_page_url"
                    preserve-state
                >
                    <Button variant="outline" size="sm">Previous</Button>
                </Link>
                <Link
                    v-if="students.next_page_url"
                    :href="students.next_page_url"
                    preserve-state
                >
                    <Button variant="outline" size="sm">Next</Button>
                </Link>
            </div>
        </div>
    </div>

    <Dialog :open="deleteDialogOpen" @update:open="deleteDialogOpen = $event">
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Delete Student</DialogTitle>
                <DialogDescription>
                    Are you sure you want to delete
                    <strong>{{ studentToDelete?.name }}</strong
                    >? This action cannot be undone and will remove their ID
                    card record.
                </DialogDescription>
            </DialogHeader>
            <DialogFooter class="gap-2">
                <Button variant="outline" @click="deleteDialogOpen = false"
                    >Cancel</Button
                >
                <Button variant="destructive" @click="deleteStudent"
                    >Delete Student</Button
                >
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>
