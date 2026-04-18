<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import SignaturePad from 'signature_pad';
import { Button } from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogTrigger,
} from '@/components/ui/dialog';
import { RotateCcw, PenLine, Check } from 'lucide-vue-next';

const props = defineProps<{
    modelValue: string | null;
}>();

const emit = defineEmits<{
    (e: 'update:modelValue', value: string | null): void;
}>();

const isModalOpen = ref(false);
const canvas = ref<HTMLCanvasElement | null>(null);
let pad: SignaturePad | null = null;
const tempSignature = ref<string | null>(null);

watch(isModalOpen, async (isOpen) => {
    if (isOpen) {
        tempSignature.value = props.modelValue;
        await nextTick();
        initPad();
    } else {
        if (pad) {
            pad.off();
            pad = null;
        }
        window.removeEventListener('resize', resizeCanvas);
    }
});

function initPad() {
    if (!canvas.value) return;
    
    pad = new SignaturePad(canvas.value, {
        backgroundColor: 'rgba(255, 255, 255, 0)', // Transparent
        penColor: 'black',
        minWidth: 1,
        maxWidth: 3,
    });

    if (tempSignature.value) {
        pad.fromDataURL(tempSignature.value);
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
}

function resizeCanvas() {
    if (!canvas.value || !pad) return;
    
    const ratio = Math.max(window.devicePixelRatio || 1, 1);
    // Use the container's clientWidth/clientHeight
    const w = canvas.value.parentElement?.clientWidth || canvas.value.width;
    const h = canvas.value.parentElement?.clientHeight || canvas.value.height;
    
    if (canvas.value.width !== w * ratio || canvas.value.height !== h * ratio) {
        const data = pad.toData();
        canvas.value.width = w * ratio;
        canvas.value.height = h * ratio;
        const ctx = canvas.value.getContext("2d");
        if (ctx) ctx.scale(ratio, ratio);
        
        pad.clear();
        pad.fromData(data);
    }
}

function clear() {
    if (pad) {
        pad.clear();
        tempSignature.value = null;
    }
}

function cropSignatureAndSave() {
    if (!pad || pad.isEmpty()) {
        emit('update:modelValue', null);
        isModalOpen.value = false;
        return;
    }
    
    // Auto-crop whitespace
    const origCanvas = canvas.value!;
    const ctx = origCanvas.getContext('2d')!;
    const imgData = ctx.getImageData(0, 0, origCanvas.width, origCanvas.height);
    const data = imgData.data;
    
    let minX = origCanvas.width;
    let minY = origCanvas.height;
    let maxX = 0;
    let maxY = 0;
    
    let isNotEmpty = false;
    
    for (let y = 0; y < origCanvas.height; y++) {
        for (let x = 0; x < origCanvas.width; x++) {
            const alpha = data[(y * origCanvas.width + x) * 4 + 3];
            if (alpha > 0) {
                isNotEmpty = true;
                if (x < minX) minX = x;
                if (x > maxX) maxX = x;
                if (y < minY) minY = y;
                if (y > maxY) maxY = y;
            }
        }
    }
    
    if (!isNotEmpty) {
        emit('update:modelValue', null);
        isModalOpen.value = false;
        return;
    }
    
    // Add a little padding
    const padding = 10;
    minX = Math.max(0, minX - padding);
    minY = Math.max(0, minY - padding);
    maxX = Math.min(origCanvas.width, maxX + padding);
    maxY = Math.min(origCanvas.height, maxY + padding);
    
    const cropWidth = maxX - minX;
    const cropHeight = maxY - minY;
    
    const cropCanvas = document.createElement('canvas');
    cropCanvas.width = cropWidth;
    cropCanvas.height = cropHeight;
    const cropCtx = cropCanvas.getContext('2d')!;
    cropCtx.putImageData(ctx.getImageData(minX, minY, cropWidth, cropHeight), 0, 0);
    
    emit('update:modelValue', cropCanvas.toDataURL());
    isModalOpen.value = false;
}
</script>

<template>
    <div class="space-y-2">
        <Dialog v-model:open="isModalOpen">
            <DialogTrigger as-child>
                <div 
                    class="relative overflow-hidden rounded-md border-2 border-dashed border-input bg-muted/30 flex flex-col justify-center items-center cursor-pointer hover:bg-muted/50 transition-colors"
                    style="height: 120px;"
                >
                    <img 
                        v-if="modelValue" 
                        :src="modelValue" 
                        class="h-full w-full object-contain p-2" 
                        alt="Signature"
                    />
                    <div v-else class="flex flex-col items-center justify-center opacity-50 space-y-2">
                        <PenLine class="h-6 w-6" />
                        <span class="text-sm font-medium">Click to Draw Signature</span>
                    </div>
                </div>
            </DialogTrigger>
            
            <DialogContent class="sm:max-w-2xl">
                <DialogHeader>
                    <DialogTitle>Draw Signature</DialogTitle>
                </DialogHeader>
                
                <div class="my-4 relative w-full h-[300px] border rounded-md overflow-hidden bg-white shadow-inner">
                    <canvas ref="canvas" class="w-full h-full touch-none cursor-crosshair"></canvas>
                    <div class="absolute bottom-4 left-0 right-0 flex justify-center pointer-events-none">
                        <div class="w-2/3 border-b-2 border-gray-200"></div>
                    </div>
                </div>
                
                <DialogFooter class="flex sm:justify-between items-center w-full">
                    <Button variant="outline" type="button" @click="clear" class="w-full sm:w-auto">
                        <RotateCcw class="h-4 w-4 mr-2" />
                        Clear
                    </Button>
                    <div class="flex gap-2 w-full sm:w-auto mt-2 sm:mt-0">
                        <Button variant="ghost" @click="isModalOpen = false" class="flex-1 sm:flex-none">Cancel</Button>
                        <Button @click="cropSignatureAndSave" class="flex-1 sm:flex-none">
                            <Check class="h-4 w-4 mr-2" />
                            Save Signature
                        </Button>
                    </div>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>
