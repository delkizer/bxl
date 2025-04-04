<template>
  <div v-if="visible" class="modal-overlay">
    <div class="modal-content">
      <h3 class="modal-title">{{ title }}</h3>
      <p class="modal-message">{{ message }}</p>
      <div class="modal-button-container">
        <!-- CODER(확인) 버튼 -->
        <button class="modal-btn" @click="$emit('confirm')">
          {{ confirmButtonLabel }}
        </button>
        <!-- 가운데 수정 버튼 -->
        <button class="modal-btn" @click="$emit('player')">
          {{ PlayerButtonLabel }}
        </button>
      </div>
      <div class="modal-button-container">
        <button class="modal-btn" @click="$emit('official')">
          {{ OfficialButtonLabel }}
        </button>
        <!-- 취소 버튼 -->
        <button class="modal-btn" @click="$emit('cancel')">
          {{ cancelButtonLabel }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CoderModal",
  props: {
    visible: Boolean,
    title: {
      type: String,
      default: "알림"
    },
    message: {
      type: String,
      default: "진행하시겠습니까?"
    },
    confirmButtonLabel: {
      type: String,
      default: "CODER"
    },
    PlayerButtonLabel: {
      type: String,
      default: "PLAYER"
    },
    OfficialButtonLabel: {
      type: String,
      default: "OFFICIAL"
    },
    cancelButtonLabel: {
      type: String,
      default: "CANCEL"
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999;
}
.modal-content {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
}
.modal-title {
  margin-top: 0;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: center;
}
.modal-message {
  margin-bottom: 20px;
  text-align: center;
}
.modal-button-container {
  display: flex; justify-content: space-evenly;
  margin: 10px;
}
.modal-btn {
  width: 120px;
  padding: 10px 20px;
  background-color: white;
  color: #333;
  border: 1px solid #333;
  font-weight: bold;
  border-radius: 5px;
  cursor: pointer;
}
</style>
