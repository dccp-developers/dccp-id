<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import {
    Trash2,
    ImagePlus,
    Type,
    UserCircle,
    Palette,
    ArrowLeftRight,
    Undo2,
    Redo2,
    Bold,
    AlignLeft,
    AlignCenter,
    AlignRight,
    CaseSensitive,
    Copy,
    ChevronUp,
    ChevronDown,
    MousePointerClick,
    Maximize2,
} from 'lucide-vue-next';

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
    letterSpacing: number;
    lineHeight: number;
    opacity: number;
    rotation: number;
};

type PhotoElement = {
    id: string;
    type: 'photo';
    x: number;
    y: number;
    width: number;
    height: number;
    borderRadius: number;
    opacity: number;
    borderColor: string;
    borderWidth: number;
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
const isResizing = ref(false);
const resizeHandle = ref<string | null>(null);
const dragOffset = ref({ x: 0, y: 0 });
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0, elX: 0, elY: 0 });
const canvasRef = ref<HTMLElement | null>(null);
const fileInputRef = ref<HTMLInputElement | null>(null);
const editingTextId = ref<string | null>(null);
const editTextRef = ref<HTMLElement | null>(null);
const showFieldPicker = ref(false);
const snapLines = ref<{ type: 'vertical' | 'horizontal'; pos: number }[]>([]);

const CARD_WIDTH = 320;
const CARD_HEIGHT = 510;
const MIN_SIZE = 5;
const MAX_HISTORY = 50;

const config = computed(() => {
    if (props.modelValue) return props.modelValue;
    return getDefaultConfig();
});

const history = ref<string[]>([]);
const historyIndex = ref(-1);
const skipHistory = ref(false);

function pushHistory(c: TemplateConfig) {
    if (skipHistory.value) return;
    const json = JSON.stringify(c);
    if (historyIndex.value >= 0 && history.value[historyIndex.value] === json)
        return;
    history.value = history.value.slice(0, historyIndex.value + 1);
    history.value.push(json);
    if (history.value.length > MAX_HISTORY) history.value.shift();
    historyIndex.value = history.value.length - 1;
}

function undo() {
    if (historyIndex.value <= 0) return;
    historyIndex.value--;
    skipHistory.value = true;
    emit('update:modelValue', JSON.parse(history.value[historyIndex.value]));
    skipHistory.value = false;
}

function redo() {
    if (historyIndex.value >= history.value.length - 1) return;
    historyIndex.value++;
    skipHistory.value = true;
    emit('update:modelValue', JSON.parse(history.value[historyIndex.value]));
    skipHistory.value = false;
}

const canUndo = computed(() => historyIndex.value > 0);
const canRedo = computed(() => historyIndex.value < history.value.length - 1);

watch(
    () => props.modelValue,
    (val) => {
        if (val && !skipHistory.value) pushHistory(val);
    },
    { immediate: true },
);

function makeTextElement(
    overrides: Partial<TextElement> & { id: string },
): TextElement {
    return {
        content: 'New Text',
        x: 50,
        y: 50,
        fontSize: 10,
        fontWeight: 'normal',
        color: activeSide.value === 'front' ? '#ffffff' : '#333333',
        textAlign: 'center',
        textTransform: 'none',
        letterSpacing: 0,
        lineHeight: 1.2,
        opacity: 100,
        rotation: 0,
        ...overrides,
    } as TextElement;
}

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
                makeTextElement({
                    id: 'el-1',
                    content: '{{school_name}}',
                    x: 50,
                    y: 12,
                    fontSize: 9,
                    fontWeight: 'bold',
                    color: '#ffffff',
                    textAlign: 'center',
                    textTransform: 'uppercase',
                }),
                makeTextElement({
                    id: 'el-2',
                    content: 'Student Identification Card',
                    x: 50,
                    y: 18,
                    fontSize: 5,
                    color: '#ffffff',
                    textAlign: 'center',
                }),
                {
                    id: 'el-3',
                    type: 'photo',
                    x: 50,
                    y: 42,
                    width: 17,
                    height: 25,
                    borderRadius: 6,
                    opacity: 100,
                    borderColor: '#ffffff33',
                    borderWidth: 1,
                },
                makeTextElement({
                    id: 'el-4',
                    content: '{{student.name}}',
                    x: 50,
                    y: 68,
                    fontSize: 11,
                    fontWeight: 'bold',
                    color: '#ffffff',
                    letterSpacing: 0.5,
                }),
                makeTextElement({
                    id: 'el-5',
                    content: '{{student.course}}',
                    x: 50,
                    y: 76,
                    fontSize: 8,
                    color: '#ffffffcc',
                    textAlign: 'center',
                }),
                makeTextElement({
                    id: 'el-6',
                    content: '{{student.student_id_number}}',
                    x: 50,
                    y: 85,
                    fontSize: 8,
                    fontWeight: 'bold',
                    color: '#ffffff',
                    letterSpacing: 1,
                }),
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
                makeTextElement({
                    id: 'el-b1',
                    content: '{{school_name}}',
                    x: 50,
                    y: 15,
                    fontSize: 8,
                    fontWeight: 'bold',
                    color: '#333333',
                    textTransform: 'uppercase',
                }),
                makeTextElement({
                    id: 'el-b2',
                    content: 'Emergency Contact',
                    x: 50,
                    y: 22,
                    fontSize: 5,
                    color: '#888888',
                }),
                makeTextElement({
                    id: 'el-b3',
                    content: 'Contact Number',
                    x: 50,
                    y: 40,
                    fontSize: 6,
                    color: '#888888',
                    textTransform: 'uppercase',
                }),
                makeTextElement({
                    id: 'el-b4',
                    content: '{{student.contact_number}}',
                    x: 50,
                    y: 48,
                    fontSize: 10,
                    fontWeight: 'bold',
                    color: '#333333',
                }),
                makeTextElement({
                    id: 'el-b5',
                    content: 'Guardian',
                    x: 50,
                    y: 60,
                    fontSize: 6,
                    color: '#888888',
                    textTransform: 'uppercase',
                }),
                makeTextElement({
                    id: 'el-b6',
                    content: '{{student.guardian_contact_person}}',
                    x: 50,
                    y: 68,
                    fontSize: 10,
                    fontWeight: 'bold',
                    color: '#333333',
                }),
                makeTextElement({
                    id: 'el-b7',
                    content: 'ID: {{student.student_id_number}}',
                    x: 50,
                    y: 88,
                    fontSize: 7,
                    color: '#999999',
                }),
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
const selectedTextElement = computed((): TextElement | null => {
    if (!selectedElementId.value) return null;
    const el = currentSide.value.elements.find(
        (e) => e.id === selectedElementId.value,
    );
    return el && el.type === 'text' ? el : null;
});
const selectedPhotoElement = computed((): PhotoElement | null => {
    if (!selectedElementId.value) return null;
    const el = currentSide.value.elements.find(
        (e) => e.id === selectedElementId.value,
    );
    return el && el.type === 'photo' ? el : null;
});

