<script setup lang="ts">
import { computed } from 'vue';

type CardData = {
    name: string;
    course: string;
    studentIdNumber: string;
    contactNumber: string;
    guardianContactPerson: string;
    photoUrl: string | null;
    schoolName: string;
};

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
type CardSide = { background: Background; elements: TemplateElement[] };
type TemplateConfig = { front: CardSide; back: CardSide };

const props = withDefaults(
    defineProps<{
        template: string;
        side: 'front' | 'back' | 'both';
        data: CardData;
        scale?: number;
        config?: TemplateConfig | null;
    }>(),
    {
        scale: 1,
        side: 'both',
    },
);

const CARD_W = 214;
const CARD_H = 340;

function initials(name: string): string {
    return (
        name
            .split(' ')
            .map((w) => w[0])
            .join('')
            .substring(0, 2)
            .toUpperCase() || '?'
    );
}

const containerStyle = computed(() => ({
    width: `${CARD_W * props.scale}px`,
    minHeight:
        props.side === 'both'
            ? `${(CARD_H * 2 + 12) * props.scale}px`
            : `${CARD_H * props.scale}px`,
}));

const cardStyle = computed(() => ({
    width: `${CARD_W * props.scale}px`,
    height: `${CARD_H * props.scale}px`,
}));

function getBgStyle(bg: Background): Record<string, string> {
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

function resolveContent(content: string): string {
    const map: Record<string, string> = {
        '{{student.name}}': props.data.name || 'Student Name',
        '{{student.course}}': props.data.course || 'Course',
        '{{student.student_id_number}}': props.data.studentIdNumber || '1000',
        '{{student.contact_number}}': props.data.contactNumber || '—',
        '{{student.guardian_contact_person}}':
            props.data.guardianContactPerson || '—',
        '{{school_name}}': props.data.schoolName || 'DCCP',
    };
    return map[content] ?? content;
}
</script>

<template>
    <div class="flex flex-col gap-2" :style="containerStyle">
        <!-- Custom template -->
        <template v-if="template === 'custom' && config">
            <div
                v-if="side === 'front' || side === 'both'"
                class="relative overflow-hidden rounded-lg shadow-md"
                :style="{
                    ...cardStyle,
                    ...getBgStyle(config.front.background),
                }"
            >
                <template v-for="el in config.front.elements" :key="el.id">
                    <div
                        v-if="el.type === 'photo'"
                        class="absolute flex items-center justify-center overflow-hidden bg-black/20"
                        :style="{
                            left: el.x + '%',
                            top: el.y + '%',
                            transform: 'translate(-50%, -50%)',
                            width: (el.width / 100) * CARD_W * scale + 'px',
                            height: (el.height / 100) * CARD_H * scale + 'px',
                            borderRadius: el.borderRadius * scale + 'px',
                        }"
                    >
                        <img
                            v-if="data.photoUrl"
                            :src="data.photoUrl"
                            alt=""
                            class="size-full object-cover"
                            :style="{
                                borderRadius: el.borderRadius * scale + 'px',
                            }"
                        />
                        <span
                            v-else
                            class="text-white/60"
                            :style="{ fontSize: 8 * scale + 'px' }"
                            >{{ initials(data.name) }}</span
                        >
                    </div>
                    <div
                        v-else-if="el.type === 'text'"
                        class="absolute"
                        :style="{
                            left: el.x + '%',
                            top: el.y + '%',
                            transform: 'translate(-50%, -50%)',
                            fontSize: el.fontSize * scale + 'px',
                            fontWeight: el.fontWeight,
                            color: el.color,
                            textAlign: el.textAlign,
                            textTransform: el.textTransform as any,
                            whiteSpace: 'nowrap',
                        }"
                    >
                        {{ resolveContent(el.content) }}
                    </div>
                </template>
            </div>
            <div
                v-if="side === 'back' || side === 'both'"
                class="relative overflow-hidden rounded-lg shadow-md"
                :style="{ ...cardStyle, ...getBgStyle(config.back.background) }"
            >
                <template v-for="el in config.back.elements" :key="el.id">
                    <div
                        v-if="el.type === 'photo'"
                        class="absolute flex items-center justify-center overflow-hidden bg-black/20"
                        :style="{
                            left: el.x + '%',
                            top: el.y + '%',
                            transform: 'translate(-50%, -50%)',
                            width: (el.width / 100) * CARD_W * scale + 'px',
                            height: (el.height / 100) * CARD_H * scale + 'px',
                            borderRadius: el.borderRadius * scale + 'px',
                        }"
                    >
                        <img
                            v-if="data.photoUrl"
                            :src="data.photoUrl"
                            alt=""
                            class="size-full object-cover"
                            :style="{
                                borderRadius: el.borderRadius * scale + 'px',
                            }"
                        />
                        <span
                            v-else
                            class="text-white/60"
                            :style="{ fontSize: 8 * scale + 'px' }"
                            >{{ initials(data.name) }}</span
                        >
                    </div>
                    <div
                        v-else-if="el.type === 'text'"
                        class="absolute"
                        :style="{
                            left: el.x + '%',
                            top: el.y + '%',
                            transform: 'translate(-50%, -50%)',
                            fontSize: el.fontSize * scale + 'px',
                            fontWeight: el.fontWeight,
                            color: el.color,
                            textAlign: el.textAlign,
                            textTransform: el.textTransform as any,
                            whiteSpace: 'nowrap',
                        }"
                    >
                        {{ resolveContent(el.content) }}
                    </div>
                </template>
            </div>
        </template>

        <!-- Predefined templates -->
        <template v-else>
            <!-- FRONT -->
            <div
                v-if="side === 'front' || side === 'both'"
                :style="cardStyle"
                class="overflow-hidden rounded-lg shadow-md"
            >
                <!-- CLASSIC BLUE - Portrait -->
                <div
                    v-if="template === 'classic'"
                    class="flex size-full flex-col items-center overflow-hidden rounded-lg"
                    style="
                        background: linear-gradient(
                            180deg,
                            #1e3a5f 0%,
                            #2d5a87 100%
                        );
                        color: white;
                        padding: 16px 20px;
                    "
                >
                    <div class="mb-1 text-center">
                        <div
                            class="text-[9px] font-bold tracking-widest uppercase opacity-95"
                        >
                            {{ data.schoolName }}
                        </div>
                        <div
                            class="text-[5px] tracking-wider uppercase opacity-60"
                        >
                            Student Identification Card
                        </div>
                    </div>
                    <div
                        class="my-2 flex size-16 items-center justify-center overflow-hidden rounded-full border-2 border-white/40 bg-white/15"
                    >
                        <img
                            v-if="data.photoUrl"
                            :src="data.photoUrl"
                            alt=""
                            class="size-full object-cover"
                        />
                        <span v-else class="text-[10px] text-white/60">{{
                            initials(data.name)
                        }}</span>
                    </div>
                    <div class="text-center">
                        <div class="text-[13px] leading-tight font-bold">
                            {{ data.name || 'Student Name' }}
                        </div>
                        <div class="mt-0.5 text-[9px] opacity-90">
                            {{ data.course || 'Course' }}
                        </div>
                        <div
                            class="mt-2 inline-block rounded-full bg-white/15 px-4 py-1 text-[10px] font-bold tracking-widest"
                        >
                            {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>

                <!-- MODERN DARK - Portrait -->
                <div
                    v-else-if="template === 'modern'"
                    class="flex size-full flex-col items-center overflow-hidden rounded-lg"
                    style="
                        background: #1a1a2e;
                        color: #e0e0e0;
                        padding: 16px 14px;
                    "
                >
                    <div
                        class="mb-1 text-[7px] font-bold tracking-[3px] text-[#e94560] uppercase"
                    >
                        {{ data.schoolName }}
                    </div>
                    <div
                        class="mb-2 text-[5px] tracking-[2px] text-[#888] uppercase"
                    >
                        Student Identification Card
                    </div>
                    <div
                        class="mb-2 flex size-16 items-center justify-center overflow-hidden rounded-md border-2 border-[#e94560] bg-[#333]"
                    >
                        <img
                            v-if="data.photoUrl"
                            :src="data.photoUrl"
                            alt=""
                            class="size-full object-cover"
                        />
                        <span v-else class="text-lg font-bold text-[#e94560]">{{
                            initials(data.name)
                        }}</span>
                    </div>
                    <div
                        class="mb-2 h-px w-12"
                        style="
                            background: linear-gradient(
                                to right,
                                #e94560,
                                transparent
                            );
                        "
                    ></div>
                    <div class="w-full text-center">
                        <div class="text-[12px] font-bold text-white">
                            {{ data.name || 'Student Name' }}
                        </div>
                        <div class="mt-0.5 text-[9px] text-[#aaa]">
                            {{ data.course || 'Course' }}
                        </div>
                        <div
                            class="mt-2 text-[10px] font-bold tracking-wider text-[#e94560]"
                        >
                            {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>

                <!-- MINIMAL WHITE - Portrait -->
                <div
                    v-else-if="template === 'minimal'"
                    class="flex size-full flex-col items-center overflow-hidden rounded-lg border border-gray-200 bg-white"
                    style="color: #333; padding: 18px 20px"
                >
                    <div
                        class="mb-2 text-[7px] font-semibold tracking-[4px] text-gray-400 uppercase"
                    >
                        {{ data.schoolName }}
                    </div>
                    <div
                        class="mb-2 flex size-16 items-center justify-center overflow-hidden rounded-full border-2 border-gray-200 bg-gray-50"
                    >
                        <img
                            v-if="data.photoUrl"
                            :src="data.photoUrl"
                            alt=""
                            class="size-full object-cover"
                        />
                        <span v-else class="text-lg font-bold text-gray-300">{{
                            initials(data.name)
                        }}</span>
                    </div>
                    <div class="text-[13px] font-bold text-gray-800">
                        {{ data.name || 'Student Name' }}
                    </div>
                    <div
                        class="mt-0.5 text-[9px] tracking-wide text-gray-400 uppercase"
                    >
                        {{ data.course || 'Course' }}
                    </div>
                    <div
                        class="mt-3 rounded-full border border-gray-200 px-4 py-1 font-mono text-[10px] tracking-wider text-gray-500"
                    >
                        {{ data.studentIdNumber || '1000' }}
                    </div>
                </div>

                <!-- GRADIENT PURPLE - Portrait -->
                <div
                    v-else-if="template === 'gradient'"
                    class="flex size-full flex-col items-center overflow-hidden rounded-lg"
                    style="
                        background: linear-gradient(
                            180deg,
                            #667eea 0%,
                            #764ba2 100%
                        );
                        color: white;
                        padding: 16px 18px;
                    "
                >
                    <div class="mb-1 text-center">
                        <div
                            class="text-[9px] font-bold tracking-widest uppercase"
                        >
                            {{ data.schoolName }}
                        </div>
                        <div
                            class="text-[5px] tracking-wider uppercase opacity-70"
                        >
                            Student Identification Card
                        </div>
                    </div>
                    <div
                        class="my-0.5 h-0.5 w-14 rounded-full bg-white/40"
                    ></div>
                    <div
                        class="my-2 flex size-16 items-center justify-center overflow-hidden rounded-xl border-2 border-white/40 bg-white/15"
                    >
                        <img
                            v-if="data.photoUrl"
                            :src="data.photoUrl"
                            alt=""
                            class="size-full object-cover"
                        />
                        <span v-else class="text-[10px] text-white/60">{{
                            initials(data.name)
                        }}</span>
                    </div>
                    <div class="text-center">
                        <div class="text-[13px] leading-tight font-bold">
                            {{ data.name || 'Student Name' }}
                        </div>
                        <div class="mt-0.5 text-[9px] opacity-90">
                            {{ data.course || 'Course' }}
                        </div>
                        <div
                            class="mt-2 inline-block rounded-full bg-white/25 px-4 py-1 text-[10px] font-bold tracking-widest"
                        >
                            {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>

                <!-- PROFESSIONAL GREEN - Portrait -->
                <div
                    v-else-if="template === 'professional'"
                    class="flex size-full flex-col items-center overflow-hidden rounded-lg"
                    style="
                        background: #1b5e20;
                        color: white;
                        padding: 14px 16px;
                    "
                >
                    <div
                        class="mb-1 text-[7px] font-bold tracking-[3px] text-[#a5d6a7] uppercase"
                    >
                        {{ data.schoolName }}
                    </div>
                    <div
                        class="mb-2 text-[5px] tracking-wider text-white/50 uppercase"
                    >
                        Student Identification Card
                    </div>
                    <div
                        class="mb-2 flex size-16 items-center justify-center overflow-hidden rounded-md border-2 border-[#a5d6a7] bg-[#1b5e20]"
                    >
                        <img
                            v-if="data.photoUrl"
                            :src="data.photoUrl"
                            alt=""
                            class="size-full object-cover"
                        />
                        <span
                            v-else
                            class="text-[10px] font-bold text-[#a5d6a7]"
                            >{{ initials(data.name) }}</span
                        >
                    </div>
                    <div class="mb-2 h-0.5 w-8 rounded bg-[#a5d6a7]"></div>
                    <div class="w-full text-center">
                        <div class="text-[13px] font-bold">
                            {{ data.name || 'Student Name' }}
                        </div>
                        <div
                            class="mt-0.5 text-[9px] tracking-wide text-[#c8e6c9] uppercase"
                        >
                            {{ data.course || 'Course' }}
                        </div>
                        <div
                            class="mt-2 inline-block rounded border border-[#a5d6a7] bg-[#2e7d32] px-3 py-1 text-[10px] font-bold tracking-widest"
                        >
                            {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>
            </div>

            <!-- BACK -->
            <div
                v-if="side === 'back' || side === 'both'"
                :style="cardStyle"
                class="overflow-hidden rounded-lg shadow-md"
            >
                <!-- Classic Back -->
                <div
                    v-if="template === 'classic'"
                    class="flex size-full flex-col items-center justify-center overflow-hidden rounded-lg"
                    style="
                        background: linear-gradient(
                            180deg,
                            #f8f9fa 0%,
                            #e9ecef 100%
                        );
                        color: #333;
                        padding: 20px 18px;
                        border: 2px solid #dee2e6;
                    "
                >
                    <div
                        class="mb-4 w-full border-b border-[#adb5bd] pb-2 text-center"
                    >
                        <div
                            class="text-[8px] font-bold tracking-widest text-[#1e3a5f] uppercase"
                        >
                            {{ data.schoolName }}
                        </div>
                        <div
                            class="text-[5px] tracking-wider text-gray-500 uppercase"
                        >
                            Emergency Contact Information
                        </div>
                    </div>
                    <div class="w-full space-y-3 text-center">
                        <div>
                            <div
                                class="text-[6px] tracking-wider text-gray-500 uppercase"
                            >
                                Contact Number
                            </div>
                            <div class="text-[11px] font-bold">
                                {{ data.contactNumber || '—' }}
                            </div>
                        </div>
                        <div>
                            <div
                                class="text-[6px] tracking-wider text-gray-500 uppercase"
                            >
                                Guardian / Contact Person
                            </div>
                            <div class="text-[11px] font-bold">
                                {{ data.guardianContactPerson || '—' }}
                            </div>
                        </div>
                    </div>
                    <div
                        class="mt-auto w-full border-t border-[#adb5bd] pt-3 text-center"
                    >
                        <div
                            class="font-mono text-[8px] tracking-widest text-gray-400"
                        >
                            ID: {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>

                <!-- Modern Back -->
                <div
                    v-else-if="template === 'modern'"
                    class="flex size-full flex-col items-center justify-center overflow-hidden rounded-lg"
                    style="
                        background: #1a1a2e;
                        color: #e0e0e0;
                        padding: 20px 16px;
                        border: 2px solid #16213e;
                    "
                >
                    <div
                        class="mb-4 w-full border-b border-[#e94560] pb-2 text-center"
                    >
                        <div
                            class="text-[8px] font-bold tracking-wider text-[#e94560] uppercase"
                        >
                            {{ data.schoolName }}
                        </div>
                        <div
                            class="text-[5px] tracking-wider text-gray-500 uppercase"
                        >
                            Emergency Contact
                        </div>
                    </div>
                    <div class="w-full space-y-3 text-center">
                        <div>
                            <div
                                class="text-[6px] tracking-wider text-gray-500 uppercase"
                            >
                                Contact Number
                            </div>
                            <div class="text-[11px] font-bold text-gray-200">
                                {{ data.contactNumber || '—' }}
                            </div>
                        </div>
                        <div>
                            <div
                                class="text-[6px] tracking-wider text-gray-500 uppercase"
                            >
                                Guardian / Contact Person
                            </div>
                            <div class="text-[11px] font-bold text-gray-200">
                                {{ data.guardianContactPerson || '—' }}
                            </div>
                        </div>
                    </div>
                    <div
                        class="mt-auto w-full border-t border-[#333] pt-3 text-center"
                    >
                        <div
                            class="font-mono text-[8px] tracking-widest text-gray-600"
                        >
                            ID: {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>

                <!-- Minimal Back -->
                <div
                    v-else-if="template === 'minimal'"
                    class="flex size-full flex-col items-center justify-center overflow-hidden rounded-lg border border-gray-200 bg-[#fafafa]"
                    style="color: #333; padding: 22px 20px"
                >
                    <div
                        class="mb-4 w-full border-b border-gray-200 pb-2 text-center"
                    >
                        <div
                            class="text-[8px] font-semibold tracking-[4px] text-gray-400 uppercase"
                        >
                            {{ data.schoolName }}
                        </div>
                        <div
                            class="text-[5px] tracking-wider text-gray-300 uppercase"
                        >
                            Emergency Contact
                        </div>
                    </div>
                    <div class="w-full space-y-3 text-center">
                        <div>
                            <div
                                class="text-[6px] tracking-widest text-gray-400 uppercase"
                            >
                                Contact Number
                            </div>
                            <div
                                class="text-[11px] font-semibold text-gray-700"
                            >
                                {{ data.contactNumber || '—' }}
                            </div>
                        </div>
                        <div>
                            <div
                                class="text-[6px] tracking-widest text-gray-400 uppercase"
                            >
                                Guardian / Contact Person
                            </div>
                            <div
                                class="text-[11px] font-semibold text-gray-700"
                            >
                                {{ data.guardianContactPerson || '—' }}
                            </div>
                        </div>
                    </div>
                    <div class="mt-auto text-center">
                        <div
                            class="font-mono text-[8px] tracking-widest text-gray-300"
                        >
                            {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>

                <!-- Gradient Back -->
                <div
                    v-else-if="template === 'gradient'"
                    class="flex size-full flex-col items-center justify-center overflow-hidden rounded-lg"
                    style="
                        background: linear-gradient(
                            180deg,
                            #f5f7fa 0%,
                            #c3cfe2 100%
                        );
                        color: #444;
                        padding: 20px 18px;
                    "
                >
                    <div
                        class="mb-4 w-3/4 border-b-2 border-[#764ba2] pb-2 text-center"
                    >
                        <div
                            class="text-[8px] font-bold tracking-wider text-[#764ba2] uppercase"
                        >
                            {{ data.schoolName }}
                        </div>
                        <div
                            class="text-[5px] tracking-wider text-gray-400 uppercase"
                        >
                            Emergency Contact Information
                        </div>
                    </div>
                    <div class="w-full space-y-3 text-center">
                        <div>
                            <div
                                class="text-[6px] tracking-wider text-gray-500 uppercase"
                            >
                                Contact Number
                            </div>
                            <div class="text-[11px] font-bold text-gray-700">
                                {{ data.contactNumber || '—' }}
                            </div>
                        </div>
                        <div>
                            <div
                                class="text-[6px] tracking-wider text-gray-500 uppercase"
                            >
                                Guardian / Contact Person
                            </div>
                            <div class="text-[11px] font-bold text-gray-700">
                                {{ data.guardianContactPerson || '—' }}
                            </div>
                        </div>
                    </div>
                    <div class="mt-auto text-center">
                        <div
                            class="font-mono text-[7px] tracking-widest text-gray-400"
                        >
                            ID: {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>

                <!-- Professional Back -->
                <div
                    v-else-if="template === 'professional'"
                    class="flex size-full flex-col items-center justify-center overflow-hidden rounded-lg"
                    style="
                        background: #f1f8e9;
                        color: #333;
                        padding: 20px 18px;
                        border: 2px solid #a5d6a7;
                    "
                >
                    <div
                        class="mb-4 w-full border-b border-[#a5d6a7] pb-2 text-center"
                    >
                        <div
                            class="text-[8px] font-bold tracking-wider text-[#1b5e20] uppercase"
                        >
                            {{ data.schoolName }}
                        </div>
                        <div
                            class="text-[5px] tracking-wider text-gray-500 uppercase"
                        >
                            Emergency Contact
                        </div>
                    </div>
                    <div class="w-full space-y-3 text-center">
                        <div>
                            <div
                                class="text-[6px] tracking-wider text-gray-500 uppercase"
                            >
                                Contact Number
                            </div>
                            <div class="text-[11px] font-bold text-[#1b5e20]">
                                {{ data.contactNumber || '—' }}
                            </div>
                        </div>
                        <div>
                            <div
                                class="text-[6px] tracking-wider text-gray-500 uppercase"
                            >
                                Guardian / Contact Person
                            </div>
                            <div class="text-[11px] font-bold text-[#1b5e20]">
                                {{ data.guardianContactPerson || '—' }}
                            </div>
                        </div>
                    </div>
                    <div
                        class="mt-auto w-full border-t border-[#a5d6a7] pt-3 text-center"
                    >
                        <div
                            class="font-mono text-[7px] tracking-widest text-gray-400"
                        >
                            ID: {{ data.studentIdNumber || '1000' }}
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>
