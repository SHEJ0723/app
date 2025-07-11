<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>停车位状态</span>
            </div>
          </template>
          <div class="parking-status">
            <el-statistic title="可用车位" :value="availableSpots">
              <template #suffix>个</template>
            </el-statistic>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>我的车辆</span>
            </div>
          </template>
          <div class="my-vehicles">
            <el-statistic title="已绑定车牌" :value="licensePlates.length">
              <template #suffix>个</template>
            </el-statistic>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>账户余额</span>
            </div>
          </template>
          <div class="balance">
            <el-statistic title="当前余额" :value="balance" :precision="2">
              <template #prefix>¥</template>
            </el-statistic>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="16">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>最近停车记录</span>
            </div>
          </template>
          <el-table :data="parkingRecords" style="width: 100%">
            <el-table-column prop="date" label="日期" width="180" />
            <el-table-column prop="duration" label="停车时长" width="180" />
            <el-table-column prop="fee" label="费用" />
            <el-table-column prop="status" label="状态" />
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>快捷操作</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/parking-reservation')">
              预约停车
            </el-button>
            <el-button type="success" @click="$router.push('/find-car')">
              查找车辆
            </el-button>
            <el-button type="warning" @click="$router.push('/auto-pay')">
              自动扣费
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 模拟数据
const availableSpots = ref(120)
const licensePlates = ref(['浙A12345', '浙B67890'])
const balance = ref(258.50)

const parkingRecords = ref([
  {
    date: '2024-01-15 14:30',
    duration: '2小时30分',
    fee: '¥15.00',
    status: '已支付'
  },
  {
    date: '2024-01-14 09:15',
    duration: '4小时15分',
    fee: '¥25.00',
    status: '已支付'
  },
  {
    date: '2024-01-13 18:45',
    duration: '1小时45分',
    fee: '¥10.00',
    status: '已支付'
  }
])
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.mt-4 {
  margin-top: 20px;
}

.box-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quick-actions .el-button {
  width: 100%;
}

.parking-status,
.my-vehicles,
.balance {
  text-align: center;
  padding: 20px 0;
}
</style> 