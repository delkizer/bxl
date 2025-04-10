<template>
  <div class="official-list-page">
    <h2>Officials Management</h2>

    <!-- 상단 기능 버튼 -->
    <div class="top-bar">
      <button class="btn" @click="showMultiAddModal = true">
        Add Multiple Officials
      </button>
      <button
        class="btn"
        @click="deleteSelectedOfficials"
        :disabled="selectedOfficials.length === 0"
      >
        Delete Selected
      </button>
    </div>

    <!-- 목록 테이블 -->
    <table class="official-table">
      <thead>
        <tr>
          <th>
            <!-- 전체 선택 -->
            <input type="checkbox" @change="toggleSelectAll($event)" />
          </th>
          <!-- 질문에서 UUID는 화면에 노출 안 함 -->
          <th>First Name</th>
          <th>Family Name</th>
          <th>Nickname</th>
          <th>Gender</th>
          <th>Nation Code</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="official in officialList" :key="official.official_uuid">
          <td>
            <input
              type="checkbox"
              :value="official.official_uuid"
              v-model="selectedOfficials"
            />
          </td>
          <td>{{ official.first_name }}</td>
          <td>{{ official.family_name }}</td>
          <td>{{ official.nickname }}</td>
          <td>{{ official.gender }}</td>
          <td>{{ official.nation_code }}</td>
          <td>
            <button class="btn" @click="openEditModal(official)">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- (A) 여러 명 동시 추가 모달 -->
    <div v-if="showMultiAddModal.valueOf()" class="modal">
      <div class="modal-content">
        <h3>Add Multiple Officials</h3>
        <table class="multi-add-table">
          <thead>
            <tr>
              <th>First Name</th>
              <th>Family Name</th>
              <th>Nickname</th>
              <th>Gender</th>
              <th>Nation</th>
              <th>Remove</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(row, idx) in newOfficials.values()"
              :key="idx"
            >
              <td><input type="text" v-model="row.first_name" /></td>
              <td><input type="text" v-model="row.family_name" /></td>
              <td><input type="text" v-model="row.nickname" /></td>
              <td>
                <select class="form-control" v-model="row.gender">
                  <option value="">성별</option>
                  <option value="000M">남</option>
                  <option value="000W">여</option>
                </select>
              </td>
              <td>
                <select class="form-control" v-model="row.nation_code">
                  <option value="">국가</option>
                  <option
                    v-for="nation in nationList"
                    :key="nation.code"
                    :value="nation.code.trim()">
                    {{nation.code_desc}}
                  </option>
                </select>

              </td>
              <td>
                <button class="btn" @click="removeNewOfficial(idx)">X</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="button-container">
          <button class="btn" @click="addNewOfficialRow">+ Add Row</button>
          <button class="btn" @click="confirmMultiAdd">Save</button>
          <button class="btn" @click="closeMultiAddModal">Cancel</button>
        </div>
      </div>
    </div>

    <!-- (B) 개별 수정 모달 -->
    <div v-if="showEditModal.valueOf()" class="modal">
      <div class="modal-content">
        <h3>Edit Official</h3>

        <div class="form-row">
          <label>First Name</label>
          <input type="text" v-model="editOfficial.first_name" />
        </div>
        <div class="form-row">
          <label>Family Name</label>
          <input type="text" v-model="editOfficial.family_name" />
        </div>
        <div class="form-row">
          <label>Nickname</label>
          <input type="text" v-model="editOfficial.nickname" />
        </div>
        <div class="form-row">
          <label>Gender</label>
          {{editOfficial.gender}}
          <select v-model="editOfficial.gender">
            <option value="">성별</option>
            <option value="000M">남</option>
            <option value="000W">여</option>
          </select>
        </div>
        <div class="form-row">
          <label>Nation Code</label>
          <select v-model="editOfficial.nation_code">
            <option value="">국가</option>
            <option
              v-for="nation in nationList"
              :key="nation.code"
              :value="nation.code.trim()"
            >
              {{ nation.code_desc }}
            </option>
          </select>
        </div>
        <div class="button-container">
          <button class="btn" @click="saveEdit">Save</button>
          <button class="btn" @click="cancelEdit">Cancel</button>
        </div>
      </div>
    </div>
    <!-- 새로운 저장/종료 버튼 -->
    <div class="button-container">
      <button class="btn btn-cancel" @click="handleCancel">종료</button>
    </div>

    <!-- 종료 모달 -->
    <ConfirmationModal
      :visible="showExitModal"
      title="종료 확인"
      message="Home으로 이동하시겠습니까?"
      confirmButtonLabel="확인"
      cancelButtonLabel="취소"
      @confirm="handleExitConfirm"
      @cancel="handleExitCancel"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from "vue-router";
import officialApi from '@/api/officialApi.js'
import tourApi from '@/api/tourApi'

import ConfirmationModal from "@/components/modal/Confirmation.vue";

// 1) Officials 목록 (테이블)
const officialList = ref<any[]>([])

// 2) 선택된 체크박스 리스트 (UUID 배열)
const selectedOfficials = ref<string[]>([])

