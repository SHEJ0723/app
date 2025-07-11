<template>
  <div class="reservation-container">
    <button class="back-btn" @click="goBack">返回</button>
    <h2>预约车位</h2>
    <!-- 车牌选择 -->
    <div class="form-row">
      <label>选择车牌：</label>
      <select v-model="selectedPlate">
        <option disabled value="">请选择车牌</option>
        <option v-for="plate in licensePlates" :key="plate" :value="plate">{{ plate }}</option>
      </select>
    </div>
    <!-- 时间选择 -->
    <div class="form-row time-select">
      <label>预约时间：</label>
      <input type="datetime-local" v-model="startTime" :min="minStartTime" />
      <span style="margin: 0 8px;">至</span>
      <input type="datetime-local" v-model="endTime" :min="startTime || minStartTime" />
    </div>
    <!-- 车位列表 -->
    <div class="parking-list">
      <div
        v-for="spot in parkingSpots"
        :key="spot.spotId"
        :class="['parking-spot', { selected: selectedSpot === spot.spotId, disabled: spot.status !== 'free' }]"
        @click="selectSpot(spot)"
      >
        <div>车位号：{{ spot.spotId }}</div>
        <div>区域：{{ spot.areaCode }}</div>
        <div>类型：{{ spot.spotType }}</div>
        <div>状态：{{ spot.status === 'free' ? '空闲' : '不可用' }}</div>
      </div>
    </div>
    <button
      class="reserve-btn"
      :disabled="!canReserve"
      @click="reserve"
    >预约</button>
  </div>
</template>

<script>
export default {
  name: 'ParkingReservation',
  data() {
    return {
      licensePlates: ['粤A12345', '粤B67890'], // mock 车牌
      selectedPlate: '',
      startTime: '',
      endTime: '',
      parkingSpots: [
        { spotId: 'A01', areaCode: 'A', spotType: '普通', status: 'free' },
        { spotId: 'A02', areaCode: 'A', spotType: '新能源', status: 'reserved' },
        { spotId: 'B01', areaCode: 'B', spotType: '普通', status: 'free' }
      ],
      selectedSpot: null
    }
  },
  computed: {
    minStartTime() {
      // 当前时间，格式为 yyyy-MM-ddTHH:mm
      const now = new Date();
      now.setMinutes(now.getMinutes() + 1); // 禁止选择当前时间之前
      return now.toISOString().slice(0, 16);
    },
    canReserve() {
      if (!this.selectedPlate || !this.startTime || !this.endTime || !this.selectedSpot) return false;
      const start = new Date(this.startTime);
      const end = new Date(this.endTime);
      const now = new Date();
      return (
        start > now &&
        end > start &&
        (end - start) / 60000 >= 30 // 至少30分钟
      );
    }
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    selectSpot(spot) {
      if (spot.status === 'free') {
        this.selectedSpot = spot.spotId;
      }
    },
    reserve() {
      if (!this.canReserve) {
        alert('请填写完整信息并确保时间有效！');
        return;
      }
      // 模拟预约成功
      alert(`预约成功！\n车牌：${this.selectedPlate}\n车位号：${this.selectedSpot}\n时间：${this.startTime} 至 ${this.endTime}`);
      // 可在此处重置表单或跳转
    }
  }
}
</script>

<style scoped>
.reservation-container {
  max-width: 500px;
  margin: 60px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(33, 150, 243, 0.08);
  padding: 32px 24px 24px 24px;
  position: relative;
}
.back-btn {
  position: absolute;
  left: 24px;
  top: 24px;
  background: #fff;
  color: #1976d2;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: background 0.2s;
}
.back-btn:hover {
  background: #e3f2fd;
}
.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 18px;
}
.form-row label {
  min-width: 80px;
  color: #1976d2;
  font-weight: bold;
}
.form-row select,
.form-row input[type="datetime-local"] {
  flex: 1;
  padding: 6px 10px;
  border: 1px solid #90caf9;
  border-radius: 4px;
  margin-left: 8px;
  font-size: 15px;
}
.time-select input[type="datetime-local"] {
  width: 180px;
}
.parking-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 32px 0;
}
.parking-spot {
  border: 2px solid #90caf9;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  background: #e3f2fd;
  transition: border 0.2s, background 0.2s;
}
.parking-spot.selected {
  border: 2px solid #1976d2;
  background: #bbdefb;
}
.parking-spot.disabled {
  color: #bdbdbd;
  background: #f5f5f5;
  cursor: not-allowed;
}
.reserve-btn {
  width: 100%;
  padding: 12px;
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.reserve-btn:disabled {
  background: #90caf9;
  cursor: not-allowed;
}
</style> 