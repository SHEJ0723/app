<template>
  <div class="parking-status">
    <h2>车位查看</h2>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else>
      <div v-for="zone in zones" :key="zone" class="zone-block">
        <h3>{{ zone }} 区</h3>
        <div class="spot-list">
          <div v-for="spot in groupedSpots[zone]" :key="spot.id" class="spot-card" :class="spot.status">
            <div class="spot-number">{{ spot.spot_number }}</div>
            <div class="spot-type">类型: {{ spot.type }}</div>
            <div class="spot-status">状态: <span :class="spot.status">{{ spot.status }}</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const spots = ref([])
const loading = ref(true)
const zones = ref(['A', 'B', 'C'])

const groupedSpots = computed(() => {
  const groups = { A: [], B: [], C: [] }
  spots.value.forEach(spot => {
    if (groups[spot.zone]) groups[spot.zone].push(spot)
  })
  return groups
})

onMounted(async () => {
  loading.value = true
  try {
    // 这里假设已登录并有token，实际项目需处理token
    const token = localStorage.getItem('token')
    const res = await axios.get('/api/parking-spots', {
      headers: { Authorization: `Bearer ${token}` },
      params: { per_page: 20 }
    })
    if (res.data.success) {
      spots.value = res.data.data
    }
  } catch (e) {
    alert('获取车位信息失败')
  }
  loading.value = false
})
</script>
<style scoped>
.parking-status {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px #0001;
  padding: 32px 24px 24px 24px;
}
.zone-block {
  margin-bottom: 32px;
}
.spot-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.spot-card {
  width: 120px;
  background: #f5f7fa;
  border-radius: 10px;
  box-shadow: 0 1px 4px #0001;
  padding: 12px 8px;
  text-align: center;
  border: 2px solid #e3e3e3;
  transition: border 0.2s;
}
.spot-card.空闲 {
  border-color: #42b983;
}
.spot-card.占用 {
  border-color: #e53935;
}
.spot-card.维修 {
  border-color: #fbc02d;
}
.spot-number {
  font-size: 22px;
  font-weight: bold;
  color: #1976d2;
  margin-bottom: 4px;
}
.spot-type {
  font-size: 14px;
  color: #888;
}
.spot-status {
  font-size: 15px;
  margin-top: 4px;
}
.spot-status .空闲 {
  color: #42b983;
}
.spot-status .占用 {
  color: #e53935;
}
.spot-status .维修 {
  color: #fbc02d;
}
.loading {
  text-align: center;
  color: #888;
  font-size: 18px;
  margin: 40px 0;
}
</style> 