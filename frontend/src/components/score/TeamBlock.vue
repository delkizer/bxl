<script setup lang="ts">
defineProps<{
  label: string          // 팀 A, 팀 B
  players: string[]      // 선수 이름 배열 (최대 3명)
  point: number
  game: number
  align?: 'left' | 'right' | 'center'  // 정렬 옵션
  playersSide?: 'left' | 'right' | 'center'  // 선수 위치 옵션 (기본 left)
}>()
</script>

<template>
  <div
    :class="[
      'flex flex-col gap-2',
      align === 'right'
        ? 'items-end text-right'
        : align === 'center'
        ? 'items-center text-center'
        : 'items-start text-left'
    ]"
  >
    <h2 class="text-sm font-semibold">{{ label }}</h2>

    <!-- 점수와 선수 목록을 한 줄에 나란히 배치 -->
    <div
      class="flex gap-4"
      :class="{
        'flex-row-reverse': align === 'right',   /* B팀이면 순서 뒤집기 */
        'justify-center':  align === 'center'
      }"
    >
      <!-- 선수 명단 -->
      <ul
        v-if="playersSide === 'right'"
        class="space-y-1 text-sm font-medium self-center pr-3
               border-r border-[--color-brand-100]"
      >
        <li v-for="p in players" :key="p">{{ p }}</li>
      </ul>

      <!-- POINT / GAME 카드 -->
      <div class="flex gap-6 text-center">
        <div>
          <p class="text-[10px] opacity-70 mb-0.5">POINT</p>
          <p class="text-3xl font-bold">{{ point }}</p>
        </div>
        <div>
          <p class="text-[10px] opacity-70 mb-0.5">GAME</p>
          <p class="text-3xl font-bold">{{ game }}</p>
        </div>
      </div>

      <!-- 오른쪽 선수 명단 -->
      <ul
        v-if="playersSide === 'left'"
        class="space-y-1 text-sm font-medium self-center pl-3
               border-l border-[--color-brand-100]"
      >
        <li v-for="p in players" :key="p">{{ p }}</li>
      </ul>


    </div>
  </div>
</template>
