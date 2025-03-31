<template>
  <div class="assign-official-page">
    <!-- 상단: Tournament / Tie / Match / Game -->
    <div class="top-selector">
      <!-- Tournament -->
      <div class="selector-item">
        <label for="tournamentSelect">Tournament</label>
        <select
          id="tournamentSelect"
          class="form-control"
          v-model="selectedTournament"
        >
          <option value="">-- Select Tournament --</option>
          <option
            v-for="t in tournaments"
            :key="t.tournament_uuid"
            :value="t.tournament_uuid"
          >
            {{ t.tournament_title }}
          </option>
        </select>
      </div>

      <!-- Tie Select -->
      <div class="selector-item">
        <label for="tieSelect">Tie</label>
        <select
          id="tieSelect"
          class="form-control"
          v-model="selectedTie"
        >
          <option value="">-- Select Tie --</option>
          <option
            v-for="tieNo in tieOptions"
            :key="tieNo"
            :value="tieNo"
          >
            Tie #{{ tieNo }}
          </option>
        </select>
      </div>

      <!-- Match Select -->
      <div class="selector-item">
        <label for="matchSelect">Match</label>
        <select
          id="matchSelect"
          class="form-control"
          v-model="selectedMatch"
        >
          <option value="">-- Select Match --</option>
          <option
            v-for="m in matchOptions"
            :key="m"
            :value="m"
          >
            Match #{{ m }}
          </option>
        </select>
      </div>

      <!-- Checkbox: "모든 Game에 적용" -->
      <div class="selector-item checkbox-container">
        <label>
          <input
            type="checkbox"
            v-model="applyToAllGames"
          />
          Apply to all 5 games
        </label>
      </div>

      <!-- Game Select (disabled if applyToAllGames = true) -->
      <div class="selector-item">
        <label for="gameSelect">Game</label>
        <select
          id="gameSelect"
          class="form-control"
          v-model="selectedGameUuid"
          :disabled="applyToAllGames"
        >
          <option value="">-- Select Game --</option>
          <!-- gameUuidList를 순회, 사용자에겐 game_no를 표시, 값은 game_uuid -->
          <option
            v-for="g in gameUuidList"
            :key="g.game_uuid"
            :value="g.game_uuid"
          >
            Game #{{ g.game_no }}
          </option>
        </select>
      </div>
    </div>

    <!-- Officials Assignment -->
    <div
      class="official-assignment-container"
      v-if="selectedTournament && selectedTie && selectedMatch && (applyToAllGames || selectedGameUuid)"
    >
      <h2>
        Officials Assignment<br />
        <span v-if="applyToAllGames">(Apply to all 5 Games in Match {{ selectedMatch }})</span>
        <span v-else>Match #{{ selectedMatch }}, Game #{{ selectedGame }}</span>
      </h2>

      <!-- Umpire, Service Judge, Line Judge (등) 테이블 -->
      <table class="official-table">
        <thead>
          <tr>
            <th>Role</th>
            <th>Assigned Official</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <!-- Umpire -->
          <tr>
            <td>Umpire</td>
            <td>
              <span v-if="umpireOfficial">
                {{ umpireOfficial.first_name }} {{ umpireOfficial.family_name }}
              </span>
              <span v-else>Unassigned</span>
            </td>
            <td>
              <button @click="openAssignModal('UMPIRE')">Assign</button>
              <button v-if="umpireOfficial" @click="removeOfficial('UMPIRE')">Remove</button>
            </td>
          </tr>
          <!-- Service Judge -->
          <tr>
            <td>Service Judge</td>
            <td>
              <span v-if="serviceJudgeOfficial">
                {{ serviceJudgeOfficial.first_name }} {{ serviceJudgeOfficial.family_name }}
              </span>
              <span v-else>Unassigned</span>
            </td>
            <td>
              <button @click="openAssignModal('SERVICE_JUDGE')">Assign</button>
              <button v-if="serviceJudgeOfficial" @click="removeOfficial('SERVICE_JUDGE')">Remove</button>
            </td>
          </tr>
          <!-- Line Judge x 4 -->
          <tr v-for="(slot, idx) in lineJudgeSlots" :key="idx">
            <td>Line Judge #{{ idx + 1 }}</td>
            <td>
              <span v-if="slot.official">
                {{ slot.official.first_name }} {{ slot.official.family_name }}
              </span>
              <span v-else>Unassigned</span>
            </td>
            <td>
              <button @click="openAssignModal('LINE_JUDGE', idx)">Assign</button>
              <button v-if="slot.official" @click="removeLineJudge(idx)">Remove</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 하단 버튼 -->
    <div
      class="action-buttons"
      v-if="selectedTournament && selectedTie && selectedMatch && (applyToAllGames || selectedGameUuid)"
    >
      <button @click="saveAssignments" class="save-btn">Save</button>
      <button @click="cancelAssignments" class="cancel-btn">Cancel</button>
    </div>

    <!-- Modal: Official 배정 -->
    <div v-if="showAssignModal" class="modal">
      <div class="modal-content">
        <h3>Assign Official - {{ currentRole }}</h3>
        <label>Select Official</label>
        <select v-model="selectedOfficialUuid">
          <option value="">-- Select --</option>
          <option
            v-for="off in officialList"
            :key="off.official_uuid"
            :value="off.official_uuid"
          >
            {{ off.first_name }} {{ off.family_name }}
          </option>
        </select>
        <div class="button-container">
          <button @click="confirmAssign">Confirm</button>
          <button @click="closeModal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import tourApi from '@/api/tourApi'
