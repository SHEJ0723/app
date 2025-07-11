<template>
  <div class="admin-statistics-container">
    <el-card>
      <template #header>
        <h3>收入与车流量统计</h3>
      </template>
      <div class="chart-placeholder">[此处可集成ECharts柱状图/折线图]</div>
    </el-card>
  </div>
</template>
<script setup>
</script>
<style scoped>
.admin-statistics-container {
  max-width: 1100px;
  margin: 30px auto;
  padding: 20px;
}
.chart-placeholder {
  width: 100%;
  height: 400px;
  background: #f5f7fa;
  border: 1px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 18px;
}
</style> 