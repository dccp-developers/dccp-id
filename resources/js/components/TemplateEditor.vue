<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
    Plus,
    Trash2,
    ImagePlus,
    Type,
    UserCircle,
    Palette,
    ArrowLeftRight,
} from 'lucide-vue-next';
import { Separator } from '@/components/ui/separator';

type Background = {
    type: 'solid' | 'gradient' | 'image';
    solidColor: string;
    gradientStart: string;
    gradientEnd: string;
    gradientAngle: string;
    imageBase64: string | null;
};

type TextElement = {
    id: string;
    type: 'text';
    content: string;
    x: number;
    y: number;
    fontSize: number;
    fontWeight: 'normal' | 'bold';
    color: string;
    textAlign: 'left' | 'center' | 'right';
    textTransform: 'none' | 'uppercase' | 'lowercase';
};

type PhotoElement = {
    id: string;
    type: 'photo';
    x: number;
    y: number;
    width: number;
    height: number;
    borderRadius: number;
};

type TemplateElement = TextElement | PhotoElement;

type CardSide = {
    background: Background;
    elements: TemplateElement[];
};

type TemplateConfig = {
    front: CardSide;
    back: CardSide;
};

const DYNAMIC_FIELDS = [
    { label: 'Student Name', value: '{{student.name}}' },
    { label: 'Course', value: '{{student.course}}' },
    { label: 'Student ID', value: '{{student.student_id_number}}' },
    { label: 'Contact #', value: '{{student.contact_number}}' },
    { label: 'Guardian', value: '{{student.guardian_contact_person}}' },
    { label: 'School', value: '{{school_name}}' },
];

const props = defineProps<{
    modelValue: TemplateConfig | null;
    photoUrl: string | null;
    studentData: {
        name: string;
        course: string;
        studentIdNumber: string;
        contactNumber: string;
        guardianContactPerson: string;
    };
}>();

const emit = defineEmits<{
    'update:modelValue': [value: TemplateConfig];
}>();

const activeSide = ref<'front' | 'back'>('front');
const selectedElementId = ref<string | null>(null);
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });
const canvasRef = ref<HTMLElement | null>(null);

const CARD_WIDTH = 320;
const CARD_HEIGHT = 510;

const config = computed(() => {
    if (props.modelValue) return props.modelValue;
    return getDefaultConfig();
});