function addTextElement() {
    const id = `el-${Date.now()}`;
    updateConfig((c) => {
        c[activeSide.value].elements.push(makeTextElement({ id }));
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
            opacity: 100,
            borderColor: '#ffffff33',
            borderWidth: 1,
        });
    });
    selectedElementId.value = id;
}

function duplicateElement(id: string) {
    const el = currentSide.value.elements.find((e) => e.id === id);
    if (!el) return;
    const newId = `el-${Date.now()}`;
    updateConfig((c) => {
        const src = c[activeSide.value].elements.find((e) => e.id === id);
        if (!src) return;
        const clone = JSON.parse(JSON.stringify(src));
        clone.id = newId;
        (clone as any).x = Math.min(95, (src as any).x + 3);
        (clone as any).y = Math.min(95, (src as any).y + 3);
        c[activeSide.value].elements.push(clone);
    });
    selectedElementId.value = newId;
}

function moveElementOrder(id: string, direction: 'up' | 'down') {
    updateConfig((c) => {
        const els = c[activeSide.value].elements;
        const idx = els.findIndex((e) => e.id === id);
        if (idx === -1) return;
        if (direction === 'up' && idx < els.length - 1) {
            [els[idx], els[idx + 1]] = [els[idx + 1], els[idx]];
        } else if (direction === 'down' && idx > 0) {
            [els[idx], els[idx - 1]] = [els[idx - 1], els[idx]];
        }
    });
}

function deleteElement(id: string) {
    updateConfig((c) => {
        c[activeSide.value].elements = c[activeSide.value].elements.filter(
            (e) => e.id !== id,
        );
    });
    if (selectedElementId.value === id) selectedElementId.value = null;
    if (editingTextId.value === id) editingTextId.value = null;
}

function selectElement(id: string) {
    selectedElementId.value = id;
}

function onCanvasClick() {
    selectedElementId.value = null;
    showFieldPicker.value = false;
}

function startEditText(elId: string) {
    editingTextId.value = elId;
    selectedElementId.value = elId;
    nextTick(() => {
        if (editTextRef.value) {
            editTextRef.value.focus();
            const range = document.createRange();
            range.selectNodeContents(editTextRef.value);
            const sel = window.getSelection();
            sel?.removeAllRanges();
            sel?.addRange(range);
        }
    });
}

function finishEditText() {
    if (!editingTextId.value || !editTextRef.value) return;
    const text =
        editTextRef.value.innerText || editTextRef.value.textContent || '';
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find(
            (e) => e.id === editingTextId.value,
        );
        if (el && el.type === 'text') el.content = text;
    });
    editingTextId.value = null;
}

function onEditTextBlur() {
    finishEditText();
}

function onEditTextInput(e: Event) {
    const target = e.target as HTMLElement;
    const text = target.innerText || target.textContent || '';
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find(
            (e) => e.id === editingTextId.value,
        );
        if (el && el.type === 'text') el.content = text;
    });
}

