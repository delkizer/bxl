<script setup lang="ts">
import { ref, watch } from 'vue'

/* 전달: area(코트 셀) */
const props = defineProps<{ area: number | null }>()

const emit = defineEmits<{
  (e:'save', data:{cause:string;shot:string;area:number}): void
}>()

/* 상태 */
const cause = ref<string|null>(null)
const shot  = ref<string|null>(null)

const causeList = ['공격 성공','상대 공격실패','상대 리턴실패']
const shotList  = [
  '스매시','하이 클리어','드롭','푸쉬',
  '언더 클리어','헤어핀','드라이브','서브에이스'
]

function reset(){ cause.value=null; shot.value=null }
function save(){
  if (cause.value && shot.value && props.area)
    emit('save',{ cause:cause.value, shot:shot.value, area:props.area })
    // 저장 후 초기화해도 되고 유지해도 됨
}

/* area 가 바뀌면 자동 초기화 */
watch(()=>props.area, reset)
</script>

<template>
  <!-- 사이드 카드 -->
  <aside class="bg-yellow-300 border-[6px] border-[#01579B]
                p-4 flex flex-col gap-4 w-full md:w-72">

    <!-- 득점 원인 -->
    <div class="flex md:flex-col gap-4">
      <button v-for="c in causeList" :key="c"
        @click="cause=c"
        class="flex-1 h-20 md:h-24 border-[4px] border-[#01579B]
               text-xl font-semibold whitespace-pre-line"
        :class="cause===c ?'bg-red-600 text-white':'bg-white hover:bg-gray-100'">
        {{ c }}
      </button>
    </div>

    <!-- 샷 종류 -->
    <div class="bg-lime-400/70 p-3 flex flex-col gap-3">
      <div class="grid grid-cols-2 gap-3">
        <button v-for="s in shotList" :key="s"
          @click="shot=s"
          class="h-12 border-[3px] border-[#01579B] font-medium whitespace-pre-line"
          :class="shot===s ?'bg-red-600 text-white':'bg-white hover:bg-gray-100'">
          {{ s }}
        </button>
      </div>

      <!-- 저장 -->
      <button
        class="h-10 mt-2 border-[4px] border-[#01579B]
               bg-red-600 text-white disabled:opacity-40"
        :disabled="!(cause&&shot&&props.area)"
        @click="save">
        확인
      </button>
    </div>
  </aside>
</template>
