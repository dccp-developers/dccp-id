<script setup lang="ts">
import { Head, usePage, router } from '@inertiajs/vue3';
import { computed, ref } from 'vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import TemplateEditor from '@/components/TemplateEditor.vue';
import { store as templatesStore } from '@/routes/templates';
import { Save } from 'lucide-vue-next';

defineOptions({
    layout: {
        breadcrumbs: [
            { title: 'Templates', href: '/templates' },
            { title: 'Create Template', href: '#' },
        ],
    },
});

const page = usePage();
const currentTeam = computed(() => (page.props.currentTeam as any)?.slug ?? '');

const formName = ref('');
const templateConfig = ref(null);
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
    router.post(templatesStore.url({ current_team: currentTeam.value }), {
        name: formName.value,
        config: templateConfig.value,
    }, {
        onFinish: () => { processing.value = false; },
    });
}
</script>

<template>
    <Head title="Create Template" />

    <div class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
                <h1 class="text-2xl font-bold tracking-tight">Create Template</h1>
                <p class="text-sm text-muted-foreground">
                    Design a new custom ID card template
                </p>
            </div>
            <div class="flex items-center gap-3">
                <div class="flex items-center gap-2">
                    <Label for="name" class="whitespace-nowrap">Template Name:</Label>
                    <Input id="name" v-model="formName" placeholder="e.g. Standard Layout" class="w-[200px]" />
                </div>
                <Button @click="submit" :disabled="processing || !formName">
                    <Save class="w-4 h-4 mr-2" />
                    Save Template
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
