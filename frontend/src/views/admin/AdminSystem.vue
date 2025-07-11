<template>
  <div class="admin-system-container">
    <el-card>
      <template #header>
        <h3>系统运维</h3>
      </template>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <h4>收费标准配置</h4>
            <el-form :model="fee" label-width="120px">
              <el-form-item label="首小时">
                <el-input v-model="fee.first" suffix="元" />
              </el-form-item>
              <el-form-item label="后续每小时">
                <el-input v-model="fee.next" suffix="元" />
              </el-form-item>
              <el-form-item label="24小时封顶">
                <el-input v-model="fee.max" suffix="元" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveFee">保存</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <h4>告警规则设置</h4>
            <el-form :model="alarm" label-width="120px">
              <el-form-item label="超时停车提醒(小时)">
                <el-input v-model="alarm.timeout" suffix="小时" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveAlarm">保存</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
      <el-divider />
      <h4>操作日志审计</h4>
      <el-table :data="logs" style="width: 100%">
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="user" label="管理员" width="120" />
        <el-table-column prop="action" label="操作内容" />
      </el-table>
    </el-card>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
const fee = ref({ first: 5, next: 2, max: 30 })
const alarm = ref({ timeout: 72 })
const logs = ref([
  { time: '2024-06-01 10:00', user: 'admin1', action: '修改收费标准' },
  { time: '2024-06-01 09:00', user: 'admin2', action: '设置超时停车告警' }
])
const saveFee = () => {
  ElMessage.success('收费标准已保存')
}
const saveAlarm = () => {
  ElMessage.success('告警规则已保存')
}
</script>
<style scoped>
.admin-system-container {
  max-width: 1100px;
  margin: 30px auto;
  padding: 20px;
}
</style> 