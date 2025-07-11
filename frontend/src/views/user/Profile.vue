<template>
  <div class="profile-container">
    <el-card>
      <template #header>
        <span>个人信息设置</span>
      </template>
      <el-form :model="form" :rules="rules" ref="profileForm" label-width="80px" class="profile-form">
        <el-form-item label="用户名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSave">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api/auth'

const form = ref({
  name: '',
  phone: '',
  email: ''
})

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ]
}

const profileForm = ref(null)

onMounted(async () => {
  // 假设有获取当前用户信息的API
  try {
    const userInfo = JSON.parse(localStorage.getItem('userInfo'))
    if (userInfo) {
      form.value.name = userInfo.name
      form.value.phone = userInfo.phone
      form.value.email = userInfo.email
    }
  } catch (e) {}
})

const onSave = () => {
  profileForm.value.validate(async (valid) => {
    if (!valid) return
    try {
      // 假设有更新用户信息的API
      // await api.updateProfile(form.value)
      ElMessage.success('保存成功')
      // 更新本地缓存
      localStorage.setItem('userInfo', JSON.stringify(form.value))
    } catch (e) {
      ElMessage.error('保存失败')
    }
  })
}
</script>

<style scoped>
.profile-container {
  max-width: 500px;
  margin: 40px auto;
}
.profile-form {
  margin-top: 20px;
}
</style> 