function onElementMouseDown(e: MouseEvent, elId: string) {
    if (editingTextId.value === elId) return;
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

function onResizeMouseDown(e: MouseEvent, elId: string, handle: string) {
    e.preventDefault();
    e.stopPropagation();
    selectedElementId.value = elId;
    isResizing.value = true;
    resizeHandle.value = handle;
    const el = currentSide.value.elements.find((e2) => e2.id === elId);
    if (!el || el.type !== 'photo') return;
    resizeStart.value = {
        x: e.clientX,
        y: e.clientY,
        width: el.width,
        height: el.height,
        elX: el.x,
        elY: el.y,
    };
}

function computeSnap(newPos: number, axis: 'x' | 'y'): number {
    const guides = [10, 25, 50, 75, 90];
    const threshold = 1.5;
    for (const g of guides) {
        if (Math.abs(newPos - g) < threshold) {
            snapLines.value = [
                { type: axis === 'x' ? 'vertical' : 'horizontal', pos: g },
            ];
            return g;
        }
    }
    snapLines.value = [];
    return newPos;
}

function onMouseMove(e: MouseEvent) {
    if (
        isResizing.value &&
        selectedElementId.value &&
        resizeHandle.value &&
        canvasRef.value
    ) {
        const canvasRect = canvasRef.value.getBoundingClientRect();
        const dx = e.clientX - resizeStart.value.x;
        const dy = e.clientY - resizeStart.value.y;
        const dwPct = (dx / canvasRect.width) * 100;
        const dhPct = (dy / canvasRect.height) * 100;

        updateConfig((c) => {
            const el = c[activeSide.value].elements.find(
                (e2) => e2.id === selectedElementId.value,
            );
            if (!el || el.type !== 'photo') return;

            if (resizeHandle.value === 'se') {
                el.width = Math.max(
                    MIN_SIZE,
                    Math.min(80, resizeStart.value.width + dwPct),
                );
                el.height = Math.max(
                    MIN_SIZE,
                    Math.min(80, resizeStart.value.height + dhPct),
                );
            } else if (resizeHandle.value === 'sw') {
                const newWidth = Math.max(
                    MIN_SIZE,
                    Math.min(80, resizeStart.value.width - dwPct),
                );
                const widthDiff = newWidth - resizeStart.value.width;
                el.width = newWidth;
                el.x = Math.max(
                    5,
                    Math.min(95, resizeStart.value.elX - widthDiff / 2),
                );
                el.height = Math.max(
                    MIN_SIZE,
                    Math.min(80, resizeStart.value.height + dhPct),
                );
            } else if (resizeHandle.value === 'ne') {
                const newHeight = Math.max(
                    MIN_SIZE,
                    Math.min(80, resizeStart.value.height - dhPct),
                );
                const heightDiff = newHeight - resizeStart.value.height;
                el.width = Math.max(
                    MIN_SIZE,
                    Math.min(80, resizeStart.value.width + dwPct),
                );
                el.height = newHeight;
                el.y = Math.max(
                    5,
                    Math.min(95, resizeStart.value.elY - heightDiff / 2),
                );
            } else if (resizeHandle.value === 'nw') {
                const newWidth = Math.max(
                    MIN_SIZE,
                    Math.min(80, resizeStart.value.width - dwPct),
                );
                const newHeight = Math.max(
                    MIN_SIZE,
                    Math.min(80, resizeStart.value.height - dhPct),
                );
                const widthDiff = newWidth - resizeStart.value.width;
                const heightDiff = newHeight - resizeStart.value.height;
                el.width = newWidth;
                el.height = newHeight;
                el.x = Math.max(
                    5,
                    Math.min(95, resizeStart.value.elX - widthDiff / 2),
                );
                el.y = Math.max(
                    5,
                    Math.min(95, resizeStart.value.elY - heightDiff / 2),
                );
            }
        });
        return;
    }

    if (!isDragging.value || !selectedElementId.value || !canvasRef.value)
        return;
    const canvasRect = canvasRef.value.getBoundingClientRect();
    const rawX = ((e.clientX - dragOffset.value.x) / canvasRect.width) * 100;
    const rawY = ((e.clientY - dragOffset.value.y) / canvasRect.height) * 100;
    const newX = computeSnap(Math.max(5, Math.min(95, rawX)), 'x');
    const newY = computeSnap(Math.max(5, Math.min(95, rawY)), 'y');
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find(
            (e2) => e2.id === selectedElementId.value,
        );
        if (el) {
            el.x = newX;
            el.y = newY;
        }
    });
}

function onMouseUp() {
    isDragging.value = false;
    isResizing.value = false;
    resizeHandle.value = null;
    snapLines.value = [];
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
    showFieldPicker.value = false;
}

function resolveContent(content: string): string {
    const map: Record<string, string> = {
        '{{student.name}}': props.studentData.name || 'Student Name',
        '{{student.course}}': props.studentData.course || 'Course',
        '{{student.student_id_number}}':
            props.studentData.studentIdNumber || '1000',
        '{{student.contact_number}}':
            props.studentData.contactNumber || '\u2014',
        '{{student.guardian_contact_person}}':
            props.studentData.guardianContactPerson || '\u2014',
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

function updateTextProp(prop: string, value: any) {
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find(
            (e) => e.id === selectedElementId.value,
        );
        if (el && el.type === 'text') (el as any)[prop] = value;
    });
}

function updatePhotoProp(prop: string, value: any) {
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find(
            (e) => e.id === selectedElementId.value,
        );
        if (el && el.type === 'photo') (el as any)[prop] = value;
    });
}

