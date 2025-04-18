<script setup lang="ts">
import { defineEmits, ref } from 'vue'

const emit = defineEmits<{
  (e: 'select', cell: number): void
}>()

const selected = ref<number | null>(null)

function pick(n: number) {
  selected.value = n
  emit('select', n)
}

const rowHeights = [8, 20, 20, 20, 24, 8]
const colWidths   = [10, 40, 40, 10]

const xLines:number[]=[], yLines:number[]=[]
let accX=60, accY=40            // 외곽 시작점
colWidths.slice(0,-1).forEach(w=>{
  accX += (w/100)*480           // 480 = 내부 폭
  xLines.push(accX)             // 세로선 3개
})

rowHeights.slice(0,-1).forEach(h=>{
  accY += (h/100)*370           // 370 = 내부 높이
  yLines.push(accY)             // 가로선 5개
})

const cells: any[] = []
const idToView: Record<number, number> = {
  /* A코트 */            /* B코트 */
   1: 11,   2:  5,        15: 11,  16: 5,
   3:  6,   4:  12,       17:  6,  18: 12,
   5:  7,   6:  1,        19:  9,  20: 1,
   7:  2,   8:  8,        21:  2,  22: 10,
   9:  9,  10:  3,        23:  7,  24: 3,
  11: 4,   12: 10,        25:  4,  26: 8,
  /* 네트 번호 */
  13: 13,  14: 14,
  27: 13,  28: 14,
}

/* A코트 1‥12 (행 0~2, 열 0~3) */
for (let r=0; r<3; r++)
  for (let c=0; c<4; c++)
    cells.push(makeCell(r*4+c+1, r, c, 'A', r*4+c+1))

/* ─ 네트 번호 ─ */
const netY = yLines[2]
/* A코트 네트 왼쪽 두 칸 (1열,2열) */
cells.push(
  { id: 13, view: 13, x: colCenter(1) + 40, y: netY+10, court:'NETA' },
  { id: 14, view: 14, x: colCenter(2) + 40, y: netY+10, court:'NETA' },
)
/* B코트 네트 오른쪽 두 칸 (3열,4열) */
cells.push(
  { id: 27, view: 14, x: colCenter(1) - 40, y: netY-10, court:'NETB' },
  { id: 28, view: 13, x: colCenter(2) - 40, y: netY-10, court:'NETB' },
)

/* B코트 15‥26 (행 5~3, 열 3~0 역순) */
let id = 15
let viewNum = 1
for (let r = 5; r >= 3; r--) {     // 행 6 → 4
  for (let c = 3; c >= 0; c--) {   // 열 4 → 1  (역방향)
    cells.push(makeCell(id++, r, c, 'B', viewNum++))
  }
}

function makeCell(realId:number, r:number, c:number,
                  court:'A'|'B', view:number){
  const cxPct = colWidths.slice(0,c).reduce((a,b)=>a+b,0)+colWidths[c]/2
  const cyPct = rowHeights.slice(0,r).reduce((a,b)=>a+b,0)+rowHeights[r]/2
  return {
    id: realId,   // 내부 고유 id (서버·선택 구분용)
    view: idToView[realId],  // 화면에 표기될 번호
    court,
    x: 60 + cxPct/100*480,
    y: 40 + cyPct/100*370
  }
}

function colCenter(c:number){
  return 60+(colWidths.slice(0,c).reduce((a,b)=>a+b,0)+colWidths[c]/2)/100*480
}
</script>

<template>
  <svg
    viewBox="0 0 600 450"
    class="w-[560px] mx-auto border-[6px] border-[#01579B] bg-yellow-300 p-4"
  >
    <!-- 녹색 그라디언트 배경 -->
    <defs>
      <linearGradient id="courtGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%"  stop-color="#006400"/>
        <stop offset="100%" stop-color="#014d01"/>
      </linearGradient>
    </defs>
    <rect x="0" y="0" width="600" height="450" fill="url(#courtGrad)" />
    <!-- A 코트: 라이트 그린 -->
    <rect x="60" y="40"  width="480" height="186" fill="#0FA34A"/>
    <!-- B 코트: 다크 그린 -->
    <rect x="60" y="226" width="480" height="184" fill="#0B6623"/>
    <!-- 코트 라인들 -->
    <g stroke="#fff" stroke-width="3">
      <rect x="60" y="40" width="480" height="370" fill="none"/>
      <!-- 세로선 -->
      <line v-for="x in xLines" :key="'v'+x" :x1="x" y1="40" :x2="x" y2="410"/>
      <!-- 가로선 -->
        <g stroke="#fff" stroke-width="3">
          <line v-for="y in yLines" :key="'h'+y" x1="60" :y1="y" x2="540" :y2="y"/>
        </g>
        <!-- ─── 네트 강조선 (4번째 행) ─── -->
        <line
          :y1="yLines[2]" :y2="yLines[2]"
          x1="60" x2="540"
          stroke="#01579B"
          stroke-width="6"
          stroke-dasharray="12 6"
        />
      <text x="300" y="110" fill="#ffffff" font-size="28" font-weight="700"
            text-anchor="middle">A 코트</text>
      <text x="300" y="355" fill="#ffffff" font-size="28" font-weight="700"
            text-anchor="middle">B 코트</text>
    </g>
    <template v-for="cell in cells" :key="cell.id">
      <circle
        :cx="cell.x" :cy="cell.y" r="16"
        :fill="selected===cell.id
          ? 'var(--color-accent)'
          : cell.court==='A'
              ? 'rgba(255,255,255,0.28)'
              : cell.court==='B'
                  ? 'rgba(0,0,0,0.35)'
                  : cell.court==='NETA'
                      ? 'rgba(255,255,255,0.28)'
                      : 'rgba(0,0,0,0.35)'"
        class="cursor-pointer transition"
        @click="pick(cell.id)"
      />
      <text
        :x="cell.x" :y="cell.y"
        :fill="cell.court==='B'||cell.court==='NETB' ? '#FFE28A' : '#FFFFFF'"
        pointer-events="none"
      >
        {{ cell.view }}
      </text>
    </template>
  </svg>
</template>
