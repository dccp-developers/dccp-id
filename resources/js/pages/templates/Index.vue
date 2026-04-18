<script setup lang="ts">
import { Head, Link, usePage } from '@inertiajs/vue3';
import { computed } from 'vue';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Plus, Palette, Settings2, Trash2 } from 'lucide-vue-next';
import IdCardPreview from '@/components/IdCardPreview.vue';
import { index as templatesIndex, create as templatesCreate, edit as templatesEdit, destroy as templatesDestroy } from '@/routes/templates';
import { router } from '@inertiajs/vue3';

defineOptions({
    layout: {
        breadcrumbs: [
            { title: 'Templates', href: '#' },
        ],
    },
});

const props = defineProps<{
    templates: Array<{
        id: number;
        name: string;
        config: any;
    }>;
}>();

const page = usePage();
const currentTeam = computed(() => (page.props.currentTeam as any)?.slug ?? '');

const dummyData = {
    name: 'Juan Dela Cruz',
    course: 'BS Information Technology',
    studentIdNumber: '2023-0001',
    contactNumber: '0912 345 6789',
    guardianContactPerson: 'Maria Dela Cruz',
    photoUrl: null,
    schoolName: 'DCCP',
};

function deleteTemplate(id: number) {
    if (confirm('Are you sure you want to delete this template?')) {
        router.delete(templatesDestroy.url({ current_team: currentTeam.value, template: id }));
    }
}
</script>

<template>
    <Head title="Templates" />

    <div class="space-y-6 px-4 py-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
                <h1 class="text-2xl font-bold tracking-tight">Templates</h1>
                <p class="text-sm text-muted-foreground">
                    Design and manage custom ID card templates
                </p>
            </div>
            <Link :href="templatesCreate.url({ current_team: currentTeam })">
                <Button>
                    <Plus class="mr-2 size-4" />
                    New Template
                </Button>
            </Link>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card v-for="template in templates" :key="template.id" class="flex flex-col overflow-hidden">
                <CardHeader class="pb-4 bg-muted/20 border-b">
                    <div class="flex items-center justify-between">
                        <CardTitle class="text-base flex items-center gap-2">
                            <Palette class="w-4 h-4 text-primary" />
                            {{ template.name }}
                        </CardTitle>
                        <div class="flex items-center gap-1">
                            <Link :href="templatesEdit.url({ current_team: currentTeam, template: template.id })">
                                <Button variant="ghost" size="icon" class="h-8 w-8 text-muted-foreground hover:text-primary">
                                    <Settings2 class="w-4 h-4" />
                                </Button>
                            </Link>
                            <Button variant="ghost" size="icon" class="h-8 w-8 text-destructive hover:text-destructive hover:bg-destructive/10" @click="deleteTemplate(template.id)">
                                <Trash2 class="w-4 h-4" />
                            </Button>
                        </div>
                    </div>
                </CardHeader>
                <CardContent class="flex-1 flex flex-col items-center justify-center p-6 bg-muted/5">
                    <div class="transform scale-90 origin-top">
                        <IdCardPreview
                            template="custom"
                            side="front"
                            :config="template.config"
                            :data="dummyData"
                            :scale="0.8"
                        />
                    </div>
                </CardContent>
            </Card>

            <div v-if="templates.length === 0" class="col-span-full py-12 text-center text-muted-foreground bg-muted/10 rounded-xl border border-dashed">
                <Palette class="w-12 h-12 mx-auto mb-4 opacity-20" />
                <h3 class="text-lg font-medium text-foreground mb-1">No templates yet</h3>
                <p class="text-sm mb-4">Create your first custom ID card template to get started.</p>
                <Link :href="templatesCreate.url({ current_team: currentTeam })">
                    <Button variant="outline">Create Template</Button>
                </Link>
            </div>
        </div>
    </div>
</template>
