<template>
  <div class="assign-official-page">
    <!-- 상단: Tournament / Tie / Match -->
    <div class="top-selector">
      <!-- Tournament -->
      <div class="selector-item">
        <label for="tournamentSelect">Tournament</label>
        <select
          id="tournamentSelect"
          class="form-control"
          v-model="selectedTournament" disabled
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
          v-model="selectedTie" disabled
        >
          <option value="">-- Select Tie --</option>
          <option
            v-for="tieNo in tieOptions"
            :key="tieNo"
            :value="tieNo.toString()"
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
    </div>
    <div class="top-selector">
      <!-- 나머지: 체크박스 + Game Select -->
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
      <!-- 체크박스 -->
      <div class="selector-item checkbox-container">
        <label>
          <input type="checkbox" v-model="applyToAllGames"/>
          Apply to all 5 games
        </label>
      </div>
      <div class="selector-item checkbox-container">
        <!-- clear 버튼 -->
        <button class="btn-clear" @click="clearAssignments">Clear</button>
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
        <span v-else>Match #{{ selectedMatch }}, Game #{{ selectedGameNo }}</span>
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
      <button @click="openSaveModal" class="save-btn">Save</button>
      <button @click="openCancelModal" class="cancel-btn">Cancel</button>
    </div>

    <!-- Modal: Official 배정 -->
<div v-if="showAssignModal" class="modal" @click.self="closeModal">
  <div class="modal-content" @click.stop>
    <h3>Assign Official - {{ currentRole }}</h3>
    <!-- (A) Officials 표 -->
    <div class="table-scroll-container">
      <table class="official-list-table">
        <thead>
        <tr>
          <th></th>
          <th>First Name</th>
          <th>Family Name</th>
          <th>Nickname</th>
          <th>Nation</th>
        </tr>
        </thead>
        <tbody>
        <tr
          v-for="off in officialList"
          :key="off.official_uuid"
          @click="rowClick(off.official_uuid)"
          :class="{
            'selected-row': selectedOfficialUuid === off.official_uuid, 'assigned-row': isAssigned(off.official_uuid)
          }"
        >
          <td>
            <!-- 라디오 버튼 (name="officialSelect" 동일) -->
            <input
              type="radio"
              name="officialSelect"
              :value="off.official_uuid"
              v-model="selectedOfficialUuid"
              :disabled="isAssigned(off.official_uuid)"
              @click.stop
            />
          </td>
          <td>{{ off.first_name }}</td>
          <td>{{ off.family_name }}</td>
          <td>{{ off.nickname }}</td>
          <td>{{ off.nation_code }}</td>
        </tr>
        </tbody>
      </table>
    </div>
    <div class="button-container">
      <button @click="closeModal">Close</button>
    </div>
  </div>
</div>
<!-- (A) 저장 확인 모달 -->
<ConfirmationModal
  :visible="showSaveConfirmModal"
  title="저장 확인"
  message="저장을 진행하시겠습니까?"
  confirmButtonLabel="확인"
  cancelButtonLabel="취소"
  @confirm="handleSaveConfirm"
  @cancel="handleSaveCancel"
/>

<ConfirmationModal
  :visible="showCancelConfirmModal"
  title="종료 확인"
  message="메인으로 이동하시겠습니까?"
  confirmButtonLabel="확인"
  cancelButtonLabel="취소"
  @confirm="handleCancelConfirm"
  @cancel="handleCancelCancel"
/>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter} from "vue-router";
import { useCoderStore } from '@/stores/coder';
import tourApi from '@/api/tourApi'
import officialApi from '@/api/officialApi'
import coderApi from '@/api/coderApi';
import ConfirmationModal from "@/components/modal/Confirmation.vue";

const router = useRouter()
const coderStore = useCoderStore()

const showSaveConfirmModal = ref(false)
const showCancelConfirmModal = ref(false)

/** 1) Tournament 목록 및 선택 **/
const tournaments = ref<any[]>([])
const selectedTournament = ref<string>('')

