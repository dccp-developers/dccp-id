<script setup lang="ts">
import { Form, Head, Link, usePage } from '@inertiajs/vue3';
import Heading from '@/components/Heading.vue';
import InputError from '@/components/InputError.vue';
import IdCardPreview from '@/components/IdCardPreview.vue';
import SignaturePad from '@/components/SignaturePad.vue';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { computed, ref } from 'vue';
import { User, Upload, Palette, UserCircle, ArrowLeft } from 'lucide-vue-next';
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
    template: string;
    template_config: any;
};

type Template = { value: string; label: string };
type TemplateConfig = {
    front: {
        background: {
            type: string;
            solidColor: string;
            gradientStart: string;
            gradientEnd: string;
            gradientAngle: string;
            imageBase64: string | null;
        };
        elements: any[];
    };
    back: {
        background: {
            type: string;
            solidColor: string;
            gradientStart: string;
            gradientEnd: string;
            gradientAngle: string;
            imageBase64: string | null;
        };
        elements: any[];
    };
};

const props = defineProps<{
    student: Student;
    templates: Template[];
}>();

defineOptions({
    layout: {
        breadcrumbs: [
            { title: 'Students', href: '#' },
            { title: 'Edit Student', href: '#' },
        ],
    },
});

const page = usePage();
const currentTeam = computed(() => (page.props.currentTeam as any)?.slug ?? '');

const photoPreview = ref<string | null>(
    props.student.photo_path ? `/storage/${props.student.photo_path}` : null,
);
const selectedTemplate = ref(props.student.template || 'classic');
const templateConfig = ref<TemplateConfig | null>(
    props.student.template_config || null,
);
const formName = ref(props.student.name);
const formCourse = ref(props.student.course);
const formContactNumber = ref(props.student.contact_number);
const formGuardian = ref(props.student.guardian_contact_person);
const formSignature = ref<string | null>(
    props.student.signature_path ? `/storage/${props.student.signature_path}` : null,
);

const previewData = computed(() => ({
    name: formName.value || 'Student Name',
    course: formCourse.value || 'Course',
    studentIdNumber: props.student.student_id_number,
    contactNumber: formContactNumber.value || '—',
    guardianContactPerson: formGuardian.value || '—',
    photoUrl: photoPreview.value,
    schoolName: 'DCCP',
}));

const templateLabel = computed(() => {
    const t = props.templates.find((t) => t.value === selectedTemplate.value);
    return t?.label ?? 'Classic Blue';
});

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

const editorStudentData = computed(() => ({
    name: formName.value || 'Student Name',
    course: formCourse.value || 'Course',
    studentIdNumber: props.student.student_id_number,
    contactNumber: formContactNumber.value || '—',
    guardianContactPerson: formGuardian.value || '—',
}));
</script>