// 3) 다중 등록 모달 표시 여부 + 입력 데이터(newOfficials)
const showMultiAddModal = ref<boolean>(false)
const newOfficials = ref<any[]>([]) // [{first_name:'', family_name:'', ...}, {...}]

// 4) 개별 수정 모달 표시 여부 + editOfficial
const showEditModal = ref(false)
const editOfficial = ref<any>({
})

const nationList = ref<any[]>([])
const showExitModal = ref(false)
const router = useRouter()

// ========== onMounted: 초기 로딩 예시 ==========
onMounted(async () => {
  try{
    const officialListRes = await officialApi.getOfficials()
    officialList.value = officialListRes.data

    const nationListRes = await tourApi.getNationList()
    nationList.value = nationListRes.data

  } catch ( error ) {
    console.log('Failed to fetch officials:', error )
  }
})

// ========== (A) 여러 명 동시 추가 메서드들 ==========
function addNewOfficialRow() {
  newOfficials.value.push({
    first_name: '',
    family_name: '',
    nickname: '',
    gender: '',
    nation_code: ''
  })
}

function removeNewOfficial(idx: number) {
  newOfficials.value.splice(idx, 1)
}

async function confirmMultiAdd() {
  try {
    const postOfficialRes = await officialApi.postOfficials(newOfficials.value)
    console.log('Officials Added : ', postOfficialRes.data)

    const getOfficialRes = await officialApi.getOfficials()
    officialList.value = getOfficialRes.data

    closeMultiAddModal()
  } catch ( error ) {
    console.error('Failed to add newe officials: ', error)
  }
}

function closeMultiAddModal() {
  showMultiAddModal.value = false
  // 입력 필드 초기화
  newOfficials.value = []
}

// ========== (B) 개별 수정 메서드들 ==========
function openEditModal(official: any) {
  showEditModal.value = true
  // 복사해서 editOfficial에 할당
  editOfficial.value = { ...official }
}

async function saveEdit() {
  try {
    const payload = [ editOfficial.value ]
    await officialApi.putOfficials( payload )
    const getOfficialsRes = await officialApi.getOfficials()
    officialList.value = getOfficialsRes.data
    cancelEdit()
  } catch( error ) {
    console.error('Failed to update official:', error)
  }
}

function cancelEdit() {
  showEditModal.value = false
  editOfficial.value = {}
}

// ========== (C) 다중 삭제 메서드 ==========
async function deleteSelectedOfficials() {
  try {
    const payload = selectedOfficials.value.map(uuid => {
      const official = officialList.value.find( o => o.official_uuid === uuid )
      return {
        official_uuid: uuid,
        first_name: official?.first_name,
        family_name: official?.family_name,
        nickname: official?.nickname,
        gender: official?.gender,
        nation_code: official?.nation_code
      }
    })

    console.log(payload)
    await officialApi.deleteOfficials(payload)

    const getOfficialsRes = await officialApi.getOfficials()
    officialList.value = getOfficialsRes.data
    selectedOfficials.value = []
  } catch( error ) {
    console.error('Failed to delete officials:', error)
  }
}

// ========== (D) 전체 선택 체크박스 ==========
function toggleSelectAll(e: Event) {
  const checked = (e.target as HTMLInputElement).checked
  if (checked) {
    selectedOfficials.value = officialList.value.map(o => o.official_uuid)
  } else {
    // 해제
    selectedOfficials.value = []
  }
}

function handleCancel() {
  // "종료" 버튼 클릭 → "종료 확인" 모달 열기
  showExitModal.value = true
}

function handleExitConfirm() {
  showExitModal.value = false
  router.push('/')
}

function handleExitCancel() {
  showExitModal.value = false
}

</script>

<style scoped>
.official-list-page {
  position: absolute;
  width: 800px;
  max-width: 900px;
  margin: 0 auto;
  background-color: #f7f7f7;
  padding: 16px;
  border-radius: 8px;
  top: 10%;
  left: 50%;     /* 수평 중앙 */
  transform: translate(-50%); /* 자기 크기의 절반만큼 이동해 완전 중앙 정렬 */
}

.top-bar {
  margin-bottom: 20px;
}

.official-table {
  width: 100%;
  border-collapse: collapse;
}

.official-table th,
.official-table td {
  border: 1px solid #ccc;
  padding: 8px 12px;
  text-align: center;
}

.multi-add-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  table-layout: fixed;
}
.multi-add-table th, .multi-add-table td {
  border: 1px solid #ccc;
  padding: 6px 10px;
  word-wrap: break-word;
}

.multi-add-table input[type="text"] {
  width: 100%;
  box-sizing: border-box;
}

.btn {
  background-color: #4CAF50;
  color: #fff;
  border: none;
  padding: 6px 14px;
  cursor: pointer;
  border-radius: 4px;
  margin-right: 6px;
}
.btn:hover {
  background-color: #45a049;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-content {
  background-color: #fff;
  width: 750px;
  max-height: 80vh;
  overflow-y: auto;
  padding: 20px;
  border-radius: 6px;
}

.form-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.button-container {
  text-align: right;
  margin-top: 10px;
}

.btn-cancel {
  background-color: #f56b6b;
  color: #fff;
}
</style>