/** 2) Tie / Match **/
const selectedTie = ref<string>('')
const tieOptions = ref<number[]>([])

const selectedMatch = ref<number | ''>('')
const matchOptions = ref<number[]>([])

const gameUuidList = ref<{ game_no: number; game_uuid: string }[]>([])
const selectedGameUuid = ref<string>('')
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
const officialList = ref<any[]>([])

/** 6) 모달 제어 **/
const showAssignModal = ref(false)
const currentRole = ref('')
const currentSlotIndex = ref<number|null>(null)
const selectedOfficialUuid = ref('')

const selectedGameNo = computed(() => {
  // gameUuidList: [{ game_no, game_uuid }, ...]
  const found = gameUuidList.value.find(g => g.game_uuid === selectedGameUuid.value)
  return found ? found.game_no : ''
})

const assignedOfficialUuids = computed( () => {
  const list: string[] = []

  // 1) Umpire
  if (umpireOfficial.value && umpireOfficial.value.official_uuid) {
    list.push(umpireOfficial.value.official_uuid)
  }

  // 2) Service Judge
  if (serviceJudgeOfficial.value && serviceJudgeOfficial.value.official_uuid) {
    list.push(serviceJudgeOfficial.value.official_uuid)
  }

  // 3) Line Judge 4 slots
  lineJudgeSlots.value.forEach(slot => {
    if (slot.official && slot.official.official_uuid) {
      list.push(slot.official.official_uuid)
    }
  })

  return list
})

/** ========== onMounted: Tournament 목록 불러오기 ========== **/
onMounted(async () => {
  try {
    const officialRes = await officialApi.getOfficials()
    officialList.value = officialRes.data

    const tourRes = await tourApi.getTourList()
    tournaments.value = tourRes.data

    if (coderStore.tournament_uuid) {
      selectedTournament.value = coderStore.tournament_uuid
    }
  } catch (error) {
    console.error("Failed to load tournaments:", error)
  }
})

watch(selectedTournament, async (newVal) => {
  coderStore.tournament_uuid = newVal

  tieOptions.value = []
  selectedTie.value = ''
  matchOptions.value = []
  selectedMatch.value = ''
  gameUuidList.value = []
  selectedGameUuid.value = ''
  applyToAllGames.value = false

  if (!newVal) {
    // 선택 취소됨
    return
  }

  if (coderStore.tieNo) {
    tieOptions.value = [ coderStore.tieNo ]  // 예: [2]
  }

  if (tieOptions.value.length > 0) {
    selectedTie.value = String(tieOptions.value[0]) // ex) "2"
  }

})

watch(selectedGameUuid, async (newVal) => {
  // applyToAllGames가 체크되어 있으면, 단일 게임 조회를 안 할 수도 있음
  if (applyToAllGames.value) {
    // 전체 게임에 대한 일괄 적용 모드면, 굳이 단일 게임 배정을 볼 필요 없다고 판단할 수도.
    // 필요에 따라 로직 추가/수정.
    return
  }
  // gameUuid가 없으면(빈 값일 경우) 화면에서 할당 상태를 초기화
  if (!newVal) {
    clearAssignments()
    return
  }

  try {
    // API 파라미터 준비
    const params = {
      tournament_uuid: selectedTournament.value,
      tie_no: Number(selectedTie.value), // tie_no가 문자열이면 Number 변환
      match_no: selectedMatch.value,
      game_uuid: newVal
    }

    const resp = await officialApi.getGameOfficial(params)
    console.log(resp.data)
    setOfficialsFromResponse(resp.data)
  } catch (error) {
    console.error('Failed to fetch game officials:', error)
  }
}),

