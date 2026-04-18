<script setup lang="ts">
import { Head, usePage, router } from '@inertiajs/vue3';
import { computed, ref, onMounted } from 'vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent } from '@/components/ui/card';
import TemplateEditor from '@/components/TemplateEditor.vue';
import { update as templatesUpdate } from '@/routes/templates';
import { Save } from 'lucide-vue-next';

defineOptions({
    layout: {
        breadcrumbs: [
            { title: 'Templates', href: '/templates' },
            { title: 'Edit Template', href: '#' },
        ],
    },
});

const props = defineProps<{
    template: {
        id: number;
        name: string;
        config: any;
    };
}>();

const page = usePage();
const currentTeam = computed(() => (page.props.currentTeam as any)?.slug ?? '');

const formName = ref(props.template.name);
const templateConfig = ref(props.template.config);
const processing = ref(false);

const editorStudentData = {
    name: 'Student Name',
    course: 'Course',
    studentIdNumber: '1000',
    contactNumber: '—',
    guardianContactPerson: '—',
};

function onTemplateConfigChange(newConfig: any) {
    templateConfig.value = newConfig;
}

function submit() {
    if (!formName.value || !templateConfig.value) {
        alert('Please provide a template name and ensure the template is valid.');
        return;
    }
    
    processing.value = true;
    router.put(templatesUpdate.url({ current_team: currentTeam.value, template: props.template.id }), {
        name: formName.value,
        config: templateConfig.value,
    }, {
        onFinish: () => { processing.value = false; },
    });
}
</script>

<template>
    <Head title="Edit Template" />

    <div class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
                <h1 class="text-2xl font-bold tracking-tight">Edit Template</h1>
                <p class="text-sm text-muted-foreground">
                    Modifying "{{ template.name }}"
                </p>
            </div>
            <div class="flex items-center gap-3">
                <div class="flex items-center gap-2">
                    <Label for="name" class="whitespace-nowrap">Template Name:</Label>
                    <Input id="name" v-model="formName" placeholder="e.g. Standard Layout" class="w-[200px]" />
                </div>
                <Button @click="submit" :disabled="processing || !formName">
                    <Save class="w-4 h-4 mr-2" />
                    Save Changes
                </Button>
            </div>
        </div>

        <Card class="border-0 shadow-none bg-transparent">
            <CardContent class="p-0">
                <TemplateEditor
                    :model-value="templateConfig"
                    :photo-url="null"
                    :student-data="editorStudentData"
                    @update:model-value="onTemplateConfigChange"
                />
            </CardContent>
        </Card>
    </div>
</template>