import officialApi from '@/api/officialApi'

/** 1) Tournament 목록 및 선택 **/
const tournaments = ref<any[]>([])
const selectedTournament = ref<string>('')

/** 2) Tie / Match **/
const tieInfo = ref<any[]>([])
const tieOptions = ref<number[]>([])
const matchOptions = ref<number[]>([])
const selectedTie = ref('')
const selectedMatch = ref('')
const selectedGame = ref('')

/** Game 목록 (API 호출 결과: game_no, game_uuid 배열) */
const gameUuidList = ref<{ game_no: number; game_uuid: string }[]>([])
const selectedGameUuid = ref<string>('')  // 개별 게임 선택 값
const applyToAllGames = ref<boolean>(false)

/** 4) Official 배정 상태 **/
const umpireOfficial = ref<any>(null)
const serviceJudgeOfficial = ref<any>(null)
const lineJudgeSlots = ref<{official: any|null}[]>([
  { official: null },
  { official: null },
  { official: null },
  { official: null },
])

/** 5) Official 목록 (실제 API 호출 가능) **/
const officialList = ref<any[]>([
  { official_uuid: '1111', first_name: 'Иван', family_name: '이바노프' },
  { official_uuid: '2222', first_name: 'NUR', family_name: 'ZULAIKHA' },
  { official_uuid: '3333', first_name: '홍',  family_name: '길동' },
])

/** 6) 모달 제어 **/
const showAssignModal = ref(false)
const currentRole = ref('')
const currentSlotIndex = ref<number|null>(null)
const selectedOfficialUuid = ref('')

/** ========== onMounted: Tournament 목록 불러오기 ========== **/
onMounted(async () => {
  try {
    const tourRes = await tourApi.getTourList()
    tournaments.value = tourRes.data // [{ tournament_uuid, tournament_title, ... }]
  } catch (error) {
    console.error("Failed to load tournaments:", error)
  }
})

/** watch: tie -> matchOptions 업데이트 */
watch(selectedTie, (newVal) => {
  selectedMatch.value = ''
  matchOptions.value = []
  gameUuidList.value = []
  selectedGameUuid.value = ''

  const found = tieInfo.value.find(item => item.tie_no === newVal)
  if (found) {
    matchOptions.value = found.match_no
  }
})

/** watch: match -> gameUuidList 업데이트 */
watch(selectedMatch, async (newVal) => {
  selectedGameUuid.value = ''
  gameUuidList.value = []
  if (!selectedTournament.value || !selectedTie.value || !newVal) {
    return
  }
  // API 호출: /api/gameuuids?tournament_uuid=xxx&tie_no=yyy&match_no=zzz
  try {
    const res = await officialApi.getGmaeuuids({
      tournament_uuid: selectedTournament.value,
      tie_no: selectedTie.value,
      match_no: newVal
    })
    gameUuidList.value = res.data.game_uuids
  } catch (err) {
    console.error("Failed to load gameUuids:", err)
  }
})