function getDefaultConfig(): TemplateConfig {
    return {
        front: {
            background: {
                type: 'solid',
                solidColor: '#1e3a5f',
                gradientStart: '#1e3a5f',
                gradientEnd: '#2d5a87',
                gradientAngle: '135',
                imageBase64: null,
            },
            elements: [
                {
                    id: 'el-1',
                    type: 'text',
                    content: '{{school_name}}',
                    x: 50,
                    y: 12,
                    fontSize: 9,
                    fontWeight: 'bold',
                    color: '#ffffff',
                    textAlign: 'center',
                    textTransform: 'uppercase',
                },
                {
                    id: 'el-2',
                    type: 'text',
                    content: 'Student Identification Card',
                    x: 50,
                    y: 18,
                    fontSize: 5,
                    fontWeight: 'normal',
                    color: '#ffffff',
                    textAlign: 'center',
                    textTransform: 'none',
                },
                {
                    id: 'el-3',
                    type: 'photo',
                    x: 50,
                    y: 42,
                    width: 17,
                    height: 25,
                    borderRadius: 6,
                },
                {
                    id: 'el-4',
                    type: 'text',
                    content: '{{student.name}}',
                    x: 50,
                    y: 68,
                    fontSize: 11,
                    fontWeight: 'bold',
                    color: '#ffffff',
                    textAlign: 'center',
                    textTransform: 'none',
                },
                {
                    id: 'el-5',
                    type: 'text',
                    content: '{{student.course}}',
                    x: 50,
                    y: 76,
                    fontSize: 8,
                    fontWeight: 'normal',
                    color: '#ffffffcc',
                    textAlign: 'center',
                    textTransform: 'none',
                },
                {
                    id: 'el-6',
                    type: 'text',
                    content: '{{student.student_id_number}}',
                    x: 50,
                    y: 85,
                    fontSize: 8,
                    fontWeight: 'bold',
                    color: '#ffffff',
                    textAlign: 'center',
                    textTransform: 'none',
                },
            ],
        },
        back: {
            background: {
                type: 'solid',
                solidColor: '#f8f9fa',
                gradientStart: '#f8f9fa',
                gradientEnd: '#e9ecef',
                gradientAngle: '135',
                imageBase64: null,
            },
            elements: [
                {
                    id: 'el-b1',
                    type: 'text',
                    content: '{{school_name}}',
                    x: 50,
                    y: 15,
                    fontSize: 8,
                    fontWeight: 'bold',
                    color: '#333333',
                    textAlign: 'center',
                    textTransform: 'uppercase',
                },
                {
                    id: 'el-b2',
                    type: 'text',
                    content: 'Emergency Contact',
                    x: 50,
                    y: 22,
                    fontSize: 5,
                    fontWeight: 'normal',
                    color: '#888888',
                    textAlign: 'center',
                    textTransform: 'none',
                },
                {
                    id: 'el-b3',
                    type: 'text',
                    content: 'Contact Number',
                    x: 50,
                    y: 40,
                    fontSize: 6,
                    fontWeight: 'normal',
                    color: '#888888',
                    textAlign: 'center',
                    textTransform: 'uppercase',
                },
                {
                    id: 'el-b4',
                    type: 'text',
                    content: '{{student.contact_number}}',
                    x: 50,
                    y: 48,
                    fontSize: 10,
                    fontWeight: 'bold',
                    color: '#333333',
                    textAlign: 'center',
                    textTransform: 'none',
                },
                {
                    id: 'el-b5',
                    type: 'text',
                    content: 'Guardian',
                    x: 50,
                    y: 60,
                    fontSize: 6,
                    fontWeight: 'normal',
                    color: '#888888',
                    textAlign: 'center',
                    textTransform: 'uppercase',
                },
                {
                    id: 'el-b6',
                    type: 'text',
                    content: '{{student.guardian_contact_person}}',
                    x: 50,
                    y: 68,
                    fontSize: 10,
                    fontWeight: 'bold',
                    color: '#333333',
                    textAlign: 'center',
                    textTransform: 'none',
                },
                {
                    id: 'el-b7',
                    type: 'text',
                    content: 'ID: {{student.student_id_number}}',
                    x: 50,
                    y: 88,
                    fontSize: 7,
                    fontWeight: 'normal',
                    color: '#999999',
                    textAlign: 'center',
                    textTransform: 'none',
                },
            ],
        },
    };
}

function updateConfig(updater: (c: TemplateConfig) => void) {
    const newConfig = JSON.parse(
        JSON.stringify(config.value),
    ) as TemplateConfig;
    updater(newConfig);
    emit('update:modelValue', newConfig);
}

const currentSide = computed(() => config.value[activeSide.value]);
const selectedElement = computed(() => {
    if (!selectedElementId.value) return null;
    return (
        currentSide.value.elements.find(
            (e) => e.id === selectedElementId.value,
        ) ?? null
    );
});

function addTextElement() {
    const id = `el-${Date.now()}`;
    updateConfig((c) => {
        c[activeSide.value].elements.push({
            id,
            type: 'text',
            content: 'New Text',
            x: 50,
            y: 50,
            fontSize: 10,
            fontWeight: 'normal',
            color: activeSide.value === 'front' ? '#ffffff' : '#333333',
            textAlign: 'center',
            textTransform: 'none',
        });
    });
    selectedElementId.value = id;
}

function addPhotoElement() {
    const id = `el-${Date.now()}`;
    updateConfig((c) => {
        c[activeSide.value].elements.push({
            id,
            type: 'photo',
            x: 50,
            y: 40,
            width: 17,
            height: 25,
            borderRadius: 6,
        });
    });
    selectedElementId.value = id;
}

function deleteElement(id: string) {
    updateConfig((c) => {
        c[activeSide.value].elements = c[activeSide.value].elements.filter(
            (e) => e.id !== id,
        );
    });
    if (selectedElementId.value === id) selectedElementId.value = null;
}

function selectElement(id: string) {
    selectedElementId.value = id;
}
function onCanvasClick() {
    selectedElementId.value = null;
}

function onElementMouseDown(e: MouseEvent, elId: string) {
    e.preventDefault();
    e.stopPropagation();
    selectedElementId.value = elId;
    isDragging.value = true;
    const el = currentSide.value.elements.find((e2) => e2.id === elId);
    if (!el) return;
    const canvasRect = canvasRef.value?.getBoundingClientRect();
    if (!canvasRect) return;
    dragOffset.value = {
        x: e.clientX - (canvasRect.width * el.x) / 100,
        y: e.clientY - (canvasRect.height * el.y) / 100,
    };
}