<template>
    <Head title="Edit Student" />

    <div class="flex h-full flex-1 flex-col gap-4 overflow-x-auto rounded-xl p-4">
        <div class="flex items-center justify-between">
            <div>
                <h1 class="text-2xl font-bold tracking-tight">Edit Student</h1>
                <p class="text-sm text-muted-foreground">
                    Update information for {{ student.name }}
                </p>
            </div>
            <Link :href="studentsIndex.url({ current_team: currentTeam })">
                <Button variant="outline"
                    ><ArrowLeft class="mr-2 size-4" />Back to Students</Button
                >
            </Link>
        </div>

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
            <div class="grid gap-6 lg:grid-cols-[1fr_380px]">
                <div class="space-y-6">
                    <Card>
                        <CardHeader class="pb-4">
                            <div class="flex items-center gap-2">
                                <User class="size-4 text-muted-foreground" />
                                <CardTitle class="text-base"
                                    >Student Information</CardTitle
                                >
                            </div>
                            <CardDescription
                                >Update the student's personal
                                details</CardDescription
                            >
                        </CardHeader>
                        <CardContent class="space-y-5">
                            <div class="flex items-start gap-6">
                                <div class="shrink-0">
                                    <Label class="mb-2 block text-sm"
                                        >Photo</Label
                                    >
                                    <label
                                        class="group flex size-28 cursor-pointer flex-col items-center justify-center gap-1.5 rounded-xl border-2 border-dashed border-muted-foreground/25 bg-muted/30 transition-colors hover:border-primary/50 hover:bg-muted/50"
                                    >
                                        <img
                                            v-if="photoPreview"
                                            :src="photoPreview"
                                            alt="Preview"
                                            class="size-full rounded-[10px] object-cover"
                                        />
                                        <template v-else>
                                            <Upload
                                                class="size-5 text-muted-foreground/50 group-hover:text-primary/70"
                                            />
                                            <span
                                                class="text-[10px] text-muted-foreground/60"
                                                >Upload</span
                                            >
                                        </template>
                                        <input
                                            type="file"
                                            accept="image/*"
                                            name="photo"
                                            class="hidden"
                                            @change="onPhotoChange"
                                        />
                                    </label>
                                    <InputError :message="errors.photo" />
                                </div>
                                <div class="flex-1 space-y-4 pt-7">
                                    <div class="space-y-1.5">
                                        <Label for="name">Full Name</Label>
                                        <Input
                                            id="name"
                                            name="name"
                                            type="text"
                                            required
                                            v-model="formName"
                                        />
                                        <InputError :message="errors.name" />
                                    </div>
                                    <div class="space-y-1.5">
                                        <Label for="course">Course</Label>
                                        <Input
                                            id="course"
                                            name="course"
                                            type="text"
                                            required
                                            v-model="formCourse"
                                        />
                                        <InputError :message="errors.course" />
                                    </div>
                                </div>
                            </div>
                            <Separator />
                            <div class="grid gap-4 sm:grid-cols-2">
                                <div class="space-y-1.5">
                                    <Label for="contact_number"
                                        >Contact Number</Label
                                    >
                                    <Input
                                        id="contact_number"
                                        name="contact_number"
                                        type="text"
                                        required
                                        v-model="formContactNumber"
                                    />
                                    <InputError
                                        :message="errors.contact_number"
                                    />
                                </div>
                                <div class="space-y-1.5">
                                    <Label for="guardian_contact_person"
                                        >Guardian / Contact Person</Label
                                    >
                                    <Input
                                        id="guardian_contact_person"
                                        name="guardian_contact_person"
                                        type="text"
                                        required
                                        v-model="formGuardian"
                                    />
                                    <InputError
                                        :message="
                                            errors.guardian_contact_person
                                        "
                                    />
                                </div>
                            </div>
                            
                            <Separator class="my-4" />
                            
                            <div class="space-y-3">
                                <div class="flex items-center justify-between">
                                    <Label>Signature</Label>
                                    <span class="text-xs text-muted-foreground">Optional, will appear on ID</span>
                                </div>
                                <SignaturePad v-model="formSignature" />
                                <input type="hidden" name="signature" :value="formSignature || ''" />
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader class="pb-4">
                            <div class="flex items-center gap-2">
                                <Palette class="size-4 text-muted-foreground" />
                                <CardTitle class="text-base"
                                    >Card Template</CardTitle
                                >
                            </div>
                            <CardDescription
                                >Choose a preset design or customize your
                                own</CardDescription
                            >
                        </CardHeader>
                        <CardContent>
                            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3">
                                <button
                                    v-for="tmpl in templates.filter(
                                        (t) => t.value !== 'custom',
                                    )"
                                    :key="tmpl.value"
                                    type="button"
                                    :class="[
                                        'flex flex-col items-center gap-2 rounded-lg border-2 p-3 transition-all',
                                        selectedTemplate === tmpl.value
                                            ? 'border-primary bg-primary/5 shadow-sm'
                                            : 'border-transparent bg-muted/40 hover:border-muted-foreground/20 hover:bg-muted/60',
                                    ]"
                                    @click="
                                        selectedTemplate = tmpl.value;
                                    "
                                >
                                    <IdCardPreview
                                        :template="tmpl.value.startsWith('db_') ? 'custom' : tmpl.value"
                                        :config="tmpl.config"
                                        side="front"
                                        :data="{
                                            name: formName || 'Student',
                                            course: formCourse || 'Course',
                                            studentIdNumber:
                                                student.student_id_number,
                                            contactNumber: '—',
                                            guardianContactPerson: '—',
                                            photoUrl: photoPreview,
                                            schoolName: 'DCCP',
                                        }"
                                        :scale="0.32"
                                    />
                                    <span
                                        class="text-center text-[11px] leading-tight font-medium"
                                        >{{ tmpl.label }}</span
                                    >
                                </button>
                            </div>
                            <input
                                type="hidden"
                                name="template"
                                :value="selectedTemplate"
                            />
                            <InputError :message="errors.template" />
                        </CardContent>
                    </Card>
                </div>

                <div class="space-y-4 self-start lg:sticky lg:top-6">
                    <Card>
                        <CardHeader class="pb-3">
                            <CardTitle class="text-base"
                                >Live Preview</CardTitle
                            >
                            <CardDescription
                                >{{ templateLabel }} template &middot; Front &
                                Back</CardDescription
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
                                        :template="selectedTemplate.startsWith('db_') ? 'custom' : selectedTemplate"
                                        :config="templates.find(t => t.value === selectedTemplate)?.config"
                                        side="front"
                                        :data="previewData"
                                    />
                                </TabsContent>
                                <TabsContent
                                    value="back"
                                    class="mt-4 flex justify-center"
                                >
                                    <IdCardPreview
                                        :template="selectedTemplate.startsWith('db_') ? 'custom' : selectedTemplate"
                                        :config="templates.find(t => t.value === selectedTemplate)?.config"
                                        side="back"
                                        :data="previewData"
                                    />
                                </TabsContent>
                                <TabsContent
                                    value="both"
                                    class="mt-4 flex justify-center"
                                >
                                    <IdCardPreview
                                        :template="selectedTemplate.startsWith('db_') ? 'custom' : selectedTemplate"
                                        :config="templates.find(t => t.value === selectedTemplate)?.config"
                                        side="both"
                                        :data="previewData"
                                    />
                                </TabsContent>
                            </Tabs>
                        </CardContent>
                    </Card>

                    <Button
                        type="submit"
                        :disabled="processing"
                        class="w-full"
                        size="lg"
                        >Save Changes</Button
                    >
                </div>
            </div>
        </Form>
    </div>
</template>
