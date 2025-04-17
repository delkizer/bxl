<script setup>
import { ref } from 'vue';
import HelpOverlay from '@/components/HelpOverlay.vue';

const help = ref(null);

function toggleHelp() {
  help.value?.open();          // open() 노출된 메서드 호출
}
</script>

<template>
  <router-view />

  <!-- ❔ 토글 버튼 (우측 하단) -->
  <button class="help-toggle" @click="toggleHelp">❔</button>

  <!-- 오버레이 -->
  <HelpOverlay ref="help" />
</template>

<style>
/* ===== 전역 reset (필요 없으면 제거) ===== */
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial, sans-serif;}
html,body{height:100%;background:#f0f4f8;}

/* ===== 고정 도움말 버튼 ===== */
.help-toggle{
  position:fixed;bottom:1.5rem;right:1.5rem;z-index:40;
  width:44px;height:44px;border:none;border-radius:50%;
  font-size:20px;font-weight:700;color:#fff;background:#14B8A6;
  box-shadow:0 2px 6px rgba(0,0,0,.2);
  cursor:pointer;transition:opacity .15s,transform .15s;
}
.help-toggle:hover{opacity:.9}
.help-toggle:active{transform:scale(.95)}
</style>
