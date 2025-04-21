<script setup lang="ts">
import { ref, defineProps, defineEmits, watch } from 'vue'

/**
 * RallyToolbar.vue — Tailwind CSS 4.x, <dialog> API 호환 개선
 * – dialogOpen 값을 watch 하여 showModal()/close() 호출
 * – v-if 제거 → DOM 상시 존재, 브라우저 지원 안 될 때 open 속성으로 대체
 * – 더하기/빼기 1씩 증감, 큰 버튼, 흰색 아이콘, ⋯ 버튼 모달
 */

// ───────────── Props / Emits ─────────────
const props = defineProps<{ modelValue: number }>()
const emit  = defineEmits<{
  (e: 'update:modelValue', v: number): void
  (e: 'inc'): void
  (e: 'dec'): void
}>()

// ───────────── State ─────────────
const dialogOpen = ref(false)
const dialogRef  = ref<HTMLDialogElement | null>(null)
const temp       = ref(props.modelValue)

// 외부 변경 ↔︎ temp 동기화 (모달 열려 있을 땐 유지)
watch(() => props.modelValue, v => {
  if (!dialogOpen.value) temp.value = v
})

// dialogOpen 플래그 → 실제 <dialog> 표시 제어
watch(dialogOpen, v => {
  const dlg = dialogRef.value
  if (!dlg) return

  try {
    if (v) {
      // 브라우저 지원 시 modal, 아니면 open 속성
      dlg.showModal?.() ?? dlg.setAttribute('open', '')
    } else {
      dlg.close?.()
      dlg.removeAttribute('open')
    }
  } catch {
    /* Safari polyfill etc. */
    if (v) dlg.setAttribute('open', '')
    else dlg.removeAttribute('open')
  }
})

// ───────────── Handlers ─────────────
function inc() {
  emit('update:modelValue', props.modelValue)
  emit('inc')
}

function dec() {
  if (props.modelValue === 0) return
  emit('update:modelValue', props.modelValue)
  emit('dec')
}

function applyManual() {
  if (temp.value < 0) temp.value = 0
  emit('update:modelValue', temp.value)
  dialogOpen.value = false
}
</script>

<template>
  <div class="w-full py-2 relative flex justify-center items-center">
    <!-- - 숫자 + 그룹 (완전 중앙) -->
    <div class="flex items-center gap-6"
         data-step="5"
         :data-guide="[
            '랠리 합계를 ',
            '+ / – 로 입력합니다.'
            ].join('\n')"
    >
      <!-- – 버튼 -->
      <button
        @click="dec"
        class="flex items-center justify-center w-28 h-12 rounded-lg bg-indigo-500 hover:bg-indigo-600 text-white text-2xl font-bold select-none active:scale-95 transition-transform">
        –
      </button>

      <!-- 현재 랠리 수 -->
      <span class="font-mono text-3xl w-24 text-center select-none">{{ modelValue }}</span>

      <!-- + 버튼 -->
      <button
        @click="inc"
        class="flex items-center justify-center w-28 h-12 rounded-lg bg-indigo-500 hover:bg-indigo-600 text-white text-2xl font-bold select-none active:scale-95 transition-transform"
      >
        +
      </button>
    </div>

    <!-- ⋯ 수동 입력 (우측 끝) -->
    <button
      v-if="true"
      @click="dialogOpen = true"
      class="absolute  flex items-center justify-center w-12 h-12 rounded-full border border-indigo-400 text-indigo-600 text-xl select-none active:scale-95 transition-transform"
        data-step="6"
      :data-left="20"
      :data-guide="[
            '숫자를 직접 입력하려면 클릭하세요.'
            ].join('\n')"
    >
    </button>

    <!-- 숫자 직접 입력 모달 -->
    <dialog ref="dialogRef" class="p-6 rounded-lg shadow-lg backdrop:bg-black/30">
      <form @submit.prevent="applyManual" class="flex flex-col gap-4 w-52">
        <h3 class="text-sm font-medium text-center">랠리 합계 직접 입력</h3>
        <input type="number" min="0" v-model.number="temp"
               class="border rounded px-3 py-2 text-center" />
        <button type="submit" class="bg-indigo-500 hover:bg-indigo-600 text-white py-2 rounded">적용</button>
        <button type="button" @click="dialogOpen = false" class="text-gray-500 py-1">취소</button>
      </form>
    </dialog>
  </div>
</template>

<style scoped>
:where(dialog[open]) {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: none;
}
</style>