/** watch: tie -> matchOptions 업데이트 */
watch(selectedTie, async (newVal) => {
  selectedMatch.value = ''
  matchOptions.value = []
  gameUuidList.value = []
  selectedGameUuid.value = ''

  if (!newVal) {
    return
  }

  const tieNoNum = Number(newVal)
  const gameDate = coderStore.gameDate
  try {
    const resp = await coderApi.getTiePage({
      tournament_uuid: selectedTournament.value,
      tie_no: tieNoNum,
      game_date: gameDate
    })

    const matchArr = resp.data.match_info?.map((m: any) => m.match_no) || []
    matchOptions.value = matchArr

    coderStore.setTieData(
      selectedTournament.value,
      tieNoNum,
      resp.data.game_date  // 혹은 gameDate
    )

    if (matchOptions.value.length > 0) {
      selectedMatch.value = matchOptions.value[0]
    }

  } catch (err) {
    console.log('Failed to load tiepage:', err)
  }

})

/** watch: match -> gameUuidList 업데이트 */
watch(selectedMatch, async (newVal) => {
  selectedGameUuid.value = ''
  gameUuidList.value = []

  if (!selectedTournament.value || !selectedTie.value || !newVal) {
    return
  }

  try {
    const res = await officialApi.getGmaeuuids({
      tournament_uuid: selectedTournament.value,
      tie_no: selectedTie.value,
      match_no: newVal
    })
    gameUuidList.value = res.data.game_uuids
    if (gameUuidList.value.length > 0) {
      selectedGameUuid.value = gameUuidList.value[0].game_uuid
    }
    await fetchAssignedOfficials(gameUuidList.value[0].game_uuid)

  } catch (err) {
    console.error("Failed to load gameUuids:", err)
  }
})

/** ========== watch: applyToAllGames 변경 시 ========== **/
watch(applyToAllGames, (newVal) => {
  if (newVal) {
    // 체크되면 Game Select를 disable => selectedGame 초기화
    selectedGameUuid.value = ''
  }
})

async function fetchAssignedOfficials(gameUuid: string ) {
  if(!gameUuid) return

  try {
    const resp = await officialApi.getGameOfficial({
      tournament_uuid: selectedTournament.value,
      tie_no:  String(selectedTie.value),
      match_no: String(selectedMatch.value),
      game_uuid: gameUuid
    })
    setOfficialsFromResponse(resp.data)
  } catch (error) {
    console.error('Failed to fetch assigned officials:', error)
  }
}

function setOfficialsFromResponse(assignedList) {
   // 1) 화면 상태 초기화
   umpireOfficial.value = null
   serviceJudgeOfficial.value = null
   lineJudgeSlots.value = [
     { official: null },
     { official: null },
     { official: null },
     { official: null },
   ]

   // 2) assignedList 순회하며 role별로 분기
   assignedList.forEach((item) => {
     if (item.official_role === 'UMPIRE') {
       umpireOfficial.value = item
     } else if (item.official_role === 'SERVICE_JUDGE') {
       serviceJudgeOfficial.value = item
     } else if (item.official_role === 'LINE_JUDGE') {
       // 선심이 여러 명일 수 있으므로, 빈 슬롯을 찾아 차례로 할당
       const emptySlot = lineJudgeSlots.value.find(slot => slot.official === null)
       if (emptySlot) {
         emptySlot.official = item
       }
     }
   })
}

function isAssigned(uuid: string) {
  return assignedOfficialUuids.value.includes(uuid)
}

function openCancelModal() {
  showCancelConfirmModal.value = true
}

async function handleCancelConfirm() {
  showCancelConfirmModal.value = false
  // 메인(/) 경로로 이동
  router.push('/')
}

function handleCancelCancel() {
  // 모달만 닫기
  showCancelConfirmModal.value = false
}

function rowClick(uuid: string) {
  if (isAssigned(uuid)) {
    return
  }

  // radio 모델 세팅
  selectedOfficialUuid.value = uuid

  // confirmAssign() 로직 통합
  const chosen = officialList.value.find(o => o.official_uuid === uuid)
  if (!chosen) return

  if (currentRole.value === 'UMPIRE') {
    umpireOfficial.value = chosen
  } else if (currentRole.value === 'SERVICE_JUDGE') {
    serviceJudgeOfficial.value = chosen
  } else if (currentRole.value === 'LINE_JUDGE' && currentSlotIndex.value !== null) {
    lineJudgeSlots.value[currentSlotIndex.value].official = chosen
  }

  // 모달 닫기
  closeModal()
}

