<script setup lang="ts">
import '@/assets/tailwind.css'
import TeamBlock from '@/components/score/TeamBlock.vue'
import CourtGrid from '@/components/score/CourtGrid.vue'
import EventDrawer from '@/components/score/EventDrawer.vue'
import RallyToolbar  from "@/components/score/RallyToolbar.vue";
import { ref } from 'vue'

const tournament  = '2025 BXL Singapore'

const matchNo     = 1
const warmUp      = '00:00'
const matchType   = '남자 단식'     // 예: 남자 단식 · 혼합 복식 · 3 × 3 …

const teamAPlayers   = ['홍길동', '김선수', '박선수']  // 최대 3명
const teamBPlayers   = ['이길동', '최선수']
const gameA       = 0

const gameB       = 0

const activeGame   = 1   // 1‥4  (진행 중인 Gm 번호)
const sdActive     = true
const ssActive     = true

const rallyCount = ref(0)

/* Drawer 상태 */
const drawerOpen = ref(false)
const selectedArea = ref<number | null>(null)

/* ➜ CourtGrid 와 동일한 매핑 */
const idToView: Record<number, number> = {
  /* A 코트 */          /* B 코트 */
   1:11,  2:5,  3:6,  4:12,  5:7,  6:1,
   7:2,   8:8,  9:9, 10:3, 11:4, 12:10,
  15:11, 16:5, 17:6, 18:12, 19:9, 20:1,
  21:2,  22:10,23:7, 24:3, 25:4, 26:8,
  /* 네트 */
  13:13, 14:14, 27:13, 28:14,
}

type LogRow = {
  ts: string
  match: number
  game: number
  cause: string
  shot: string
  area: number
  view: number
}


const hovered = ref<number|null>(null)

/* ─ 로그 상태, 토글 ─ */
const logs = ref<
  { ts:string; match:number; game:number;
    cause:string; shot:string; area:number; view:number }[]
>([])

const logOpen = ref(true)

function decRally() {
  if ( rallyCount.value > 0 ) rallyCount.value--
}

/* 미니맵 클릭 → Drawer 오픈 */
function onSelect(cell: number) {
  selectedArea.value = cell
  drawerOpen.value = true
}

/* 저장 콜백 */
function onSave(p:{cause:string; shot:string; area:number}){
  logs.value.unshift({
    ts   : new Date().toLocaleTimeString('ko-KR',{hour12:false}),
    match: matchNo,          // ← 현재 매치 번호
    game : activeGame,       // ← 진행 중인 Gm 번호
    cause: p.cause,
    shot : p.shot,
    area : p.area,
    view : idToView[p.area] ?? p.area
  })
}

/* 토글 핸들러 */
function toggleLog(){ logOpen.value = !logOpen.value }

const editedIdx = ref<number | null>(null)

function applyLog(row:LogRow, idx:number){
  editedIdx.value = idx
  // TODO: 이 로그를 화면 상태로 반영
}