/** ========== watch: selectedTournament 변경 시 ========== **/
watch(selectedTournament, async (newVal) => {
  // 초기화
  tieInfo.value = []
  tieOptions.value = []
  matchOptions.value = []
  selectedTie.value = ''
  selectedMatch.value = ''
  applyToAllGames.value = false
  selectedGame.value = ''

  if (!newVal) {
    // 선택 취소됨
    return
  }

  try {
    // tournament_uuid를 params에 전달
    const res = await officialApi.getGameTies({ tournament_uuid: newVal })
    tieInfo.value = res.data.tie_info || []
    tieOptions.value = tieInfo.value.map(t => t.tie_no)

    // 첫 Tie 자동 선택 (옵션)
    if (tieInfo.value.length > 0) {
      const firstTie = tieInfo.value[0]
      selectedTie.value = firstTie.tie_no
      matchOptions.value = firstTie.match_no
    }
  } catch (err) {
    console.error("Failed to load tie/match:", err)
  }
})

/** ========== watch: applyToAllGames 변경 시 ========== **/
watch(applyToAllGames, (newVal) => {
  if (newVal) {
    // 체크되면 Game Select를 disable => selectedGame 초기화
    selectedGame.value = ''
  }
})

/** ========== 공식 메서드들 ========== **/

function openAssignModal(role: string, slotIdx: number|null = null) {
  currentRole.value = role
  currentSlotIndex.value = slotIdx
  selectedOfficialUuid.value = ''
  showAssignModal.value = true
}

function closeModal() {
  showAssignModal.value = false
  currentRole.value = ''
  currentSlotIndex.value = null
  selectedOfficialUuid.value = ''
}

function confirmAssign() {
  const chosen = officialList.value.find(o => o.official_uuid === selectedOfficialUuid.value)
  if (!chosen) return

  if (currentRole.value === 'UMPIRE') {
    umpireOfficial.value = chosen
  } else if (currentRole.value === 'SERVICE_JUDGE') {
    serviceJudgeOfficial.value = chosen
  } else if (currentRole.value === 'LINE_JUDGE' && currentSlotIndex.value !== null) {
    lineJudgeSlots.value[currentSlotIndex.value].official = chosen
  }
  closeModal()
}

function removeOfficial(role: string) {
  if (role === 'UMPIRE') {
    umpireOfficial.value = null
  } else if (role === 'SERVICE_JUDGE') {
    serviceJudgeOfficial.value = null
  }
}

function removeLineJudge(idx: number) {
  lineJudgeSlots.value[idx].official = null
}

function saveAssignments() {
  if (!selectedTie.value || !selectedMatch.value) {
    alert("Tie/Match is not selected.")
    return
  }
  if (!applyToAllGames.value && !selectedGame.value) {
    alert("Select game or check 'Apply to all 5 games'.")
    return
  }

  if (applyToAllGames.value) {
    alert(`Saving all 5 games for Tie ${selectedTie.value}, Match ${selectedMatch.value}`)
  } else {
    alert(`Saving single game ${selectedGame.value} for Tie ${selectedTie.value}, Match ${selectedMatch.value}`)
  }
  // 실제 API 호출 로직 작성
}

function cancelAssignments() {
  alert("Cancelled")
}
</script>

<style scoped>
.assign-official-page {
  position: absolute;
  width: 800px;
  margin: 0 auto;
  padding: 16px;
  left: 50%;
  transform: translate(-50%);
}

.top-selector {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.selector-item {
  display: flex;
  flex-direction: column;
}

.form-control {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.checkbox-container {
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.official-assignment-container {
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
}

.official-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
.official-table th, .official-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

/* 하단 버튼 */
.action-buttons {
  text-align: right;
  margin: 10px 0;
}
.save-btn,
.cancel-btn {
  padding: 8px 20px;
  margin-left: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* 모달 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background-color: #fff;
  width: 400px;
  padding: 20px;
  border-radius: 6px;
}
.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
  gap: 10px;
}
</style>