function onMouseMove(e: MouseEvent) {
    if (!isDragging.value || !selectedElementId.value || !canvasRef.value)
        return;
    const canvasRect = canvasRef.value.getBoundingClientRect();
    const newX = ((e.clientX - dragOffset.value.x) / canvasRect.width) * 100;
    const newY = ((e.clientY - dragOffset.value.y) / canvasRect.height) * 100;
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find(
            (e2) => e2.id === selectedElementId.value,
        );
        if (el) {
            el.x = Math.max(5, Math.min(95, newX));
            el.y = Math.max(5, Math.min(95, newY));
        }
    });
}

function onMouseUp() {
    isDragging.value = false;
}

function onBackgroundImageUpload(e: Event) {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
        const base64 = ev.target?.result as string;
        updateConfig((c) => {
            c[activeSide.value].background.imageBase64 = base64;
            c[activeSide.value].background.type = 'image';
        });
    };
    reader.readAsDataURL(file);
}

function insertField(field: string) {
    if (!selectedElementId.value) return;
    const el = currentSide.value.elements.find(
        (e) => e.id === selectedElementId.value,
    );
    if (!el || el.type !== 'text') return;
    updateConfig((c) => {
        const txt = c[activeSide.value].elements.find(
            (e) => e.id === selectedElementId.value,
        );
        if (txt && txt.type === 'text') txt.content = field;
    });
}

function resolveContent(content: string): string {
    const map: Record<string, string> = {
        '{{student.name}}': props.studentData.name || 'Student Name',
        '{{student.course}}': props.studentData.course || 'Course',
        '{{student.student_id_number}}':
            props.studentData.studentIdNumber || '1000',
        '{{student.contact_number}}': props.studentData.contactNumber || '—',
        '{{student.guardian_contact_person}}':
            props.studentData.guardianContactPerson || '—',
        '{{school_name}}': 'DCCP',
    };
    return map[content] ?? content;
}

