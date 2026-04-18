import json

content = """<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
    Trash2,
    ImagePlus,
    Type,
    UserCircle,
    ArrowLeftRight,
    Undo2,
    Redo2,
    Bold,
    AlignLeft,
    AlignCenter,
    AlignRight,
    CaseSensitive,
    Copy,
    MousePointerClick,
    Square,
    Circle,
    Minus,
    QrCode,
    ZoomIn,
    ZoomOut,
    MoveUp,
    MoveDown,
    Settings2,
    AlignJustify
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
    fontFamily: string;
    fontWeight: 'normal' | 'bold';
    color: string;
    textAlign: 'left' | 'center' | 'right' | 'justify';
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
    rotation: number;
};

type ShapeElement = {
    id: string;
    type: 'shape';
    shapeType: 'rectangle' | 'circle' | 'line';
    x: number;
    y: number;
    width: number;
    height: number;
    backgroundColor: string;
    borderColor: string;
    borderWidth: number;
    borderRadius: number;
    opacity: number;
    rotation: number;
};

type QrElement = {
    id: string;
    type: 'qr';
    content: string;
    x: number;
    y: number;
    size: number;
    color: string;
    backgroundColor: string;
    opacity: number;
    rotation: number;
};

type TemplateElement = TextElement | PhotoElement | ShapeElement | QrElement;

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

const FONTS = [
    'Inter',
    'Arial',
    'Helvetica',
    'Times New Roman',
    'Courier New',
    'Verdana',
    'Georgia',
    'Palatino',
    'Garamond',
    'Bookman',
    'Comic Sans MS',
    'Trebuchet MS',
    'Arial Black',
    'Impact'
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
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0, elX: 0, elY: 0, size: 0 });
const canvasRef = ref<HTMLElement | null>(null);
const editingTextId = ref<string | null>(null);
const editTextRef = ref<HTMLElement | null>(null);
const snapLines = ref<{ type: 'vertical' | 'horizontal'; pos: number }[]>([]);
const zoom = ref(100);

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

function zoomIn() { zoom.value = Math.min(zoom.value + 10, 250); }
function zoomOut() { zoom.value = Math.max(zoom.value - 10, 30); }

function getDefaultConfig(): TemplateConfig {
    return {
        front: {
            background: { type: 'solid', solidColor: '#1e3a5f', gradientStart: '#1e3a5f', gradientEnd: '#2d5a87', gradientAngle: '135', imageBase64: null },
            elements: [
                { id: 'el-1', type: 'text', content: '{{school_name}}', x: 50, y: 12, fontSize: 18, fontFamily: 'Inter', fontWeight: 'bold', color: '#ffffff', textAlign: 'center', textTransform: 'uppercase', letterSpacing: 0, lineHeight: 1.2, opacity: 100, rotation: 0 },
                { id: 'el-2', type: 'text', content: 'Student Identification Card', x: 50, y: 18, fontSize: 10, fontFamily: 'Inter', fontWeight: 'normal', color: '#ffffff', textAlign: 'center', textTransform: 'none', letterSpacing: 0, lineHeight: 1.2, opacity: 100, rotation: 0 },
                { id: 'el-3', type: 'photo', x: 50, y: 42, width: 35, height: 30, borderRadius: 6, opacity: 100, borderColor: '#ffffff33', borderWidth: 1, rotation: 0 },
                { id: 'el-4', type: 'text', content: '{{student.name}}', x: 50, y: 68, fontSize: 20, fontFamily: 'Inter', fontWeight: 'bold', color: '#ffffff', textAlign: 'center', textTransform: 'none', letterSpacing: 0.5, lineHeight: 1.2, opacity: 100, rotation: 0 },
                { id: 'el-5', type: 'text', content: '{{student.course}}', x: 50, y: 76, fontSize: 14, fontFamily: 'Inter', fontWeight: 'normal', color: '#ffffffcc', textAlign: 'center', textTransform: 'none', letterSpacing: 0, lineHeight: 1.2, opacity: 100, rotation: 0 },
                { id: 'el-6', type: 'text', content: '{{student.student_id_number}}', x: 50, y: 85, fontSize: 14, fontFamily: 'Inter', fontWeight: 'bold', color: '#ffffff', textAlign: 'center', textTransform: 'none', letterSpacing: 1, lineHeight: 1.2, opacity: 100, rotation: 0 },
            ],
        },
        back: {
            background: { type: 'solid', solidColor: '#f8f9fa', gradientStart: '#f8f9fa', gradientEnd: '#e9ecef', gradientAngle: '135', imageBase64: null },
            elements: [
                { id: 'el-b1', type: 'text', content: '{{school_name}}', x: 50, y: 15, fontSize: 16, fontFamily: 'Inter', fontWeight: 'bold', color: '#333333', textAlign: 'center', textTransform: 'uppercase', letterSpacing: 0, lineHeight: 1.2, opacity: 100, rotation: 0 },
                { id: 'el-b2', type: 'text', content: 'Emergency Contact', x: 50, y: 22, fontSize: 10, fontFamily: 'Inter', fontWeight: 'normal', color: '#888888', textAlign: 'center', textTransform: 'none', letterSpacing: 0, lineHeight: 1.2, opacity: 100, rotation: 0 },
                { id: 'el-b4', type: 'text', content: '{{student.contact_number}}', x: 50, y: 48, fontSize: 18, fontFamily: 'Inter', fontWeight: 'bold', color: '#333333', textAlign: 'center', textTransform: 'none', letterSpacing: 0, lineHeight: 1.2, opacity: 100, rotation: 0 },
                { id: 'el-b6', type: 'text', content: '{{student.guardian_contact_person}}', x: 50, y: 68, fontSize: 18, fontFamily: 'Inter', fontWeight: 'bold', color: '#333333', textAlign: 'center', textTransform: 'none', letterSpacing: 0, lineHeight: 1.2, opacity: 100, rotation: 0 },
                { id: 'el-b7', type: 'qr', content: '{{student.student_id_number}}', x: 50, y: 88, size: 15, color: '#000000', backgroundColor: '#ffffff', opacity: 100, rotation: 0 },
            ],
        },
    };
}

function updateConfig(updater: (c: TemplateConfig) => void) {
    const newConfig = JSON.parse(JSON.stringify(config.value)) as TemplateConfig;
    updater(newConfig);
    emit('update:modelValue', newConfig);
}

const currentSide = computed(() => config.value[activeSide.value]);
const selectedElement = computed(() => {
    if (!selectedElementId.value) return null;
    return currentSide.value.elements.find((e) => e.id === selectedElementId.value) ?? null;
});

function addTextElement() {
    const id = `el-${Date.now()}`;
    updateConfig((c) => {
        c[activeSide.value].elements.push({ id, type: 'text', content: 'New Text', x: 50, y: 50, fontSize: 16, fontFamily: 'Inter', fontWeight: 'normal', color: activeSide.value === 'front' ? '#ffffff' : '#333333', textAlign: 'center', textTransform: 'none', letterSpacing: 0, lineHeight: 1.2, opacity: 100, rotation: 0 });
    });
    selectedElementId.value = id;
}

function addPhotoElement() {
    const id = `el-${Date.now()}`;
    updateConfig((c) => {
        c[activeSide.value].elements.push({ id, type: 'photo', x: 50, y: 50, width: 35, height: 30, borderRadius: 6, opacity: 100, borderColor: '#ffffff33', borderWidth: 1, rotation: 0 });
    });
    selectedElementId.value = id;
}

function addShapeElement(shapeType: 'rectangle' | 'circle' | 'line') {
    const id = `el-${Date.now()}`;
    updateConfig((c) => {
        c[activeSide.value].elements.push({ id, type: 'shape', shapeType, x: 50, y: 50, width: 30, height: shapeType === 'line' ? 1 : 30, backgroundColor: shapeType === 'line' ? '#000000' : '#3b82f6', borderColor: '#000000', borderWidth: 0, borderRadius: shapeType === 'circle' ? 50 : 0, opacity: 100, rotation: 0 });
    });
    selectedElementId.value = id;
}

function addQrElement() {
    const id = `el-${Date.now()}`;
    updateConfig((c) => {
        c[activeSide.value].elements.push({ id, type: 'qr', content: '{{student.student_id_number}}', x: 50, y: 50, size: 20, color: '#000000', backgroundColor: '#ffffff', opacity: 100, rotation: 0 });
    });
    selectedElementId.value = id;
}

function duplicateElement(id: string) {
    const newId = `el-${Date.now()}`;
    updateConfig((c) => {
        const src = c[activeSide.value].elements.find((e) => e.id === id);
        if (!src) return;
        const clone = JSON.parse(JSON.stringify(src));
        clone.id = newId;
        clone.x = Math.min(95, clone.x + 3);
        clone.y = Math.min(95, clone.y + 3);
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
        c[activeSide.value].elements = c[activeSide.value].elements.filter((e) => e.id !== id);
    });
    if (selectedElementId.value === id) selectedElementId.value = null;
    if (editingTextId.value === id) editingTextId.value = null;
}

function onCanvasClick() {
    selectedElementId.value = null;
    editingTextId.value = null;
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
    const text = editTextRef.value.innerText || editTextRef.value.textContent || '';
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find((e) => e.id === editingTextId.value);
        if (el && el.type === 'text') el.content = text;
    });
    editingTextId.value = null;
}

function onEditTextBlur() { finishEditText(); }
function onEditTextInput(e: Event) {
    const target = e.target as HTMLElement;
    const text = target.innerText || target.textContent || '';
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find((e) => e.id === editingTextId.value);
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
    if (!el) return;
    resizeStart.value = {
        x: e.clientX,
        y: e.clientY,
        width: (el as any).width || 0,
        height: (el as any).height || 0,
        size: (el as any).size || 0,
        elX: el.x,
        elY: el.y,
    };
}

function computeSnap(newPos: number, axis: 'x' | 'y'): number {
    const guides = [10, 25, 50, 75, 90];
    const threshold = 1.5;
    for (const g of guides) {
        if (Math.abs(newPos - g) < threshold) {
            snapLines.value = [{ type: axis === 'x' ? 'vertical' : 'horizontal', pos: g }];
            return g;
        }
    }
    snapLines.value = [];
    return newPos;
}

function onMouseMove(e: MouseEvent) {
    if (isResizing.value && selectedElementId.value && resizeHandle.value && canvasRef.value) {
        const canvasRect = canvasRef.value.getBoundingClientRect();
        // Adjust for zoom level
        const zoomFactor = zoom.value / 100;
        const dx = (e.clientX - resizeStart.value.x) / zoomFactor;
        const dy = (e.clientY - resizeStart.value.y) / zoomFactor;
        
        const dwPct = (dx / (CARD_WIDTH)) * 100;
        const dhPct = (dy / (CARD_HEIGHT)) * 100;

        updateConfig((c) => {
            const el = c[activeSide.value].elements.find((e2) => e2.id === selectedElementId.value);
            if (!el) return;

            if (el.type === 'qr') {
                if (resizeHandle.value === 'se') {
                    const newSize = Math.max(MIN_SIZE, Math.min(80, resizeStart.value.size + Math.max(dwPct, dhPct)));
                    el.size = newSize;
                }
                return;
            }

            if (el.type === 'photo' || el.type === 'shape') {
                if (resizeHandle.value === 'se') {
                    el.width = Math.max(MIN_SIZE, Math.min(100, resizeStart.value.width + dwPct));
                    el.height = Math.max(MIN_SIZE, Math.min(100, resizeStart.value.height + dhPct));
                } else if (resizeHandle.value === 'sw') {
                    const newWidth = Math.max(MIN_SIZE, Math.min(100, resizeStart.value.width - dwPct));
                    const widthDiff = newWidth - resizeStart.value.width;
                    el.width = newWidth;
                    el.x = Math.max(0, Math.min(100, resizeStart.value.elX - widthDiff / 2));
                    el.height = Math.max(MIN_SIZE, Math.min(100, resizeStart.value.height + dhPct));
                } else if (resizeHandle.value === 'ne') {
                    const newHeight = Math.max(MIN_SIZE, Math.min(100, resizeStart.value.height - dhPct));
                    const heightDiff = newHeight - resizeStart.value.height;
                    el.width = Math.max(MIN_SIZE, Math.min(100, resizeStart.value.width + dwPct));
                    el.height = newHeight;
                    el.y = Math.max(0, Math.min(100, resizeStart.value.elY - heightDiff / 2));
                } else if (resizeHandle.value === 'nw') {
                    const newWidth = Math.max(MIN_SIZE, Math.min(100, resizeStart.value.width - dwPct));
                    const newHeight = Math.max(MIN_SIZE, Math.min(100, resizeStart.value.height - dhPct));
                    const widthDiff = newWidth - resizeStart.value.width;
                    const heightDiff = newHeight - resizeStart.value.height;
                    el.width = newWidth;
                    el.height = newHeight;
                    el.x = Math.max(0, Math.min(100, resizeStart.value.elX - widthDiff / 2));
                    el.y = Math.max(0, Math.min(100, resizeStart.value.elY - heightDiff / 2));
                }
            }
        });
        return;
    }

    if (!isDragging.value || !selectedElementId.value || !canvasRef.value) return;
    
    const canvasRect = canvasRef.value.getBoundingClientRect();
    const rawX = ((e.clientX - dragOffset.value.x) / canvasRect.width) * 100;
    const rawY = ((e.clientY - dragOffset.value.y) / canvasRect.height) * 100;
    
    const newX = computeSnap(Math.max(0, Math.min(100, rawX)), 'x');
    const newY = computeSnap(Math.max(0, Math.min(100, rawY)), 'y');
    
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find((e2) => e2.id === selectedElementId.value);
        if (el) { el.x = newX; el.y = newY; }
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

function resolveContent(content: string): string {
    const map: Record<string, string> = {
        '{{student.name}}': props.studentData?.name || 'Student Name',
        '{{student.course}}': props.studentData?.course || 'Course',
        '{{student.student_id_number}}': props.studentData?.studentIdNumber || '1000',
        '{{student.contact_number}}': props.studentData?.contactNumber || '\u2014',
        '{{student.guardian_contact_person}}': props.studentData?.guardianContactPerson || '\u2014',
        '{{school_name}}': 'DCCP',
    };
    return map[content] ?? content;
}

function getBackgroundStyle(bg: Background): Record<string, string> {
    if (bg.type === 'gradient')
        return { background: `linear-gradient(${bg.gradientAngle || 135}deg, ${bg.gradientStart || '#667eea'}, ${bg.gradientEnd || '#764ba2'})` };
    if (bg.type === 'image' && bg.imageBase64)
        return { backgroundImage: `url(${bg.imageBase64})`, backgroundSize: 'cover', backgroundPosition: 'center' };
    return { backgroundColor: bg.solidColor || '#1e3a5f' };
}

function updateSelectedProp(prop: string, value: any) {
    if (!selectedElementId.value) return;
    updateConfig((c) => {
        const el = c[activeSide.value].elements.find((e) => e.id === selectedElementId.value);
        if (el) (el as any)[prop] = value;
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
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.tagName === 'SELECT') return;
        e.preventDefault();
        deleteElement(selectedElementId.value);
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
        e.preventDefault();
        if (e.shiftKey) redo();
        else undo();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'y') { e.preventDefault(); redo(); }
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
  <div class="flex flex-col h-[800px] border rounded-xl overflow-hidden bg-background shadow-xl font-sans">
    <!-- Top Bar -->
    <div class="h-14 border-b flex items-center justify-between px-4 bg-muted/20">
      <div class="flex items-center space-x-2">
        <Button variant="ghost" size="sm" :disabled="!canUndo" @click="undo"><Undo2 class="w-4 h-4 mr-1.5" /> Undo</Button>
        <Button variant="ghost" size="sm" :disabled="!canRedo" @click="redo"><Redo2 class="w-4 h-4 mr-1.5" /> Redo</Button>
        <Separator orientation="vertical" class="h-6 mx-2" />
        <Button variant="ghost" size="sm" @click="activeSide = 'front'" :class="{ 'bg-primary/10 text-primary': activeSide === 'front' }">Front</Button>
        <Button variant="ghost" size="sm" @click="activeSide = 'back'" :class="{ 'bg-primary/10 text-primary': activeSide === 'back' }">Back</Button>
      </div>
      <div class="flex items-center space-x-2">
        <Button variant="outline" size="sm" @click="addTextElement"><Type class="w-4 h-4 mr-1.5" /> Text</Button>
        <Button variant="outline" size="sm" @click="addPhotoElement"><ImagePlus class="w-4 h-4 mr-1.5" /> Photo</Button>
        <Button variant="outline" size="sm" @click="addShapeElement('rectangle')"><Square class="w-4 h-4 mr-1.5" /> Shape</Button>
        <Button variant="outline" size="sm" @click="addQrElement"><QrCode class="w-4 h-4 mr-1.5" /> QR</Button>
      </div>
    </div>

    <!-- Main Workspace -->
    <div class="flex flex-1 overflow-hidden">
      
      <!-- Left Sidebar: Layers & Background -->
      <div class="w-72 border-r flex flex-col bg-muted/5 z-10">
        <Tabs defaultValue="layers" class="flex-1 flex flex-col">
          <TabsList class="w-full justify-start rounded-none border-b h-12 px-0 bg-transparent">
            <TabsTrigger value="layers" class="flex-1 data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none h-12">
              <Layers class="w-4 h-4 mr-2" /> Layers
            </TabsTrigger>
            <TabsTrigger value="background" class="flex-1 data-[state=active]:bg-transparent data-[state=active]:shadow-none data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none h-12">
              <Palette class="w-4 h-4 mr-2" /> Background
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="layers" class="flex-1 overflow-y-auto p-3 m-0 space-y-1">
             <div v-for="el in currentSide.elements.slice().reverse()" :key="el.id" 
                  class="flex cursor-pointer items-center justify-between rounded-md px-2 py-2 text-sm transition-colors hover:bg-accent border border-transparent"
                  :class="{ 'bg-accent border-border': selectedElementId === el.id }"
                  @click="selectedElementId = el.id"
                  @dblclick="el.type === 'text' ? startEditText(el.id) : undefined">
                <span class="flex items-center gap-2 truncate">
                    <Type v-if="el.type === 'text'" class="size-4 text-muted-foreground" />
                    <UserCircle v-else-if="el.type === 'photo'" class="size-4 text-muted-foreground" />
                    <Square v-else-if="el.type === 'shape' && el.shapeType === 'rectangle'" class="size-4 text-muted-foreground" />
                    <Circle v-else-if="el.type === 'shape' && el.shapeType === 'circle'" class="size-4 text-muted-foreground" />
                    <Minus v-else-if="el.type === 'shape' && el.shapeType === 'line'" class="size-4 text-muted-foreground" />
                    <QrCode v-else-if="el.type === 'qr'" class="size-4 text-muted-foreground" />
                    
                    <span class="truncate max-w-[140px]">
                      {{ el.type === 'photo' ? 'Photo' : 
                         el.type === 'shape' ? 'Shape (' + el.shapeType + ')' :
                         el.type === 'qr' ? 'QR Code' :
                         (el.content.length > 20 ? resolveContent(el.content).substring(0, 20) + '...' : resolveContent(el.content)) }}
                    </span>
                </span>
             </div>
             <div v-if="currentSide.elements.length === 0" class="text-center text-xs text-muted-foreground py-8">
                No elements on this side
             </div>
          </TabsContent>
          
          <TabsContent value="background" class="flex-1 overflow-y-auto p-4 m-0 space-y-5">
             <div class="flex bg-muted p-1 rounded-lg">
                <Button size="sm" :variant="currentSide.background.type === 'solid' ? 'default' : 'ghost'" class="flex-1 h-8" @click="updateConfig((c) => { c[activeSide].background.type = 'solid'; })">Solid</Button>
                <Button size="sm" :variant="currentSide.background.type === 'gradient' ? 'default' : 'ghost'" class="flex-1 h-8" @click="updateConfig((c) => { c[activeSide].background.type = 'gradient'; })">Gradient</Button>
                <Button size="sm" :variant="currentSide.background.type === 'image' ? 'default' : 'ghost'" class="flex-1 h-8" @click="updateConfig((c) => { c[activeSide].background.type = 'image'; })">Image</Button>
             </div>
             
             <div v-if="currentSide.background.type === 'solid'" class="space-y-2">
                 <Label class="text-sm">Color</Label>
                 <div class="flex items-center gap-2">
                     <input type="color" :value="currentSide.background.solidColor" @input="updateConfig((c) => { c[activeSide].background.solidColor = ($event.target as HTMLInputElement).value; })" class="size-9 cursor-pointer rounded-md border p-1" />
                     <Input :value="currentSide.background.solidColor" @input="updateConfig((c) => { c[activeSide].background.solidColor = ($event.target as HTMLInputElement).value; })" class="font-mono text-sm uppercase" />
                 </div>
             </div>
             
             <div v-if="currentSide.background.type === 'gradient'" class="space-y-4">
                 <div class="space-y-2">
                     <Label class="text-sm">Start Color</Label>
                     <div class="flex items-center gap-2">
                         <input type="color" :value="currentSide.background.gradientStart" @input="updateConfig((c) => { c[activeSide].background.gradientStart = ($event.target as HTMLInputElement).value; })" class="size-9 cursor-pointer rounded-md border p-1" />
                         <Input :value="currentSide.background.gradientStart" @input="updateConfig((c) => { c[activeSide].background.gradientStart = ($event.target as HTMLInputElement).value; })" class="font-mono text-sm uppercase" />
                     </div>
                 </div>
                 <div class="space-y-2">
                     <Label class="text-sm">End Color</Label>
                     <div class="flex items-center gap-2">
                         <input type="color" :value="currentSide.background.gradientEnd" @input="updateConfig((c) => { c[activeSide].background.gradientEnd = ($event.target as HTMLInputElement).value; })" class="size-9 cursor-pointer rounded-md border p-1" />
                         <Input :value="currentSide.background.gradientEnd" @input="updateConfig((c) => { c[activeSide].background.gradientEnd = ($event.target as HTMLInputElement).value; })" class="font-mono text-sm uppercase" />
                     </div>
                 </div>
                 <div class="space-y-2">
                     <Label class="text-sm">Angle ({{currentSide.background.gradientAngle}}&deg;)</Label>
                     <input type="range" min="0" max="360" :value="currentSide.background.gradientAngle" @input="updateConfig((c) => { c[activeSide].background.gradientAngle = ($event.target as HTMLInputElement).value; })" class="w-full" />
                 </div>
             </div>
             
             <div v-if="currentSide.background.type === 'image'" class="space-y-4">
                 <div v-if="currentSide.background.imageBase64" class="space-y-2">
                     <div class="w-full aspect-[320/510] overflow-hidden rounded-md border shadow-sm relative group">
                         <img :src="currentSide.background.imageBase64" class="w-full h-full object-cover" />
                         <div class="absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                            <Button size="sm" variant="destructive" @click="updateConfig((c) => { c[activeSide].background.imageBase64 = null; c[activeSide].background.type = 'solid'; })">
                                <Trash2 class="w-4 h-4 mr-2" /> Remove Image
                            </Button>
                         </div>
                     </div>
                 </div>
                 <div v-else>
                     <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer bg-muted/50 hover:bg-muted transition-colors">
                        <div class="flex flex-col items-center justify-center pt-5 pb-6">
                            <ImagePlus class="w-8 h-8 mb-3 text-muted-foreground" />
                            <p class="mb-1 text-sm font-semibold">Click to upload</p>
                            <p class="text-xs text-muted-foreground">PNG, JPG or SVG</p>
                        </div>
                        <input type="file" accept="image/*" class="hidden" @change="onBackgroundImageUpload" />
                     </label>
                 </div>
             </div>
          </TabsContent>
        </Tabs>
      </div>

      <!-- Canvas Area -->
      <div class="flex-1 bg-[radial-gradient(circle,#e5e7eb_1px,transparent_1px)] bg-[size:20px_20px] dark:bg-[radial-gradient(circle,#374151_1px,transparent_1px)] flex items-center justify-center relative overflow-hidden" @click.self="onCanvasClick">
         
         <div 
             ref="canvasRef"
             class="relative transition-transform duration-200 shadow-2xl ring-1 ring-black/10 select-none bg-white origin-center"
             :style="{ width: CARD_WIDTH + 'px', height: CARD_HEIGHT + 'px', transform: `scale(${zoom / 100})`, ...getBackgroundStyle(currentSide.background) }"
             @click.self="onCanvasClick"
         >
             <!-- Snap Lines -->
             <div v-for="line in snapLines" :key="line.type + line.pos" class="pointer-events-none absolute z-50"
                  :style="line.type === 'vertical' ? { left: line.pos + '%', top: 0, bottom: 0, width: '1px', backgroundColor: '#3b82f6', opacity: '0.6' } : { top: line.pos + '%', left: 0, right: 0, height: '1px', backgroundColor: '#3b82f6', opacity: '0.6' }" />

             <!-- Elements -->
             <div v-for="el in currentSide.elements" :key="el.id" class="group absolute"
                  :class="{ 'z-50': selectedElementId === el.id, 'z-10': selectedElementId !== el.id }"
                  :style="{ left: el.x + '%', top: el.y + '%', transform: 'translate(-50%, -50%)' + (el.rotation ? ` rotate(${el.rotation}deg)` : '') }"
                  @mousedown="onElementMouseDown($event, el.id)"
                  @dblclick.stop="el.type === 'text' ? startEditText(el.id) : undefined">
                  
                  <div v-if="el.type === 'photo'" class="relative flex items-center justify-center overflow-hidden bg-muted/50"
                       :class="selectedElementId === el.id ? 'ring-2 ring-blue-500 ring-offset-0' : 'hover:ring-2 hover:ring-blue-300 hover:ring-offset-0'"
                       :style="{ width: (el.width / 100) * CARD_WIDTH + 'px', height: (el.height / 100) * CARD_HEIGHT + 'px', borderRadius: el.borderRadius + 'px', opacity: (el.opacity ?? 100) / 100, border: el.borderWidth ? `${el.borderWidth}px solid ${el.borderColor}` : 'none' }">
                      <img v-if="photoUrl" :src="photoUrl" class="size-full object-cover" :style="{ borderRadius: el.borderRadius + 'px' }" />
                      <UserCircle v-else class="size-10 text-muted-foreground/60" />
                      
                      <template v-if="selectedElementId === el.id">
                          <div class="absolute top-0 left-0 size-3 -translate-x-1/2 -translate-y-1/2 cursor-nw-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'nw')" />
                          <div class="absolute top-0 right-0 size-3 translate-x-1/2 -translate-y-1/2 cursor-ne-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'ne')" />
                          <div class="absolute bottom-0 left-0 size-3 -translate-x-1/2 translate-y-1/2 cursor-sw-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'sw')" />
                          <div class="absolute right-0 bottom-0 size-3 translate-x-1/2 translate-y-1/2 cursor-se-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'se')" />
                      </template>
                  </div>

                  <div v-else-if="el.type === 'shape'" class="relative flex items-center justify-center overflow-visible"
                       :class="selectedElementId === el.id ? 'ring-2 ring-blue-500 ring-offset-0' : 'hover:ring-2 hover:ring-blue-300 hover:ring-offset-0'"
                       :style="{ width: (el.width / 100) * CARD_WIDTH + 'px', height: (el.height / 100) * CARD_HEIGHT + 'px', opacity: (el.opacity ?? 100) / 100 }">
                      
                      <div class="w-full h-full" :style="{ backgroundColor: el.backgroundColor, borderRadius: el.shapeType === 'circle' ? '50%' : el.borderRadius + 'px', border: el.borderWidth ? `${el.borderWidth}px solid ${el.borderColor}` : 'none' }" />

                      <template v-if="selectedElementId === el.id">
                          <div class="absolute top-0 left-0 size-3 -translate-x-1/2 -translate-y-1/2 cursor-nw-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'nw')" />
                          <div class="absolute top-0 right-0 size-3 translate-x-1/2 -translate-y-1/2 cursor-ne-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'ne')" />
                          <div class="absolute bottom-0 left-0 size-3 -translate-x-1/2 translate-y-1/2 cursor-sw-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'sw')" />
                          <div class="absolute right-0 bottom-0 size-3 translate-x-1/2 translate-y-1/2 cursor-se-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'se')" />
                      </template>
                  </div>

                  <div v-else-if="el.type === 'qr'" class="relative flex items-center justify-center overflow-visible"
                       :class="selectedElementId === el.id ? 'ring-2 ring-blue-500 ring-offset-0' : 'hover:ring-2 hover:ring-blue-300 hover:ring-offset-0'"
                       :style="{ width: (el.size / 100) * CARD_WIDTH + 'px', height: (el.size / 100) * CARD_WIDTH + 'px', opacity: (el.opacity ?? 100) / 100, backgroundColor: el.backgroundColor, padding: '4px' }">
                      
                      <QrCode class="w-full h-full" :style="{ color: el.color }" />

                      <template v-if="selectedElementId === el.id">
                          <div class="absolute right-0 bottom-0 size-3 translate-x-1/2 translate-y-1/2 cursor-se-resize rounded-full border-2 border-white bg-blue-500 shadow-sm" @mousedown.stop="onResizeMouseDown($event, el.id, 'se')" />
                      </template>
                  </div>

                  <div v-else-if="el.type === 'text'" class="relative cursor-move transition-shadow"
                       :class="selectedElementId === el.id ? 'ring-2 ring-blue-500 ring-offset-0' : 'hover:ring-1 hover:ring-blue-300'"
                       :style="{ fontSize: el.fontSize + 'px', fontFamily: el.fontFamily, fontWeight: el.fontWeight, color: el.color, textAlign: el.textAlign, textTransform: el.textTransform as any, letterSpacing: el.letterSpacing + 'px', lineHeight: el.lineHeight, opacity: (el.opacity ?? 100) / 100, whiteSpace: 'nowrap', minWidth: '20px', padding: '2px 4px' }">
                      
                      <div v-if="editingTextId === el.id" ref="editTextRef" contenteditable="true" class="min-w-[30px] rounded-sm ring-2 ring-blue-400 outline-none"
                           :style="{ fontSize: el.fontSize + 'px', fontFamily: el.fontFamily, fontWeight: el.fontWeight, color: el.color, textAlign: el.textAlign, textTransform: el.textTransform as any, letterSpacing: el.letterSpacing + 'px', lineHeight: el.lineHeight, whiteSpace: 'nowrap', background: 'rgba(0,0,0,0.2)', padding: '2px 6px' }"
                           @blur="onEditTextBlur" @input="onEditTextInput" @keydown.enter.prevent="finishEditText" v-text="el.content" />
                      <template v-else>{{ resolveContent(el.content) }}</template>
                  </div>

             </div>
         </div>
         
         <div class="absolute bottom-4 right-4 flex items-center bg-background/90 backdrop-blur-sm border rounded-lg shadow-lg px-2 py-1">
            <Button variant="ghost" size="icon" class="w-8 h-8 rounded-md" @click="zoomOut"><ZoomOut class="w-4 h-4" /></Button>
            <span class="text-xs font-semibold w-12 text-center">{{zoom}}%</span>
            <Button variant="ghost" size="icon" class="w-8 h-8 rounded-md" @click="zoomIn"><ZoomIn class="w-4 h-4" /></Button>
         </div>
      </div>

      <!-- Right Sidebar: Properties -->
      <div class="w-80 border-l flex flex-col bg-muted/5 z-10 overflow-hidden shadow-[-4px_0_15px_rgba(0,0,0,0.03)]">
        <div class="p-3 border-b flex items-center justify-between bg-background h-12">
           <h3 class="font-semibold flex items-center text-sm"><Settings2 class="w-4 h-4 mr-2 text-primary" /> Properties</h3>
           <div class="flex items-center gap-0.5" v-if="selectedElement">
               <Button variant="ghost" size="icon" class="h-7 w-7" @click="moveElementOrder(selectedElementId!, 'up')" title="Bring Forward"><MoveUp class="w-3.5 h-3.5" /></Button>
               <Button variant="ghost" size="icon" class="h-7 w-7" @click="moveElementOrder(selectedElementId!, 'down')" title="Send Backward"><MoveDown class="w-3.5 h-3.5" /></Button>
               <Separator orientation="vertical" class="h-4 mx-1" />
               <Button variant="ghost" size="icon" class="h-7 w-7" @click="duplicateElement(selectedElementId!)" title="Duplicate"><Copy class="w-3.5 h-3.5" /></Button>
               <Button variant="ghost" size="icon" class="h-7 w-7 text-destructive hover:text-destructive hover:bg-destructive/10" @click="deleteElement(selectedElementId!)" title="Delete"><Trash2 class="w-3.5 h-3.5" /></Button>
           </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4 space-y-6" v-if="selectedElement">
           
           <!-- POSITION & OPACITY (COMMON FOR ALL) -->
           <div class="space-y-4">
              <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Layout</h4>
              <div class="grid grid-cols-2 gap-3">
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground">X Position (%)</Label>
                    <Input type="number" :value="Math.round(selectedElement.x)" @input="updateSelectedProp('x', parseFloat(($event.target as HTMLInputElement).value))" class="h-8 text-sm" />
                 </div>
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground">Y Position (%)</Label>
                    <Input type="number" :value="Math.round(selectedElement.y)" @input="updateSelectedProp('y', parseFloat(($event.target as HTMLInputElement).value))" class="h-8 text-sm" />
                 </div>
              </div>
              
              <div class="grid grid-cols-2 gap-3">
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground flex justify-between">Opacity <span>{{selectedElement.opacity}}%</span></Label>
                    <input type="range" min="0" max="100" :value="selectedElement.opacity" @input="updateSelectedProp('opacity', parseInt(($event.target as HTMLInputElement).value))" class="w-full" />
                 </div>
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground flex justify-between">Rotation <span>{{selectedElement.rotation}}&deg;</span></Label>
                    <input type="range" min="-180" max="180" :value="selectedElement.rotation" @input="updateSelectedProp('rotation', parseInt(($event.target as HTMLInputElement).value))" class="w-full" />
                 </div>
              </div>
           </div>

           <Separator />

           <!-- TEXT PROPERTIES -->
           <template v-if="selectedElement.type === 'text'">
              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Text Content</h4>
                 <div class="space-y-1.5">
                    <Input :value="selectedElement.content" @input="updateSelectedProp('content', ($event.target as HTMLInputElement).value)" />
                 </div>
                 <div class="flex flex-wrap gap-1.5">
                    <button v-for="field in DYNAMIC_FIELDS" :key="field.value"
                            class="rounded text-[10px] px-2 py-1 border transition-colors hover:bg-primary hover:text-primary-foreground font-medium"
                            :class="selectedElement.content === field.value ? 'bg-primary text-primary-foreground border-primary' : 'bg-background text-muted-foreground'"
                            @click="updateSelectedProp('content', field.value)">
                        {{ field.label }}
                    </button>
                 </div>
              </div>

              <Separator />

              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Typography</h4>
                 
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground">Font Family</Label>
                    <select class="w-full h-9 rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                            :value="selectedElement.fontFamily"
                            @change="updateSelectedProp('fontFamily', ($event.target as HTMLSelectElement).value)">
                        <option v-for="font in FONTS" :key="font" :value="font">{{ font }}</option>
                    </select>
                 </div>

                 <div class="grid grid-cols-2 gap-3">
                     <div class="space-y-1.5">
                        <Label class="text-xs text-muted-foreground">Font Size (px)</Label>
                        <Input type="number" min="4" max="72" :value="selectedElement.fontSize" @input="updateSelectedProp('fontSize', parseInt(($event.target as HTMLInputElement).value))" class="h-8" />
                     </div>
                     <div class="space-y-1.5">
                        <Label class="text-xs text-muted-foreground">Text Color</Label>
                        <div class="flex items-center gap-1.5">
                            <input type="color" :value="selectedElement.color" @input="updateSelectedProp('color', ($event.target as HTMLInputElement).value)" class="size-8 cursor-pointer rounded border p-0.5" />
                            <Input :value="selectedElement.color" @input="updateSelectedProp('color', ($event.target as HTMLInputElement).value)" class="h-8 flex-1 font-mono text-xs uppercase" />
                        </div>
                     </div>
                 </div>

                 <div class="space-y-1.5">
                     <Label class="text-xs text-muted-foreground">Style & Alignment</Label>
                     <div class="flex gap-1">
                         <Button size="sm" :variant="selectedElement.fontWeight === 'bold' ? 'default' : 'outline'" class="flex-1 h-8" @click="updateSelectedProp('fontWeight', selectedElement.fontWeight === 'bold' ? 'normal' : 'bold')"><Bold class="w-3.5 h-3.5" /></Button>
                         <Button size="sm" :variant="selectedElement.textAlign === 'left' ? 'default' : 'outline'" class="flex-1 h-8" @click="updateSelectedProp('textAlign', 'left')"><AlignLeft class="w-3.5 h-3.5" /></Button>
                         <Button size="sm" :variant="selectedElement.textAlign === 'center' ? 'default' : 'outline'" class="flex-1 h-8" @click="updateSelectedProp('textAlign', 'center')"><AlignCenter class="w-3.5 h-3.5" /></Button>
                         <Button size="sm" :variant="selectedElement.textAlign === 'right' ? 'default' : 'outline'" class="flex-1 h-8" @click="updateSelectedProp('textAlign', 'right')"><AlignRight class="w-3.5 h-3.5" /></Button>
                     </div>
                     <div class="flex gap-1 mt-1">
                         <Button size="sm" :variant="selectedElement.textTransform === 'none' ? 'default' : 'outline'" class="flex-1 h-8" @click="updateSelectedProp('textTransform', 'none')"><CaseSensitive class="w-3.5 h-3.5 mr-1" /> Aa</Button>
                         <Button size="sm" :variant="selectedElement.textTransform === 'uppercase' ? 'default' : 'outline'" class="flex-1 h-8" @click="updateSelectedProp('textTransform', 'uppercase')">AA</Button>
                     </div>
                 </div>

                 <div class="grid grid-cols-2 gap-3">
                     <div class="space-y-1.5">
                        <Label class="text-xs text-muted-foreground flex justify-between">Spacing <span>{{selectedElement.letterSpacing}}px</span></Label>
                        <input type="range" min="-5" max="20" step="0.5" :value="selectedElement.letterSpacing" @input="updateSelectedProp('letterSpacing', parseFloat(($event.target as HTMLInputElement).value))" class="w-full" />
                     </div>
                     <div class="space-y-1.5">
                        <Label class="text-xs text-muted-foreground flex justify-between">Line Height <span>{{selectedElement.lineHeight}}</span></Label>
                        <input type="range" min="0.5" max="3" step="0.1" :value="selectedElement.lineHeight" @input="updateSelectedProp('lineHeight', parseFloat(($event.target as HTMLInputElement).value))" class="w-full" />
                     </div>
                 </div>
              </div>
           </template>

           <!-- PHOTO PROPERTIES -->
           <template v-else-if="selectedElement.type === 'photo'">
              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Dimensions</h4>
                 <div class="grid grid-cols-2 gap-3">
                     <div class="space-y-1.5">
                        <Label class="text-xs text-muted-foreground">Width (%)</Label>
                        <Input type="number" min="5" max="100" :value="Math.round(selectedElement.width)" @input="updateSelectedProp('width', parseInt(($event.target as HTMLInputElement).value))" class="h-8" />
                     </div>
                     <div class="space-y-1.5">
                        <Label class="text-xs text-muted-foreground">Height (%)</Label>
                        <Input type="number" min="5" max="100" :value="Math.round(selectedElement.height)" @input="updateSelectedProp('height', parseInt(($event.target as HTMLInputElement).value))" class="h-8" />
                     </div>
                 </div>
                 
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground flex justify-between">Corner Radius <span>{{selectedElement.borderRadius}}px</span></Label>
                    <input type="range" min="0" max="100" :value="selectedElement.borderRadius" @input="updateSelectedProp('borderRadius', parseInt(($event.target as HTMLInputElement).value))" class="w-full" />
                 </div>
              </div>

              <Separator />

              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Border</h4>
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground flex justify-between">Border Width <span>{{selectedElement.borderWidth}}px</span></Label>
                    <input type="range" min="0" max="10" :value="selectedElement.borderWidth" @input="updateSelectedProp('borderWidth', parseInt(($event.target as HTMLInputElement).value))" class="w-full" />
                 </div>
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground">Border Color</Label>
                    <div class="flex items-center gap-1.5">
                        <input type="color" :value="selectedElement.borderColor" @input="updateSelectedProp('borderColor', ($event.target as HTMLInputElement).value)" class="size-8 cursor-pointer rounded border p-0.5" />
                        <Input :value="selectedElement.borderColor" @input="updateSelectedProp('borderColor', ($event.target as HTMLInputElement).value)" class="h-8 flex-1 font-mono text-xs uppercase" />
                    </div>
                 </div>
              </div>
           </template>

           <!-- SHAPE PROPERTIES -->
           <template v-else-if="selectedElement.type === 'shape'">
              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Shape Type</h4>
                 <div class="flex bg-muted p-1 rounded-lg">
                    <Button size="sm" :variant="selectedElement.shapeType === 'rectangle' ? 'default' : 'ghost'" class="flex-1 h-8" @click="updateSelectedProp('shapeType', 'rectangle')"><Square class="w-4 h-4" /></Button>
                    <Button size="sm" :variant="selectedElement.shapeType === 'circle' ? 'default' : 'ghost'" class="flex-1 h-8" @click="updateSelectedProp('shapeType', 'circle')"><Circle class="w-4 h-4" /></Button>
                    <Button size="sm" :variant="selectedElement.shapeType === 'line' ? 'default' : 'ghost'" class="flex-1 h-8" @click="updateSelectedProp('shapeType', 'line')"><Minus class="w-4 h-4" /></Button>
                 </div>
              </div>

              <Separator />

              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Dimensions</h4>
                 <div class="grid grid-cols-2 gap-3">
                     <div class="space-y-1.5">
                        <Label class="text-xs text-muted-foreground">Width (%)</Label>
                        <Input type="number" min="1" max="100" :value="Math.round(selectedElement.width)" @input="updateSelectedProp('width', parseInt(($event.target as HTMLInputElement).value))" class="h-8" />
                     </div>
                     <div class="space-y-1.5">
                        <Label class="text-xs text-muted-foreground">Height (%)</Label>
                        <Input type="number" min="1" max="100" :value="Math.round(selectedElement.height)" @input="updateSelectedProp('height', parseInt(($event.target as HTMLInputElement).value))" class="h-8" />
                     </div>
                 </div>
                 
                 <div class="space-y-1.5" v-if="selectedElement.shapeType === 'rectangle'">
                    <Label class="text-xs text-muted-foreground flex justify-between">Corner Radius <span>{{selectedElement.borderRadius}}px</span></Label>
                    <input type="range" min="0" max="100" :value="selectedElement.borderRadius" @input="updateSelectedProp('borderRadius', parseInt(($event.target as HTMLInputElement).value))" class="w-full" />
                 </div>
              </div>

              <Separator />

              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Appearance</h4>
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground">Fill Color</Label>
                    <div class="flex items-center gap-1.5">
                        <input type="color" :value="selectedElement.backgroundColor" @input="updateSelectedProp('backgroundColor', ($event.target as HTMLInputElement).value)" class="size-8 cursor-pointer rounded border p-0.5" />
                        <Input :value="selectedElement.backgroundColor" @input="updateSelectedProp('backgroundColor', ($event.target as HTMLInputElement).value)" class="h-8 flex-1 font-mono text-xs uppercase" />
                    </div>
                 </div>
                 
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground flex justify-between">Border Width <span>{{selectedElement.borderWidth}}px</span></Label>
                    <input type="range" min="0" max="10" :value="selectedElement.borderWidth" @input="updateSelectedProp('borderWidth', parseInt(($event.target as HTMLInputElement).value))" class="w-full" />
                 </div>
                 <div class="space-y-1.5" v-if="selectedElement.borderWidth > 0">
                    <Label class="text-xs text-muted-foreground">Border Color</Label>
                    <div class="flex items-center gap-1.5">
                        <input type="color" :value="selectedElement.borderColor" @input="updateSelectedProp('borderColor', ($event.target as HTMLInputElement).value)" class="size-8 cursor-pointer rounded border p-0.5" />
                        <Input :value="selectedElement.borderColor" @input="updateSelectedProp('borderColor', ($event.target as HTMLInputElement).value)" class="h-8 flex-1 font-mono text-xs uppercase" />
                    </div>
                 </div>
              </div>
           </template>

           <!-- QR PROPERTIES -->
           <template v-else-if="selectedElement.type === 'qr'">
              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">QR Code Data</h4>
                 <div class="space-y-1.5">
                    <Input :value="selectedElement.content" @input="updateSelectedProp('content', ($event.target as HTMLInputElement).value)" />
                 </div>
                 <div class="flex flex-wrap gap-1.5">
                    <button v-for="field in DYNAMIC_FIELDS" :key="field.value"
                            class="rounded text-[10px] px-2 py-1 border transition-colors hover:bg-primary hover:text-primary-foreground font-medium"
                            :class="selectedElement.content === field.value ? 'bg-primary text-primary-foreground border-primary' : 'bg-background text-muted-foreground'"
                            @click="updateSelectedProp('content', field.value)">
                        {{ field.label }}
                    </button>
                 </div>
              </div>

              <Separator />

              <div class="space-y-4">
                 <h4 class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Appearance</h4>
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground flex justify-between">Size (%) <span>{{selectedElement.size}}%</span></Label>
                    <input type="range" min="5" max="80" :value="selectedElement.size" @input="updateSelectedProp('size', parseInt(($event.target as HTMLInputElement).value))" class="w-full" />
                 </div>
                 
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground">QR Color</Label>
                    <div class="flex items-center gap-1.5">
                        <input type="color" :value="selectedElement.color" @input="updateSelectedProp('color', ($event.target as HTMLInputElement).value)" class="size-8 cursor-pointer rounded border p-0.5" />
                        <Input :value="selectedElement.color" @input="updateSelectedProp('color', ($event.target as HTMLInputElement).value)" class="h-8 flex-1 font-mono text-xs uppercase" />
                    </div>
                 </div>
                 <div class="space-y-1.5">
                    <Label class="text-xs text-muted-foreground">Background Color</Label>
                    <div class="flex items-center gap-1.5">
                        <input type="color" :value="selectedElement.backgroundColor" @input="updateSelectedProp('backgroundColor', ($event.target as HTMLInputElement).value)" class="size-8 cursor-pointer rounded border p-0.5" />
                        <Input :value="selectedElement.backgroundColor" @input="updateSelectedProp('backgroundColor', ($event.target as HTMLInputElement).value)" class="h-8 flex-1 font-mono text-xs uppercase" />
                    </div>
                 </div>
              </div>
           </template>

        </div>
        <div class="flex-1 flex flex-col items-center justify-center text-muted-foreground p-8 text-center" v-else>
            <MousePointerClick class="w-12 h-12 mb-3 opacity-20" />
            <p class="text-sm font-medium">No Element Selected</p>
            <p class="text-xs mt-1 opacity-70">Click on an element in the canvas or layers panel to edit its properties.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Range input styling for a better UI */
input[type=range] {
  -webkit-appearance: none;
  width: 100%;
  background: transparent;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: hsl(var(--primary));
  cursor: pointer;
  margin-top: -6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
input[type=range]::-webkit-slider-runnable-track {
  width: 100%;
  height: 4px;
  cursor: pointer;
  background: hsl(var(--muted));
  border-radius: 2px;
}
input[type=range]:focus {
  outline: none;
}
input[type=range]:focus::-webkit-slider-thumb {
  ring: 2px solid hsl(var(--ring));
}
</style>
"""

with open("resources/js/components/TemplateEditor.vue", "w") as f:
    f.write(content)