function rowClass(idx: number) {
  return [
    'transition-colors',          // 부드러운 색 전환
    'hover:bg-gray-50',           // 마우스 오버 색
    hovered.value === idx    ? 'bg-gray-100 cursor-pointer' : '',
    editedIdx.value === idx  ? 'bg-[--color-brand-600]/20'  : '',
    idx === 0                ? 'bg-purple-100'              : '',
  ]
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-app text-app pt-8">
    <div class="w-full flex justify-center">
      <div class="w-full max-w-6xl px-4 space-y-8">

        <!-- 대회 메타 -->
        <section class="space-y-4 bg-white/60 backdrop-blur rounded-xl px-6 py-4"
                 data-step="1"
                 data-guide="대회 정보 및 경기 정보"
        >
          <h1 class="text-center font-semibold text-xl text-[--color-brand-600]">
            {{ tournament }}
          </h1>

          <div class="flex justify-center gap-8 text-lg font-semibold">
            <span>Match No.{{ matchNo }}</span>
            <span>Warm‑Up&nbsp;{{ warmUp }}</span>
          </div>
        </section>

        <div class="text-center !mt-6 ">
          <span class="inline-block bg-[--color-brand-50] text-[--color-brand-600]
                       px-4 py-1 rounded-full text-sm font-medium tracking-wide">
            {{ matchType }}
          </span>
        </div>


        <!-- 스코어 / 선수 블록 -->
        <section class="grid grid-cols-3 items-center gap-8"
                 data-step="2"
                 data-guide="팀 점수 / MATCH의 포인트 / 게임 스코어 선수 등 정보를 CODER 쪽에서 전달 받음 "
        >
          <!-- 팀 A : 왼쪽 정렬 -->
          <TeamBlock
            label="팀 A"
            :players="teamAPlayers"
            :point="0"
            :game="0"
            align="center"
            playersSide="left"
          />
          <!-- 세트 스코어 -->
          <div class="flex flex-col items-center justify-center mb-4">
            <p class="text-5xl font-bold text-[--color-accent]">
              {{ gameA }}‑{{ gameB }}
            </p>
          </div>

          <!-- 팀 B -->
          <TeamBlock
            label="팀 B"
            :players="teamBPlayers"
            :point="0"
            :game="0"
            align="center"
            playersSide="right"
          />
        </section>

        <!-- Game & Mode 버튼 영역 ------------------------------------ -->
        <section class="flex flex-wrap justify-center gap-4"
        >

          <!-- Gm1~4 버튼 -->
          <button
            v-for="(n, idx ) in 4"
            :key="`gm${n}`"
            class="h-10 w-20 rounded-md font-medium select-none transition
                   bg-gray-300 text-gray-600"
            :class="{
              'bg-[--color-brand-600] text-white': n === activeGame
            }"
                 :data-step="3"
                 :data-guide="idx === 0 ? '현재 진행중인 게임 정보' : null"
          >
            Gm&nbsp;{{ n }}
          </button>

          <button
            :class="[
              'h-10 w-20 rounded-md font-medium select-none transition',
              sdActive
                ? 'bg-[var(--color-accent)] text-white'
                : 'bg-gray-300 text-gray-600'
            ]"
            data-step="4"
            data-guide="서든데스와 셔틀콕 셧다운 상태인지 노출 "
          >
            SD
          </button>

          <button
            :class="[
              'h-10 w-20 rounded-md font-medium select-none transition',
              ssActive
                ? 'bg-emerald-500 text-white'
                : 'bg-gray-300 text-gray-600'
            ]"
          >
            SS
          </button>
        </section>
      </div>
    </div>
    <div class="!mt-4">
        <!-- Rally Toolbar (NEW) -->
        <RallyToolbar
          v-model="rallyCount"
          @inc="rallyCount++"
          @dec="decRally"
        />
    </div>
    <div class="flex flex-col md:flex-row gap-8 items-start justify-center !mt-4">
      <div class="flex flex-col md:flex-row gap-8 items-start mx-auto max-w-6xl">
        <!-- 왼쪽 : Shot 패널 -->
        <EventDrawer
          :open="drawerOpen"
          :area="selectedArea"
          @save="onSave"
          @close="drawerOpen = false"
          class="w-full md:w-72 shrink-0"   />

        <!-- 오른쪽 : 득점 Area + 코트 -->
        <CourtGrid
          class="mt-2 w-[560px] shrink-0"
          @select="onSelect"
          data-step="10"
          :data-guide="[
            '코트에서 셔틀콕이 떨어진 위치에 해당하는',
            '번호를 클릭핫네요'
            ].join('\n')"
        />
      </div>
    </div>
    <!-- 로그 영역 ----------------------------------------------------- -->
    <div class="flex flex-col md:flex-row gap-8 items-start justify-center !mt-4">
    <section class="mt-6 w-full max-w-6xl mx-auto">
      <!-- 헤더 + 토글 버튼 -->
      <div class="flex items-center gap-4 mb-2">
        <h3 class="font-semibold text-lg">입력 로그</h3>
        <button @click="toggleLog"
                class="px-2 py-1 text-sm rounded
                       bg-[var(--color-brand-600)] text-white">
          {{ logOpen ? '숨기기' : '열기' }}
        </button>
      </div>

      <!-- 표(보이기/숨기기) -->
      <transition name="fade">
<table class="w-full text-sm border-collapse">
  <thead class="bg-[var(--color-brand-600)] text-white">
    <tr>
      <th class="w-12">No</th>
      <th class="w-20">시간</th>
      <th class="w-14">매치</th>   <!-- ★ -->
      <th class="w-14">게임</th>   <!-- ★ -->
      <th class="text-left px-2">득점 원인 / 샷</th>
      <th class="w-14">Area</th>
      <th class="w-14"></th>
    </tr>
  </thead>

  <tbody v-show="logOpen">
    <tr v-for="(l,idx) in logs" :key="idx"
        @mouseover="hovered = idx" @mouseleave="hovered = null"  :class="rowClass(idx)"
        class="hover:bg-gray-50 transition-colors"
    >
      <td class="text-center">{{ logs.length - idx }}</td>
      <td class="text-center font-mono text-xs">{{ l.ts }}</td>
      <td class="text-center">{{ l.match }}</td>         <!-- ★ -->
      <td class="text-center">{{ l.game }}</td>          <!-- ★ -->
      <td class="px-2">
        <span class="font-semibold">{{ l.cause }}</span>
        <span class="text-gray-500"> · {{ l.shot }}</span>
      </td>
      <td class="text-center font-semibold">{{ l.view }}</td>
      <!-- 🔗 빈 링크 · 클릭 시 applyLog 호출 -->
      <td class="text-center">
        <a href="#" @click.prevent="applyLog(l)"
           class="text-[--color-brand-600] underline">수정</a>
      </td>
    </tr>

    <tr v-if="!logs.length">
      <td colspan="6" class="text-center py-6 text-gray-400">
        아직 입력된 이벤트가 없습니다
      </td>
    </tr>
  </tbody>
</table>

      </transition>
    </section>

    </div>
  </div>

</template>




<style scoped>

</style>
