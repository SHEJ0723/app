<template>
  <div class="admin-dashboard-container">
    <el-card>
      <template #header>
        <h3>数据看板</h3>
      </template>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-statistic title="当日收入(元)" :value="income" />
        </el-col>
        <el-col :span="8">
          <el-statistic title="今日车流量(辆)" :value="traffic" />
        </el-col>
        <el-col :span="8">
          <el-statistic 
            title="高峰时段" 
            :value="0" 
            :formatter="() => peakTime"
          />
        </el-col>
      </el-row>
      <el-divider />
      <el-row>
        <el-col :span="24">
          <el-card>
            <h4>高峰时段预警（折线图）</h4>
            <div class="chart-placeholder">[此处可集成ECharts折线图]</div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>
<script setup>
import { ref } from 'vue'
const income = ref(12800)
const traffic = ref(320)
const peakTime = ref('17:00-19:00')
</script>
<style scoped>
.admin-dashboard-container {
  max-width: 1100px;
  margin: 30px auto;
  padding: 20px;
}
.chart-placeholder {
  width: 100%;
  height: 300px;
  background: #f5f7fa;
  border: 1px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 18px;
}
</style> 