function getBackgroundStyle(bg: Background): Record<string, string> {
    if (bg.type === 'gradient')
        return {
            background: `linear-gradient(${bg.gradientAngle || 135}deg, ${bg.gradientStart || '#667eea'}, ${bg.gradientEnd || '#764ba2'})`,
        };
    if (bg.type === 'image' && bg.imageBase64)
        return {
            backgroundImage: `url(${bg.imageBase64})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
        };
    return { backgroundColor: bg.solidColor || '#1e3a5f' };
}

onMounted(() => {
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
});
onUnmounted(() => {
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
});
</script>

<template>
    <div class="space-y-4">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
                <Button
                    size="sm"
                    :variant="activeSide === 'front' ? 'default' : 'outline'"
                    @click="
                        activeSide = 'front';
                        selectedElementId = null;
                    "
                >
                    <ArrowLeftRight class="mr-1.5 size-3.5" /> Front
                </Button>
                <Button
                    size="sm"
                    :variant="activeSide === 'back' ? 'default' : 'outline'"
                    @click="
                        activeSide = 'back';
                        selectedElementId = null;
                    "
                >
                    <ArrowLeftRight class="mr-1.5 size-3.5" /> Back
                </Button>
                <span class="ml-1 text-xs text-muted-foreground"
                    >Editing:
                    {{ activeSide === 'front' ? 'Front' : 'Back' }}</span
                >
            </div>
            <div class="flex gap-1.5">
                <Button size="sm" variant="outline" @click="addTextElement"
                    ><Type class="mr-1 size-3" /> Text</Button
                >
                <Button size="sm" variant="outline" @click="addPhotoElement"
                    ><UserCircle class="mr-1 size-3" /> Photo</Button
                >
                <label
                    class="inline-flex cursor-pointer items-center gap-1.5 rounded-md border px-3 py-1.5 text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground"
                >
                    <ImagePlus class="size-3" /> BG Image
                    <input
                        type="file"
                        accept="image/*"
                        class="hidden"
                        @change="onBackgroundImageUpload"
                    />
                </label>
            </div>
        </div>

        <div class="grid gap-4 xl:grid-cols-[1fr_280px]">
            <div class="flex justify-center">
                <div
                    ref="canvasRef"
                    class="relative cursor-crosshair overflow-hidden rounded-lg shadow-lg select-none"
                    :style="{
                        width: CARD_WIDTH + 'px',
                        height: CARD_HEIGHT + 'px',
                        ...getBackgroundStyle(currentSide.background),
                    }"
                    @click="onCanvasClick"
                >
                    <div
                        v-for="el in currentSide.elements"
                        :key="el.id"
                        class="absolute cursor-move"
                        :class="{
                            'z-10 ring-2 ring-primary ring-offset-1':
                                selectedElementId === el.id,
                            'ring-1 ring-transparent hover:ring-primary/30':
                                selectedElementId !== el.id,
                        }"
                        :style="{
                            left: el.x + '%',
                            top: el.y + '%',
                            transform: 'translate(-50%, -50%)',
                        }"
                        @mousedown="onElementMouseDown($event, el.id)"
                    >
                        <div
                            v-if="el.type === 'photo'"
                            class="flex items-center justify-center overflow-hidden bg-black/20"
                            :style="{
                                width: (el.width / 100) * CARD_WIDTH + 'px',
                                height: (el.height / 100) * CARD_HEIGHT + 'px',
                                borderRadius: el.borderRadius + 'px',
                            }"
                        >
                            <img
                                v-if="photoUrl"
                                :src="photoUrl"
                                alt=""
                                class="size-full object-cover"
                                :style="{
                                    borderRadius: el.borderRadius + 'px',
                                }"
                            />
                            <UserCircle v-else class="size-8 text-white/60" />
                        </div>
                        <div
                            v-else-if="el.type === 'text'"
                            :style="{
                                fontSize: el.fontSize + 'px',
                                fontWeight: el.fontWeight,
                                color: el.color,
                                textAlign: el.textAlign,
                                textTransform: el.textTransform as any,
                                whiteSpace: 'nowrap',
                                minWidth: '20px',
                            }"
                        >
                            {{ resolveContent(el.content) }}
                        </div>
                    </div>
                </div>
            </div>

            <div class="space-y-4">
                <Card>
                    <CardHeader class="pb-3">
                        <div class="flex items-center gap-2">
                            <Palette class="size-4 text-muted-foreground" />
                            <CardTitle class="text-sm">Background</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-3">
                        <div class="flex gap-1.5">
                            <Button
                                size="sm"
                                :variant="
                                    currentSide.background.type === 'solid'
                                        ? 'default'
                                        : 'outline'
                                "
                                class="flex-1"
                                @click="
                                    updateConfig((c) => {
                                        c[activeSide].background.type = 'solid';
                                    })
                                "
                                >Solid</Button
                            >
                            <Button
                                size="sm"
                                :variant="
                                    currentSide.background.type === 'gradient'
                                        ? 'default'
                                        : 'outline'
                                "
                                class="flex-1"
                                @click="
                                    updateConfig((c) => {
                                        c[activeSide].background.type =
                                            'gradient';
                                    })
                                "
                                >Gradient</Button
                            >
                        </div>
                        <div
                            v-if="currentSide.background.type === 'solid'"
                            class="space-y-1.5"
                        >
                            <Label class="text-xs">Color</Label>
                            <div class="flex items-center gap-2">
                                <input
                                    type="color"
                                    :value="currentSide.background.solidColor"
                                    @input="
                                        updateConfig((c) => {
                                            c[
                                                activeSide
                                            ].background.solidColor = (
                                                $event.target as HTMLInputElement
                                            ).value;
                                        })
                                    "
                                    class="size-7 cursor-pointer rounded border"
                                />
                                <Input
                                    :value="currentSide.background.solidColor"
                                    @input="
                                        updateConfig((c) => {
                                            c[
                                                activeSide
                                            ].background.solidColor = (
                                                $event.target as HTMLInputElement
                                            ).value;
                                        })
                                    "
                                    class="h-7 flex-1 font-mono text-xs"
                                />
                            </div>
                        </div>
                        <div
                            v-if="currentSide.background.type === 'gradient'"
                            class="space-y-2"
                        >
                            <Label class="text-xs">Start Color</Label>
                            <div class="flex items-center gap-2">
                                <input
                                    type="color"
                                    :value="
                                        currentSide.background.gradientStart
                                    "
                                    @input="
                                        updateConfig((c) => {
                                            c[
                                                activeSide
                                            ].background.gradientStart = (
                                                $event.target as HTMLInputElement
                                            ).value;
                                        })
                                    "
                                    class="size-7 cursor-pointer rounded border"
                                />
                                <Input
                                    :value="
                                        currentSide.background.gradientStart
                                    "
                                    @input="
                                        updateConfig((c) => {
                                            c[
                                                activeSide
                                            ].background.gradientStart = (
                                                $event.target as HTMLInputElement
                                            ).value;
                                        })
                                    "
                                    class="h-7 flex-1 font-mono text-xs"
                                />
                            </div>
                            <Label class="text-xs">End Color</Label>
                            <div class="flex items-center gap-2">
                                <input
                                    type="color"
                                    :value="currentSide.background.gradientEnd"
                                    @input="
                                        updateConfig((c) => {
                                            c[
                                                activeSide
                                            ].background.gradientEnd = (
                                                $event.target as HTMLInputElement
                                            ).value;
                                        })
                                    "
                                    class="size-7 cursor-pointer rounded border"
                                />
                                <Input
                                    :value="currentSide.background.gradientEnd"
                                    @input="
                                        updateConfig((c) => {
                                            c[
                                                activeSide
                                            ].background.gradientEnd = (
                                                $event.target as HTMLInputElement
                                            ).value;
                                        })
                                    "
                                    class="h-7 flex-1 font-mono text-xs"
                                />
                            </div>
                            <Label class="text-xs"
                                >Angle:
                                {{
                                    currentSide.background.gradientAngle
                                }}&deg;</Label
                            >
                            <input
                                type="range"
                                min="0"
                                max="360"
                                :value="currentSide.background.gradientAngle"
                                @input="
                                    updateConfig((c) => {
                                        c[activeSide].background.gradientAngle =
                                            (
                                                $event.target as HTMLInputElement
                                            ).value;
                                    })
                                "
                                class="w-full"
                            />
                        </div>
                    </CardContent>
                </Card>

                <Card v-if="selectedElement && selectedElement.type === 'text'">
                    <CardHeader class="pb-3">
                        <div class="flex items-center justify-between">
                            <CardTitle class="text-sm"
                                >Text Properties</CardTitle
                            >
                            <Button
                                variant="ghost"
                                size="icon"
                                class="size-6 text-destructive"
                                @click="deleteElement(selectedElementId!)"
                                ><Trash2 class="size-3"
                            /></Button>
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-3">
                        <div class="space-y-1.5">
                            <Label class="text-xs">Content</Label>
                            <Input
                                :value="selectedElement.content"
                                @input="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'text')
                                            el.content = (
                                                $event.target as HTMLInputElement
                                            ).value;
                                    })
                                "
                            />
                            <div class="flex flex-wrap gap-1">
                                <button
                                    v-for="field in DYNAMIC_FIELDS"
                                    :key="field.value"
                                    class="rounded border px-1.5 py-0.5 text-[10px] hover:bg-accent"
                                    @click="insertField(field.value)"
                                >
                                    {{ field.label }}
                                </button>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2">
                            <div class="space-y-1">
                                <Label class="text-xs"
                                    >Size:
                                    {{ selectedElement.fontSize }}px</Label
                                >
                                <input
                                    type="range"
                                    min="6"
                                    max="24"
                                    :value="selectedElement.fontSize"
                                    @input="
                                        updateConfig((c) => {
                                            const el = c[
                                                activeSide
                                            ].elements.find(
                                                (e) =>
                                                    e.id === selectedElementId,
                                            );
                                            if (el && el.type === 'text')
                                                el.fontSize = parseInt(
                                                    (
                                                        $event.target as HTMLInputElement
                                                    ).value,
                                                );
                                        })
                                    "
                                    class="w-full"
                                />
                            </div>
                            <div class="space-y-1">
                                <Label class="text-xs">Color</Label>
                                <input
                                    type="color"
                                    :value="selectedElement.color"
                                    @input="
                                        updateConfig((c) => {
                                            const el = c[
                                                activeSide
                                            ].elements.find(
                                                (e) =>
                                                    e.id === selectedElementId,
                                            );
                                            if (el && el.type === 'text')
                                                el.color = (
                                                    $event.target as HTMLInputElement
                                                ).value;
                                        })
                                    "
                                    class="size-7 w-full cursor-pointer rounded border"
                                />
                            </div>
                        </div>
                        <div class="flex gap-1.5">
                            <Button
                                size="sm"
                                :variant="
                                    selectedElement.fontWeight === 'bold'
                                        ? 'default'
                                        : 'outline'
                                "
                                @click="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'text')
                                            el.fontWeight = 'bold';
                                    })
                                "
                                class="flex-1"
                                >Bold</Button
                            >
                            <Button
                                size="sm"
                                :variant="
                                    selectedElement.textAlign === 'left'
                                        ? 'default'
                                        : 'outline'
                                "
                                @click="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'text')
                                            el.textAlign = 'left';
                                    })
                                "
                                class="flex-1"
                                >Left</Button
                            >
                            <Button
                                size="sm"
                                :variant="
                                    selectedElement.textAlign === 'center'
                                        ? 'default'
                                        : 'outline'
                                "
                                @click="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'text')
                                            el.textAlign = 'center';
                                    })
                                "
                                class="flex-1"
                                >Center</Button
                            >
                            <Button
                                size="sm"
                                :variant="
                                    selectedElement.textAlign === 'right'
                                        ? 'default'
                                        : 'outline'
                                "
                                @click="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'text')
                                            el.textAlign = 'right';
                                    })
                                "
                                class="flex-1"
                                >Right</Button
                            >
                        </div>
                        <div class="flex gap-1.5">
                            <Button
                                size="sm"
                                :variant="
                                    selectedElement.textTransform === 'none'
                                        ? 'default'
                                        : 'outline'
                                "
                                @click="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'text')
                                            el.textTransform = 'none';
                                    })
                                "
                                class="flex-1"
                                >Aa</Button
                            >
                            <Button
                                size="sm"
                                :variant="
                                    selectedElement.textTransform ===
                                    'uppercase'
                                        ? 'default'
                                        : 'outline'
                                "
                                @click="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'text')
                                            el.textTransform = 'uppercase';
                                    })
                                "
                                class="flex-1"
                                >AA</Button
                            >
                        </div>
                    </CardContent>
                </Card>

                <Card
                    v-else-if="
                        selectedElement && selectedElement.type === 'photo'
                    "
                >
                    <CardHeader class="pb-3">
                        <div class="flex items-center justify-between">
                            <CardTitle class="text-sm"
                                >Photo Properties</CardTitle
                            >
                            <Button
                                variant="ghost"
                                size="icon"
                                class="size-6 text-destructive"
                                @click="deleteElement(selectedElementId!)"
                                ><Trash2 class="size-3"
                            /></Button>
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-3">
                        <div class="space-y-1">
                            <Label class="text-xs"
                                >Width: {{ selectedElement.width }}%</Label
                            >
                            <input
                                type="range"
                                min="5"
                                max="50"
                                :value="selectedElement.width"
                                @input="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'photo')
                                            el.width = parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            );
                                    })
                                "
                                class="w-full"
                            />
                        </div>
                        <div class="space-y-1">
                            <Label class="text-xs"
                                >Height: {{ selectedElement.height }}%</Label
                            >
                            <input
                                type="range"
                                min="5"
                                max="50"
                                :value="selectedElement.height"
                                @input="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'photo')
                                            el.height = parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            );
                                    })
                                "
                                class="w-full"
                            />
                        </div>
                        <div class="space-y-1">
                            <Label class="text-xs"
                                >Roundness:
                                {{ selectedElement.borderRadius }}px</Label
                            >
                            <input
                                type="range"
                                min="0"
                                max="50"
                                :value="selectedElement.borderRadius"
                                @input="
                                    updateConfig((c) => {
                                        const el = c[activeSide].elements.find(
                                            (e) => e.id === selectedElementId,
                                        );
                                        if (el && el.type === 'photo')
                                            el.borderRadius = parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            );
                                    })
                                "
                                class="w-full"
                            />
                        </div>
                    </CardContent>
                </Card>

                <Card v-else>
                    <CardHeader class="pb-3">
                        <CardTitle class="text-sm">Elements</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p class="mb-2 text-xs text-muted-foreground">
                            Click an element on the card to edit, or add new
                            ones above.
                        </p>
                        <div class="max-h-48 space-y-1 overflow-y-auto">
                            <div
                                v-for="el in currentSide.elements"
                                :key="el.id"
                                class="flex cursor-pointer items-center justify-between rounded-md px-2 py-1.5 text-xs hover:bg-accent"
                                :class="{
                                    'bg-accent': selectedElementId === el.id,
                                }"
                                @click="selectedElementId = el.id"
                            >
                                <span class="flex items-center gap-1.5">
                                    <Type
                                        v-if="el.type === 'text'"
                                        class="size-3"
                                    />
                                    <UserCircle v-else class="size-3" />
                                    {{
                                        el.type === 'photo'
                                            ? 'Photo'
                                            : el.content.length > 20
                                              ? resolveContent(
                                                    el.content,
                                                ).substring(0, 20) + '...'
                                              : resolveContent(el.content)
                                    }}
                                </span>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-5 text-destructive"
                                    @click.stop="deleteElement(el.id)"
                                    ><Trash2 class="size-3"
                                /></Button>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    </div>
</template>
