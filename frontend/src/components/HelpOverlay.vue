<script setup>
import { ref, nextTick, defineExpose } from 'vue';

const visible = ref(false);
const items   = ref([]);

async function collect() {
  await nextTick();                 // router‑view DOM 완료 대기

  items.value = [...document.querySelectorAll('[data-guide]')].map(el => {
    const { top, left } = el.getBoundingClientRect();
    return {
      step : el.dataset.step ?? '',
      guide: el.dataset.guide ?? '',
      width: el.dataset.guidew ?? el.dataset.width ?? '',
      top  : top  + window.scrollY,
      left : left + window.scrollX,
    };
  });
}

async function open()  { await collect(); visible.value = true; }
function close()        { visible.value = false; }

defineExpose({ open, close });
</script>

<template>
  <div v-if="visible" class="overlay-backdrop" @click.self="close">
    <div
      v-for="i in items"
      :key="i.step"
      class="overlay-item"
      :style="{ top: i.top + 'px', left: i.left + 'px' }"
    >
      <span class="bubble-number">{{ i.step }}</span>
      <span class="bubble-text"
            :style="{ maxWidth: i.width ? i.width + 'px' : '300px' }"
            v-html="i.guide.replace(/(\r?\n|\r)/g, '<br>')"></span>
    </div>
  </div>
</template>

<style scoped>
/* 전체 배경 */
.overlay-backdrop{
  position: fixed;
  inset: 0;                         /* top/right/bottom/left 0 */
  background: rgba(0,0,0,.4);
  z-index: 2000;
}

/* 각 아이템(말풍선) 컨테이너 */
.overlay-item{
  position: absolute;
  display: flex;
  align-items: center;
  font-size: 14px;
  user-select: none;
}

/* 숫자 원 */
.bubble-number{
  width: 26px; height: 26px;
  margin-right: 6px;
  border-radius: 50%;
  background:#14B8A6;              /* Teal 500 */
  color:#fff; font-weight: 700;
  display:flex;align-items:center;justify-content:center;
}

/* 설명 텍스트 */
.bubble-text{
  background: rgba(255,255,255,.9);
  padding: 4px 8px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,.15);
  max-width: 260px;                /* 길면 줄바꿈 */
  line-height: 1.3;
}
</style>
