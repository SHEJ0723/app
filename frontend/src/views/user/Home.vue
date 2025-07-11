<template>
  <div class="user-home">
    <div class="quick-actions">
      <el-card class="action-card" @click="goTo('ParkingReservation')">
        <el-icon><Calendar /></el-icon>
        <div>预订车位</div>
      </el-card>
      <el-card class="action-card" @click="goTo('ParkingStatus')">
        <el-icon><Location /></el-icon>
        <div>车位查看</div>
      </el-card>
      <el-card class="action-card" @click="goTo('ParkingMap')">
        <el-icon><MapLocation /></el-icon>
        <div>停车场布局图</div>
      </el-card>
      <el-card class="action-card" @click="goTo('Fee')">
        <el-icon><Money /></el-icon>
        <div>收费明细</div>
      </el-card>
      <el-card class="action-card" @click="goTo('Orders')">
        <el-icon><List /></el-icon>
        <div>订单查看</div>
      </el-card>
    </div>
    <div class="parking-map-section">
      <h3>园区停车场布局</h3>
      <img :src="parkingBg" alt="停车场布局图" class="parking-map-img" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Calendar, Location, MapLocation, Money, List } from '@element-plus/icons-vue'
import parkingBg from '@/assets/parking-bg.svg'

const router = useRouter()
function goTo(name) {
  router.push({ name })
}
</script>

<style scoped>
.user-home {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px 0;
  background: #f6faff;
}
.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: space-around;
}
.action-card {
  width: 120px;
  height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px #1976d220;
  border: 1.5px solid #e3eaf5;
  transition: box-shadow 0.2s, border-color 0.2s, transform 0.15s;
}
.action-card:hover {
  box-shadow: 0 6px 24px #1976d240;
  border-color: #1976d2;
  transform: translateY(-2px) scale(1.04);
}
.action-card .el-icon {
  font-size: 36px;
  margin-bottom: 10px;
  color: #1976d2;
}
.action-card div {
  font-weight: 600;
  color: #222;
  letter-spacing: 1px;
}
.parking-map-section {
  margin-top: 24px;
  text-align: center;
}
.parking-map-section h3 {
  color: #1976d2;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 12px;
}
.parking-map-img {
  max-width: 100%;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 2px 12px #1976d220;
  border: 1.5px solid #e3eaf5;
}
@media (max-width: 600px) {
  .quick-actions {
    gap: 8px;
  }
  .action-card {
    width: 44vw;
    height: 90px;
    font-size: 14px;
    border-radius: 10px;
  }
  .parking-map-section h3 {
    font-size: 16px;
  }
}
</style> 