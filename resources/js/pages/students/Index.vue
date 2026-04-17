<script setup lang="ts">
import { Head, Link, router } from '@inertiajs/vue3';
import { computed, ref } from 'vue';
import Heading from '@/components/Heading.vue';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Pencil, Plus, Search, Trash2, Download } from 'lucide-vue-next';
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

const props = defineProps<{
    students: PaginatedStudents;
    filters: { search: string };
}>();

const search = ref(props.filters.search);
const deleteDialogOpen = ref(false);
const studentToDelete = ref<Student | null>(null);

let searchTimeout: ReturnType<typeof setTimeout> | null = null;

function onSearchInput() {
    if (searchTimeout) clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        router.get(
            studentsIndex.url({
                current_team: route().params.current_team as string,
            }),
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
            current_team: route().params.current_team as string,
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

const currentTeam = computed(() => route().params.current_team as string);
</script>

<template>
    <Head title="Students" />

    <div class="flex flex-col gap-6">
        <div class="flex items-center justify-between">
            <Heading title="Students" description="Manage student ID cards" />
            <Link :href="studentsCreate.url({ current_team: currentTeam })">
                <Button>
                    <Plus class="size-4" />
                    Add Student
                </Button>
            </Link>
        </div>

        <div class="relative w-full max-w-sm">
            <Search
                class="absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground"
            />
            <Input
                v-model="search"
                placeholder="Search students..."
                class="pl-9"
                @input="onSearchInput"
            />
        </div>

        <div
            v-if="students.data.length === 0"
            class="py-12 text-center text-muted-foreground"
        >
            <p v-if="filters.search">
                No students found matching "{{ filters.search }}".
            </p>
            <p v-else>No students yet. Click "Add Student" to get started.</p>
        </div>

        <div
            v-else
            class="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
        >
            <Card
                v-for="student in students.data"
                :key="student.id"
                class="overflow-hidden"
            >
                <div
                    class="flex aspect-[3.375/2.125] flex-col items-center justify-center bg-gradient-to-br from-[#1e3a5f] to-[#2d5a87] p-4 text-white"
                >
                    <div
                        class="mb-2 flex h-16 w-16 items-center justify-center overflow-hidden rounded bg-white/20"
                    >
                        <img
                            v-if="student.photo_path"
                            :src="`/storage/${student.photo_path}`"
                            :alt="student.name"
                            class="h-full w-full rounded object-cover"
                        />
                        <span v-else class="text-xs text-white/60"
                            >No Photo</span
                        >
                    </div>
                    <p class="text-center text-sm leading-tight font-bold">
                        {{ student.name }}
                    </p>
                    <p class="text-xs opacity-90">{{ student.course }}</p>
                    <p
                        class="mt-1 rounded bg-white/15 px-2 py-0.5 text-xs font-bold"
                    >
                        {{ student.student_id_number }}
                    </p>
                </div>
                <CardHeader class="pb-2">
                    <CardTitle class="text-sm">{{ student.name }}</CardTitle>
                </CardHeader>
                <CardContent class="pt-0">
                    <p class="text-xs text-muted-foreground">
                        {{ student.course }} &middot; ID:
                        {{ student.student_id_number }}
                    </p>
                </CardContent>
                <div class="flex items-center gap-1 px-4 pb-4">
                    <Link
                        :href="
                            studentsShow.url({
                                current_team: currentTeam,
                                student: student.id,
                            })
                        "
                    >
                        <Button variant="ghost" size="sm">View</Button>
                    </Link>
                    <Link
                        :href="
                            studentsEdit.url({
                                current_team: currentTeam,
                                student: student.id,
                            })
                        "
                    >
                        <Button variant="ghost" size="sm"
                            ><Pencil class="size-3.5"
                        /></Button>
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
                        <Button variant="ghost" size="sm"
                            ><Download class="size-3.5"
                        /></Button>
                    </a>
                    <Button
                        variant="ghost"
                        size="sm"
                        class="text-destructive"
                        @click="confirmDelete(student)"
                        ><Trash2 class="size-3.5"
                    /></Button>
                </div>
            </Card>
        </div>

        <div
            v-if="students.last_page > 1"
            class="flex items-center justify-center gap-2"
        >
            <Link
                v-if="students.prev_page_url"
                :href="students.prev_page_url"
                preserve-state
            >
                <Button variant="outline" size="sm">&laquo; Previous</Button>
            </Link>
            <span class="text-sm text-muted-foreground"
                >Page {{ students.current_page }} of
                {{ students.last_page }}</span
            >
            <Link
                v-if="students.next_page_url"
                :href="students.next_page_url"
                preserve-state
            >
                <Button variant="outline" size="sm">Next &raquo;</Button>
            </Link>
        </div>
    </div>

    <Dialog :open="deleteDialogOpen" @update:open="deleteDialogOpen = $event">
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Delete Student</DialogTitle>
                <DialogDescription>
                    Are you sure you want to delete
                    <strong>{{ studentToDelete?.name }}</strong
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
