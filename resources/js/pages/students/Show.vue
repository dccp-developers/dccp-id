<script setup lang="ts">
import { Head, Link, router, usePage } from '@inertiajs/vue3';
import { computed, ref } from 'vue';
import IdCardPreview from '@/components/IdCardPreview.vue';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
    Pencil,
    Download,
    Trash2,
    ArrowLeft,
    Phone,
    Users,
    Hash,
    GraduationCap,
    CreditCard,
} from 'lucide-vue-next';
import {
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

const props = defineProps<{
    student: Student;
    templates: { value: string; label: string }[];
}>();

defineOptions({
    layout: {
        breadcrumbs: [
            { title: 'Students', href: '#' },
            { title: 'Student Details', href: '#' },
        ],
    },
});

const page = usePage();
const currentTeam = computed(() => (page.props.currentTeam as any)?.slug ?? '');

const deleteDialogOpen = ref(false);

const templateLabels: Record<string, string> = {
    classic: 'Classic Blue',
    modern: 'Modern Dark',
    minimal: 'Minimal White',
    gradient: 'Gradient Purple',
    professional: 'Professional Green',
    custom: 'Custom',
};

const previewData = computed(() => ({
    name: props.student.name,
    course: props.student.course,
    studentIdNumber: props.student.student_id_number,
    contactNumber: props.student.contact_number,
    guardianContactPerson: props.student.guardian_contact_person,
    photoUrl: props.student.photo_path
        ? `/storage/${props.student.photo_path}`
        : null,
    schoolName: 'DCCP',
}));

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

    <div class="space-y-6">
        <div
            class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
        >
            <div>
                <h1 class="text-2xl font-bold tracking-tight">
                    {{ student.name }}
                </h1>
                <p class="text-sm text-muted-foreground">
                    {{ student.course }} &middot;
                    {{ student.student_id_number }}
                </p>
            </div>
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
                        ><Pencil class="mr-1.5 size-3.5" />Edit</Button
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
                        ><Download class="mr-1.5 size-3.5" />PDF</Button
                    >
                </a>
                <Button
                    variant="outline"
                    size="sm"
                    class="text-destructive hover:bg-destructive/10"
                    @click="deleteDialogOpen = true"
                >
                    <Trash2 class="mr-1.5 size-3.5" />Delete
                </Button>
            </div>
        </div>

        <div class="grid gap-6 lg:grid-cols-[1fr_400px]">
            <div class="space-y-6">
                <Card>
                    <CardHeader class="pb-4">
                        <CardTitle class="text-base"
                            >Personal Information</CardTitle
                        >
                    </CardHeader>
                    <CardContent>
                        <div class="flex items-center gap-5">
                            <div
                                class="flex size-20 shrink-0 items-center justify-center overflow-hidden rounded-xl border-2 border-muted-foreground/10 bg-muted"
                            >
                                <img
                                    v-if="student.photo_path"
                                    :src="`/storage/${student.photo_path}`"
                                    :alt="student.name"
                                    class="size-full object-cover"
                                />
                                <span
                                    v-else
                                    class="text-2xl font-bold text-muted-foreground/40"
                                    >{{
                                        student.name
                                            .split(' ')
                                            .map((w) => w[0])
                                            .join('')
                                            .substring(0, 2)
                                    }}</span
                                >
                            </div>
                            <div class="min-w-0">
                                <h2 class="truncate text-xl font-semibold">
                                    {{ student.name }}
                                </h2>
                                <div class="mt-1 flex items-center gap-2">
                                    <Badge
                                        variant="secondary"
                                        class="font-mono"
                                        >{{ student.student_id_number }}</Badge
                                    >
                                    <Badge variant="outline">{{
                                        templateLabels[student.template] ||
                                        student.template
                                    }}</Badge>
                                </div>
                            </div>
                        </div>

                        <Separator class="my-4" />

                        <div class="grid gap-4 sm:grid-cols-2">
                            <div
                                class="flex items-start gap-3 rounded-lg bg-muted/40 p-3"
                            >
                                <GraduationCap
                                    class="mt-0.5 size-4 shrink-0 text-muted-foreground"
                                />
                                <div>
                                    <p
                                        class="text-xs font-medium text-muted-foreground"
                                    >
                                        Course
                                    </p>
                                    <p class="text-sm font-semibold">
                                        {{ student.course }}
                                    </p>
                                </div>
                            </div>
                            <div
                                class="flex items-start gap-3 rounded-lg bg-muted/40 p-3"
                            >
                                <Phone
                                    class="mt-0.5 size-4 shrink-0 text-muted-foreground"
                                />
                                <div>
                                    <p
                                        class="text-xs font-medium text-muted-foreground"
                                    >
                                        Contact Number
                                    </p>
                                    <p class="text-sm font-semibold">
                                        {{ student.contact_number }}
                                    </p>
                                </div>
                            </div>
                            <div
                                class="flex items-start gap-3 rounded-lg bg-muted/40 p-3"
                            >
                                <Users
                                    class="mt-0.5 size-4 shrink-0 text-muted-foreground"
                                />
                                <div>
                                    <p
                                        class="text-xs font-medium text-muted-foreground"
                                    >
                                        Guardian
                                    </p>
                                    <p class="text-sm font-semibold">
                                        {{ student.guardian_contact_person }}
                                    </p>
                                </div>
                            </div>
                            <div
                                class="flex items-start gap-3 rounded-lg bg-muted/40 p-3"
                            >
                                <CreditCard
                                    class="mt-0.5 size-4 shrink-0 text-muted-foreground"
                                />
                                <div>
                                    <p
                                        class="text-xs font-medium text-muted-foreground"
                                    >
                                        Student ID
                                    </p>
                                    <p class="font-mono text-sm font-semibold">
                                        {{ student.student_id_number }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div class="self-start lg:sticky lg:top-6">
                <Card>
                    <CardHeader class="pb-3">
                        <CardTitle class="text-base">ID Card Preview</CardTitle>
                        <CardDescription
                            >{{
                                templateLabels[student.template] ||
                                'Classic Blue'
                            }}
                            template</CardDescription
                        >
                    </CardHeader>
                    <CardContent>
                        <Tabs default-value="both">
                            <TabsList class="w-full">
                                <TabsTrigger value="front" class="flex-1"
                                    >Front</TabsTrigger
                                >
                                <TabsTrigger value="back" class="flex-1"
                                    >Back</TabsTrigger
                                >
                                <TabsTrigger value="both" class="flex-1"
                                    >Both</TabsTrigger
                                >
                            </TabsList>
                            <TabsContent
                                value="front"
                                class="mt-4 flex justify-center"
                            >
                                <IdCardPreview
                                    :template="student.template || 'classic'"
                                    side="front"
                                    :data="previewData"
                                    :config="student.template_config"
                                />
                            </TabsContent>
                            <TabsContent
                                value="back"
                                class="mt-4 flex justify-center"
                            >
                                <IdCardPreview
                                    :template="student.template || 'classic'"
                                    side="back"
                                    :data="previewData"
                                    :config="student.template_config"
                                />
                            </TabsContent>
                            <TabsContent
                                value="both"
                                class="mt-4 flex justify-center"
                            >
                                <IdCardPreview
                                    :template="student.template || 'classic'"
                                    side="both"
                                    :data="previewData"
                                    :config="student.template_config"
                                />
                            </TabsContent>
                        </Tabs>
                    </CardContent>
                </Card>
            </div>
        </div>
    </div>

    <Dialog :open="deleteDialogOpen" @update:open="deleteDialogOpen = $event">
        <DialogContent>
            <DialogHeader>
                <DialogTitle>Delete Student</DialogTitle>
                <DialogDescription>
                    Are you sure you want to delete
                    <strong>{{ student.name }}</strong
                    >? This action cannot be undone and will permanently remove
                    their ID card record.
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