function onKeyDown(e: KeyboardEvent) {
    if (editingTextId.value) {
        if (e.key === 'Escape') finishEditText();
        return;
    }
    if (e.key === 'Delete' || e.key === 'Backspace') {
        if (!selectedElementId.value) return;
        const target = e.target as HTMLElement;
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') return;
        e.preventDefault();
        deleteElement(selectedElementId.value);
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
        e.preventDefault();
        if (e.shiftKey) redo();
        else undo();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'y') {
        e.preventDefault();
        redo();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        if (selectedElementId.value) duplicateElement(selectedElementId.value);
    }
}

onMounted(() => {
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    window.addEventListener('keydown', onKeyDown);
});
onUnmounted(() => {
    window.removeEventListener('mousemove', onMouseMove);
    window.removeEventListener('mouseup', onMouseUp);
    window.removeEventListener('keydown', onKeyDown);
});
</script>

<template>
    <div class="space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-2">
            <div class="flex items-center gap-1.5">
                <Button
                    size="sm"
                    variant="outline"
                    :disabled="!canUndo"
                    @click="undo"
                >
                    <Undo2 class="mr-1 size-3.5" /> Undo
                </Button>
                <Button
                    size="sm"
                    variant="outline"
                    :disabled="!canRedo"
                    @click="redo"
                >
                    <Redo2 class="mr-1 size-3.5" /> Redo
                </Button>
                <Separator orientation="vertical" class="mx-1 h-6" />
                <Button
                    size="sm"
                    :variant="activeSide === 'front' ? 'default' : 'outline'"
                    @click="
                        activeSide = 'front';
                        selectedElementId = null;
                        editingTextId = null;
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
                        editingTextId = null;
                    "
                >
                    <ArrowLeftRight class="mr-1.5 size-3.5" /> Back
                </Button>
            </div>
            <div class="flex gap-1.5">
                <Button size="sm" variant="outline" @click="addTextElement">
                    <Type class="mr-1 size-3" /> Text
                </Button>
                <Button size="sm" variant="outline" @click="addPhotoElement">
                    <UserCircle class="mr-1 size-3" /> Photo
                </Button>
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

        <div class="grid gap-4 xl:grid-cols-[1fr_300px]">
            <div class="flex justify-center">
                <div
                    ref="canvasRef"
                    class="relative cursor-crosshair overflow-hidden rounded-lg shadow-2xl ring-1 ring-black/10 select-none"
                    :style="{
                        width: CARD_WIDTH + 'px',
                        height: CARD_HEIGHT + 'px',
                        ...getBackgroundStyle(currentSide.background),
                    }"
                    @click="onCanvasClick"
                >
                    <div
                        v-for="line in snapLines"
                        :key="line.type + line.pos"
                        class="pointer-events-none absolute z-50"
                        :style="
                            line.type === 'vertical'
                                ? {
                                      left: line.pos + '%',
                                      top: 0,
                                      bottom: 0,
                                      width: '1px',
                                      backgroundColor: '#3b82f6',
                                      opacity: '0.6',
                                  }
                                : {
                                      top: line.pos + '%',
                                      left: 0,
                                      right: 0,
                                      height: '1px',
                                      backgroundColor: '#3b82f6',
                                      opacity: '0.6',
                                  }
                        "
                    />

                    <div
                        v-for="el in currentSide.elements"
                        :key="el.id"
                        class="group absolute"
                        :class="{
                            'z-10': selectedElementId === el.id,
                            'z-0': selectedElementId !== el.id,
                        }"
                        :style="{
                            left: el.x + '%',
                            top: el.y + '%',
                            transform:
                                'translate(-50%, -50%)' +
                                (el.type === 'text' &&
                                'rotation' in el &&
                                el.rotation
                                    ? ` rotate(${el.rotation}deg)`
                                    : ''),
                        }"
                        @mousedown="onElementMouseDown($event, el.id)"
                        @dblclick.stop="
                            el.type === 'text'
                                ? startEditText(el.id)
                                : undefined
                        "
                    >
                        <div
                            v-if="el.type === 'photo'"
                            class="relative flex items-center justify-center overflow-hidden"
                            :class="
                                selectedElementId === el.id
                                    ? 'ring-2 ring-blue-500 ring-offset-1'
                                    : 'hover:ring-2 hover:ring-blue-300 hover:ring-offset-1'
                            "
                            :style="{
                                width: (el.width / 100) * CARD_WIDTH + 'px',
                                height: (el.height / 100) * CARD_HEIGHT + 'px',
                                borderRadius: el.borderRadius + 'px',
                                opacity: (el.opacity ?? 100) / 100,
                                border: el.borderWidth
                                    ? `${el.borderWidth}px solid ${el.borderColor}`
                                    : 'none',
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
                            <template v-if="selectedElementId === el.id">
                                <div
                                    class="absolute top-0 left-0 size-3 -translate-x-1/2 -translate-y-1/2 cursor-nw-resize rounded-full border-2 border-white bg-blue-500 shadow-lg transition-transform hover:scale-125"
                                    @mousedown.stop="
                                        onResizeMouseDown($event, el.id, 'nw')
                                    "
                                />
                                <div
                                    class="absolute top-0 right-0 size-3 translate-x-1/2 -translate-y-1/2 cursor-ne-resize rounded-full border-2 border-white bg-blue-500 shadow-lg transition-transform hover:scale-125"
                                    @mousedown.stop="
                                        onResizeMouseDown($event, el.id, 'ne')
                                    "
                                />
                                <div
                                    class="absolute bottom-0 left-0 size-3 -translate-x-1/2 translate-y-1/2 cursor-sw-resize rounded-full border-2 border-white bg-blue-500 shadow-lg transition-transform hover:scale-125"
                                    @mousedown.stop="
                                        onResizeMouseDown($event, el.id, 'sw')
                                    "
                                />
                                <div
                                    class="absolute right-0 bottom-0 size-3 translate-x-1/2 translate-y-1/2 cursor-se-resize rounded-full border-2 border-white bg-blue-500 shadow-lg transition-transform hover:scale-125"
                                    @mousedown.stop="
                                        onResizeMouseDown($event, el.id, 'se')
                                    "
                                />
                            </template>
                        </div>

                        <div
                            v-else-if="el.type === 'text'"
                            class="relative cursor-move rounded-sm transition-shadow"
                            :class="
                                selectedElementId === el.id
                                    ? 'shadow-lg ring-2 ring-blue-500 ring-offset-1'
                                    : 'hover:ring-1 hover:ring-blue-300'
                            "
                            :style="{
                                fontSize: el.fontSize + 'px',
                                fontWeight: el.fontWeight,
                                color: el.color,
                                textAlign: el.textAlign,
                                textTransform: el.textTransform as any,
                                letterSpacing: el.letterSpacing + 'px',
                                lineHeight: el.lineHeight,
                                opacity: (el.opacity ?? 100) / 100,
                                whiteSpace: 'nowrap',
                                minWidth: '20px',
                                padding: '2px 4px',
                            }"
                        >
                            <div
                                v-if="editingTextId === el.id"
                                ref="editTextRef"
                                contenteditable="true"
                                class="min-w-[30px] rounded-sm ring-2 ring-blue-400 outline-none"
                                :style="{
                                    fontSize: el.fontSize + 'px',
                                    fontWeight: el.fontWeight,
                                    color: el.color,
                                    textAlign: el.textAlign,
                                    textTransform: el.textTransform as any,
                                    letterSpacing: el.letterSpacing + 'px',
                                    lineHeight: el.lineHeight,
                                    whiteSpace: 'nowrap',
                                    background: 'rgba(0,0,0,0.2)',
                                    padding: '2px 6px',
                                }"
                                @blur="onEditTextBlur"
                                @input="onEditTextInput"
                                @keydown.enter.prevent="finishEditText"
                                v-text="el.content"
                            />
                            <template v-else>
                                {{ resolveContent(el.content) }}
                            </template>

                            <div
                                v-if="
                                    selectedElementId === el.id &&
                                    editingTextId !== el.id
                                "
                                class="pointer-events-none absolute -top-1 left-1/2 -translate-x-1/2 -translate-y-full rounded bg-blue-500 px-1.5 py-0.5 text-[9px] whitespace-nowrap text-white shadow"
                            >
                                {{ el.fontSize }}px &middot; {{ el.fontWeight }}
                            </div>
                        </div>
                    </div>

                    <div
                        v-if="!currentSide.elements.length"
                        class="absolute inset-0 flex flex-col items-center justify-center gap-2 text-white/40"
                    >
                        <MousePointerClick class="size-8" />
                        <span class="text-xs"
                            >Add elements from the toolbar</span
                        >
                    </div>
                </div>
            </div>

            <div class="space-y-3">
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
                            <label
                                class="inline-flex flex-1 cursor-pointer items-center justify-center gap-1.5 rounded-md border px-3 py-1.5 text-sm font-medium ring-offset-background transition-colors"
                                :class="
                                    currentSide.background.type === 'image'
                                        ? 'bg-primary text-primary-foreground'
                                        : 'hover:bg-accent hover:text-accent-foreground'
                                "
                            >
                                <ImagePlus class="size-3" /> Image
                                <input
                                    type="file"
                                    accept="image/*"
                                    class="hidden"
                                    @change="onBackgroundImageUpload"
                                />
                            </label>
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
                                    class="size-8 cursor-pointer rounded border"
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
                                    class="h-8 flex-1 font-mono text-xs"
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
                                    class="size-8 cursor-pointer rounded border"
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
                                    class="h-8 flex-1 font-mono text-xs"
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
                                    class="size-8 cursor-pointer rounded border"
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
                                    class="h-8 flex-1 font-mono text-xs"
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
                        <div
                            v-if="
                                currentSide.background.type === 'image' &&
                                currentSide.background.imageBase64
                            "
                            class="space-y-2"
                        >
                            <div class="flex items-center gap-2">
                                <div
                                    class="size-12 overflow-hidden rounded border"
                                >
                                    <img
                                        :src="
                                            currentSide.background.imageBase64!
                                        "
                                        class="size-full object-cover"
                                    />
                                </div>
                                <Button
                                    size="sm"
                                    variant="destructive"
                                    @click="
                                        updateConfig((c) => {
                                            c[
                                                activeSide
                                            ].background.imageBase64 = null;
                                            c[activeSide].background.type =
                                                'solid';
                                        })
                                    "
                                >
                                    <Trash2 class="mr-1 size-3" /> Remove
                                </Button>
                            </div>
                        </div>
                        <div
                            v-if="
                                currentSide.background.type === 'image' &&
                                !currentSide.background.imageBase64
                            "
                        >
                            <p class="text-xs text-muted-foreground">
                                Upload an image using the toolbar or the Image
                                button above.
                            </p>
                        </div>
                    </CardContent>
                </Card>

                <Card v-if="selectedTextElement">
                    <CardHeader class="pb-3">
                        <div class="flex items-center justify-between">
                            <CardTitle
                                class="flex items-center gap-1.5 text-sm"
                            >
                                <Type class="size-3.5" />
                                Text Properties
                            </CardTitle>
                            <div class="flex items-center gap-1">
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-6"
                                    title="Duplicate"
                                    @click="
                                        duplicateElement(selectedElementId!)
                                    "
                                    ><Copy class="size-3"
                                /></Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-6"
                                    title="Move Up"
                                    @click="
                                        moveElementOrder(
                                            selectedElementId!,
                                            'up',
                                        )
                                    "
                                    ><ChevronUp class="size-3"
                                /></Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-6"
                                    title="Move Down"
                                    @click="
                                        moveElementOrder(
                                            selectedElementId!,
                                            'down',
                                        )
                                    "
                                    ><ChevronDown class="size-3"
                                /></Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-6 text-destructive"
                                    @click="deleteElement(selectedElementId!)"
                                    ><Trash2 class="size-3"
                                /></Button>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-3">
                        <div class="space-y-1.5">
                            <Label class="text-xs">Content</Label>
                            <Input
                                :value="selectedTextElement.content"
                                @input="
                                    updateTextProp(
                                        'content',
                                        ($event.target as HTMLInputElement)
                                            .value,
                                    )
                                "
                            />
                            <div class="flex flex-wrap gap-1">
                                <button
                                    v-for="field in DYNAMIC_FIELDS"
                                    :key="field.value"
                                    class="rounded-md border px-1.5 py-0.5 text-[10px] transition-colors hover:bg-primary hover:text-primary-foreground"
                                    :class="
                                        selectedTextElement.content ===
                                        field.value
                                            ? 'bg-primary text-primary-foreground'
                                            : ''
                                    "
                                    @click="insertField(field.value)"
                                >
                                    {{ field.label }}
                                </button>
                            </div>
                        </div>

                        <Separator />

                        <div class="space-y-1.5">
                            <Label class="text-xs font-medium"
                                >Typography</Label
                            >
                            <div class="grid grid-cols-2 gap-2">
                                <div class="space-y-1">
                                    <Label
                                        class="text-[10px] text-muted-foreground"
                                        >Size:
                                        {{
                                            selectedTextElement.fontSize
                                        }}px</Label
                                    >
                                    <input
                                        type="range"
                                        min="4"
                                        max="32"
                                        :value="selectedTextElement.fontSize"
                                        @input="
                                            updateTextProp(
                                                'fontSize',
                                                parseInt(
                                                    (
                                                        $event.target as HTMLInputElement
                                                    ).value,
                                                ),
                                            )
                                        "
                                        class="w-full"
                                    />
                                </div>
                                <div class="space-y-1">
                                    <Label
                                        class="text-[10px] text-muted-foreground"
                                        >Color</Label
                                    >
                                    <div class="flex items-center gap-1.5">
                                        <input
                                            type="color"
                                            :value="selectedTextElement.color"
                                            @input="
                                                updateTextProp(
                                                    'color',
                                                    (
                                                        $event.target as HTMLInputElement
                                                    ).value,
                                                )
                                            "
                                            class="size-7 cursor-pointer rounded border"
                                        />
                                        <Input
                                            :value="selectedTextElement.color"
                                            @input="
                                                updateTextProp(
                                                    'color',
                                                    (
                                                        $event.target as HTMLInputElement
                                                    ).value,
                                                )
                                            "
                                            class="h-7 flex-1 font-mono text-[10px]"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="space-y-1.5">
                            <Label class="text-[10px] text-muted-foreground"
                                >Alignment &amp; Style</Label
                            >
                            <div class="flex gap-1">
                                <Button
                                    size="sm"
                                    :variant="
                                        selectedTextElement.fontWeight ===
                                        'bold'
                                            ? 'default'
                                            : 'outline'
                                    "
                                    class="flex-1"
                                    @click="
                                        updateTextProp(
                                            'fontWeight',
                                            selectedTextElement.fontWeight ===
                                                'bold'
                                                ? 'normal'
                                                : 'bold',
                                        )
                                    "
                                >
                                    <Bold class="mr-1 size-3" />
                                </Button>
                                <Button
                                    size="sm"
                                    :variant="
                                        selectedTextElement.textAlign === 'left'
                                            ? 'default'
                                            : 'outline'
                                    "
                                    class="flex-1"
                                    @click="updateTextProp('textAlign', 'left')"
                                >
                                    <AlignLeft class="size-3" />
                                </Button>
                                <Button
                                    size="sm"
                                    :variant="
                                        selectedTextElement.textAlign ===
                                        'center'
                                            ? 'default'
                                            : 'outline'
                                    "
                                    class="flex-1"
                                    @click="
                                        updateTextProp('textAlign', 'center')
                                    "
                                >
                                    <AlignCenter class="size-3" />
                                </Button>
                                <Button
                                    size="sm"
                                    :variant="
                                        selectedTextElement.textAlign ===
                                        'right'
                                            ? 'default'
                                            : 'outline'
                                    "
                                    class="flex-1"
                                    @click="
                                        updateTextProp('textAlign', 'right')
                                    "
                                >
                                    <AlignRight class="size-3" />
                                </Button>
                            </div>
                            <div class="flex gap-1">
                                <Button
                                    size="sm"
                                    :variant="
                                        selectedTextElement.textTransform ===
                                        'none'
                                            ? 'default'
                                            : 'outline'
                                    "
                                    class="flex-1"
                                    @click="
                                        updateTextProp('textTransform', 'none')
                                    "
                                >
                                    <CaseSensitive class="mr-1 size-3" /> Aa
                                </Button>
                                <Button
                                    size="sm"
                                    :variant="
                                        selectedTextElement.textTransform ===
                                        'uppercase'
                                            ? 'default'
                                            : 'outline'
                                    "
                                    class="flex-1"
                                    @click="
                                        updateTextProp(
                                            'textTransform',
                                            'uppercase',
                                        )
                                    "
                                >
                                    AA
                                </Button>
                            </div>
                        </div>

                        <Separator />

                        <div class="grid grid-cols-2 gap-2">
                            <div class="space-y-1">
                                <Label class="text-[10px] text-muted-foreground"
                                    >Spacing:
                                    {{
                                        selectedTextElement.letterSpacing ?? 0
                                    }}px</Label
                                >
                                <input
                                    type="range"
                                    min="-2"
                                    max="8"
                                    step="0.5"
                                    :value="
                                        selectedTextElement.letterSpacing ?? 0
                                    "
                                    @input="
                                        updateTextProp(
                                            'letterSpacing',
                                            parseFloat(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            ),
                                        )
                                    "
                                    class="w-full"
                                />
                            </div>
                            <div class="space-y-1">
                                <Label class="text-[10px] text-muted-foreground"
                                    >Line Height:
                                    {{
                                        (
                                            selectedTextElement.lineHeight ??
                                            1.2
                                        ).toFixed(1)
                                    }}</Label
                                >
                                <input
                                    type="range"
                                    min="0.8"
                                    max="2"
                                    step="0.1"
                                    :value="
                                        selectedTextElement.lineHeight ?? 1.2
                                    "
                                    @input="
                                        updateTextProp(
                                            'lineHeight',
                                            parseFloat(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            ),
                                        )
                                    "
                                    class="w-full"
                                />
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-2">
                            <div class="space-y-1">
                                <Label class="text-[10px] text-muted-foreground"
                                    >Opacity:
                                    {{
                                        selectedTextElement.opacity ?? 100
                                    }}%</Label
                                >
                                <input
                                    type="range"
                                    min="10"
                                    max="100"
                                    step="5"
                                    :value="selectedTextElement.opacity ?? 100"
                                    @input="
                                        updateTextProp(
                                            'opacity',
                                            parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            ),
                                        )
                                    "
                                    class="w-full"
                                />
                            </div>
                            <div class="space-y-1">
                                <Label class="text-[10px] text-muted-foreground"
                                    >Rotation:
                                    {{
                                        selectedTextElement.rotation ?? 0
                                    }}&deg;</Label
                                >
                                <input
                                    type="range"
                                    min="-180"
                                    max="180"
                                    :value="selectedTextElement.rotation ?? 0"
                                    @input="
                                        updateTextProp(
                                            'rotation',
                                            parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            ),
                                        )
                                    "
                                    class="w-full"
                                />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card v-else-if="selectedPhotoElement">
                    <CardHeader class="pb-3">
                        <div class="flex items-center justify-between">
                            <CardTitle
                                class="flex items-center gap-1.5 text-sm"
                            >
                                <UserCircle class="size-3.5" />
                                Photo Properties
                            </CardTitle>
                            <div class="flex items-center gap-1">
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-6"
                                    title="Duplicate"
                                    @click="
                                        duplicateElement(selectedElementId!)
                                    "
                                    ><Copy class="size-3"
                                /></Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-6"
                                    title="Move Up"
                                    @click="
                                        moveElementOrder(
                                            selectedElementId!,
                                            'up',
                                        )
                                    "
                                    ><ChevronUp class="size-3"
                                /></Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-6"
                                    title="Move Down"
                                    @click="
                                        moveElementOrder(
                                            selectedElementId!,
                                            'down',
                                        )
                                    "
                                    ><ChevronDown class="size-3"
                                /></Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    class="size-6 text-destructive"
                                    @click="deleteElement(selectedElementId!)"
                                    ><Trash2 class="size-3"
                                /></Button>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent class="space-y-3">
                        <div class="grid grid-cols-2 gap-2">
                            <div class="space-y-1">
                                <Label class="text-xs"
                                    >Width:
                                    {{ selectedPhotoElement.width }}%</Label
                                >
                                <input
                                    type="range"
                                    min="5"
                                    max="50"
                                    :value="selectedPhotoElement.width"
                                    @input="
                                        updatePhotoProp(
                                            'width',
                                            parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            ),
                                        )
                                    "
                                    class="w-full"
                                />
                            </div>
                            <div class="space-y-1">
                                <Label class="text-xs"
                                    >Height:
                                    {{ selectedPhotoElement.height }}%</Label
                                >
                                <input
                                    type="range"
                                    min="5"
                                    max="50"
                                    :value="selectedPhotoElement.height"
                                    @input="
                                        updatePhotoProp(
                                            'height',
                                            parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            ),
                                        )
                                    "
                                    class="w-full"
                                />
                            </div>
                        </div>
                        <div class="space-y-1">
                            <Label class="text-xs"
                                >Corner Radius:
                                {{ selectedPhotoElement.borderRadius }}px</Label
                            >
                            <input
                                type="range"
                                min="0"
                                max="50"
                                :value="selectedPhotoElement.borderRadius"
                                @input="
                                    updatePhotoProp(
                                        'borderRadius',
                                        parseInt(
                                            ($event.target as HTMLInputElement)
                                                .value,
                                        ),
                                    )
                                "
                                class="w-full"
                            />
                        </div>
                        <div class="grid grid-cols-2 gap-2">
                            <div class="space-y-1">
                                <Label class="text-xs"
                                    >Opacity:
                                    {{
                                        selectedPhotoElement.opacity ?? 100
                                    }}%</Label
                                >
                                <input
                                    type="range"
                                    min="10"
                                    max="100"
                                    step="5"
                                    :value="selectedPhotoElement.opacity ?? 100"
                                    @input="
                                        updatePhotoProp(
                                            'opacity',
                                            parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            ),
                                        )
                                    "
                                    class="w-full"
                                />
                            </div>
                            <div class="space-y-1">
                                <Label class="text-xs"
                                    >Border:
                                    {{
                                        selectedPhotoElement.borderWidth ?? 0
                                    }}px</Label
                                >
                                <input
                                    type="range"
                                    min="0"
                                    max="5"
                                    :value="
                                        selectedPhotoElement.borderWidth ?? 0
                                    "
                                    @input="
                                        updatePhotoProp(
                                            'borderWidth',
                                            parseInt(
                                                (
                                                    $event.target as HTMLInputElement
                                                ).value,
                                            ),
                                        )
                                    "
                                    class="w-full"
                                />
                            </div>
                        </div>
                        <div class="space-y-1">
                            <Label class="text-xs">Border Color</Label>
                            <div class="flex items-center gap-1.5">
                                <input
                                    type="color"
                                    :value="
                                        selectedPhotoElement.borderColor ??
                                        '#ffffff33'
                                    "
                                    @input="
                                        updatePhotoProp(
                                            'borderColor',
                                            ($event.target as HTMLInputElement)
                                                .value,
                                        )
                                    "
                                    class="size-7 cursor-pointer rounded border"
                                />
                                <Input
                                    :value="
                                        selectedPhotoElement.borderColor ??
                                        '#ffffff33'
                                    "
                                    @input="
                                        updatePhotoProp(
                                            'borderColor',
                                            ($event.target as HTMLInputElement)
                                                .value,
                                        )
                                    "
                                    class="h-7 flex-1 font-mono text-xs"
                                />
                            </div>
                        </div>
                        <p class="text-[10px] text-muted-foreground">
                            Drag corner handles to resize. Double-click text to
                            edit inline.
                        </p>
                    </CardContent>
                </Card>

                <Card v-else>
                    <CardHeader class="pb-3">
                        <CardTitle class="flex items-center gap-1.5 text-sm">
                            <Maximize2 class="size-3.5 text-muted-foreground" />
                            Elements
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p class="mb-2 text-xs text-muted-foreground">
                            Click to select &middot; Double-click text to edit
                            &middot; Delete to remove &middot; Ctrl+D to
                            duplicate
                        </p>
                        <div class="max-h-56 space-y-1 overflow-y-auto">
                            <div
                                v-for="el in currentSide.elements"
                                :key="el.id"
                                class="flex cursor-pointer items-center justify-between rounded-md px-2 py-1.5 text-xs transition-colors hover:bg-accent"
                                :class="{
                                    'bg-accent': selectedElementId === el.id,
                                }"
                                @click="selectedElementId = el.id"
                                @dblclick="
                                    el.type === 'text'
                                        ? startEditText(el.id)
                                        : undefined
                                "
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
                                <div class="flex items-center gap-0.5">
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        class="size-5"
                                        title="Duplicate"
                                        @click.stop="duplicateElement(el.id)"
                                    >
                                        <Copy class="size-2.5" />
                                    </Button>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        class="size-5 text-destructive"
                                        @click.stop="deleteElement(el.id)"
                                    >
                                        <Trash2 class="size-2.5" />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    </div>
</template>