function openAssignModal(role: string, slotIdx: number|null = null) {
  currentRole.value = role
  currentSlotIndex.value = slotIdx
  selectedOfficialUuid.value = ''
  showAssignModal.value = true
}

function clearAssignments() {
  // 1) Umpire 해제
  umpireOfficial.value = null

  // 2) Service Judge 해제
  serviceJudgeOfficial.value = null

  // 3) Line Judges 해제
  lineJudgeSlots.value.forEach(slot => {
    slot.official = null
  })

  // Game Select/Checkbox
  selectedGameUuid.value = ''
  applyToAllGames.value = false
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

function openSaveModal() {
  if (!selectedTie.value || !selectedMatch.value) {
    alert("Tie/Match is not selected.")
    return
  }
  if (!applyToAllGames.value && !selectedGameUuid.value) {
    alert("Select game or check 'Apply to all 5 games'.")
    return
  }

  showSaveConfirmModal.value = true
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

async function handleSaveConfirm() {
  showSaveConfirmModal.value = false // 모달 닫기

  // 실제 API 호출 로직
  try {
    if (!selectedTie.value || !selectedMatch.value) {
      alert("Tie/Match is not selected.")
      return
    }
    if (!applyToAllGames.value && !selectedGameUuid.value) {
      alert("Select game or check 'Apply to all 5 games'.")
      return
    }

    let targetGames: string[] = []
    if (applyToAllGames.value) {
      // 모든 gameUuidList
      targetGames = gameUuidList.value.map(g => g.game_uuid)
    } else {
      // 단일 selectedGameUuid
      if (selectedGameUuid.value) {
        targetGames = [ selectedGameUuid.value ]
      }
    }

    const payload: Array<{ game_uuid: string; official_uuid: string; official_role: string }> = []
    if (umpireOfficial.value && umpireOfficial.value.official_uuid) {
      for (const gUuid of targetGames) {
        payload.push({
          game_uuid: gUuid,
          official_uuid: umpireOfficial.value.official_uuid,
          official_role: 'UMPIRE'
        })
      }
    }

    if (serviceJudgeOfficial.value && serviceJudgeOfficial.value.official_uuid) {
      for (const gUuid of targetGames) {
        payload.push({
          game_uuid: gUuid,
          official_uuid: serviceJudgeOfficial.value.official_uuid,
          official_role: 'SERVICE_JUDGE'
        })
      }
    }

    lineJudgeSlots.value.forEach((slot, idx) => {
      if (slot.official && slot.official.official_uuid) {
        for (const gUuid of targetGames) {
          payload.push({
            game_uuid: gUuid,
            official_uuid: slot.official.official_uuid,
            official_role: 'LINE_JUDGE'
          })
        }
      }
    })

    if (payload.length === 0) {
      alert("No officials assigned to save.")
      return
    }

    console.log("Saving gameOfficials payload:", payload)
    const response = await coderApi.postGameOfficials(payload)
    // 응답 처리
    console.log("Save success:", response.data)

    alert("Officials saved successfully!")

  } catch (error) {
    console.error('Failed to save', error)
    // 실패 처리
  }
}

function handleSaveCancel() {
  showSaveConfirmModal.value = false
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

.official-list-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
.official-list-table th, .official-list-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.table-scroll-container {
  max-height: 400px;
  overflow-y: auto;
  display: block;
}

.official-list-table tbody tr:hover {
  background-color: #f5f5f5;
  cursor: pointer;   /* 포인터 커서 */
}

.selected-row {
  background-color: #d9edf7; /* 하늘색 등 */
}

.assigned-row {
  background-color: #eee;
  color: #888;
  cursor: not-allowed;
}
.assigned-row:hover {
  background-color: #eee; /* 호버해도 변하지 않도록 */
}

.btn-clear {
  padding: 6px 14px;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #ccc;
  background-color: #f2f2f2;
}
.btn-clear:hover {
  background-color: #ddd;
}
</style>
