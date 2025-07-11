<template>
  <div class="login-bg">
    <div class="bg-shape circle1"></div>
    <div class="bg-shape circle2"></div>
    <div class="bg-shape triangle"></div>
    <div class="login-card">
      <div class="login-title">用户注册</div>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="registerForm.name"
            prefix-icon="User"
            placeholder="请输入姓名"
          />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="registerForm.phone"
            prefix-icon="Phone"
            placeholder="请输入手机号"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            prefix-icon="Message"
            placeholder="请输入邮箱"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            prefix-icon="Lock"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            prefix-icon="Lock"
            placeholder="请再次输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            class="login-btn"
            @click="handleRegister"
          >
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
        <div class="register-link">
          <router-link to="/login">已有账号？立即登录</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Phone } from '@element-plus/icons-vue'
import { authAPI } from '../api/auth'
import bgImg from '@/assets/images/bg-login.jpg'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)
const registerForm = reactive({
  name: '',
  phone: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const validatePhone = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入手机号'))
  } else if (!/^1[3-9]\d{9}$/.test(value)) {
    callback(new Error('请输入正确的手机号格式'))
  } else {
    callback()
  }
}

const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { validator: validatePhone, trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  try {
    await registerFormRef.value.validate()
    loading.value = true
    const { name, phone, email, password } = registerForm
    const response = await authAPI.register({ name, phone, email, password })
    if (response.success) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || '注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style>
.login-container {
  background: url('https://img.freepik.com/free-vector/abstract-blue-geometric-shapes-background_1035-17545.jpg') center/cover;
  height: 100vh;
  display: grid;
  place-items: center;
}
.login-card {
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 40px;
  width: 400px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
</style>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  /* background: #f5f7fa; */
  background: transparent;
  padding: 0 16px;
}
.register-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px #0001;
  padding: 32px 24px 24px 24px;
  box-sizing: border-box;
}
@media (max-width: 600px) {
  .register-card {
    padding: 16px 6px 16px 6px;
    border-radius: 0;
    box-shadow: none;
  }
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  color: #333;
  margin-bottom: 10px;
  font-size: 24px;
}

.register-header p {
  color: #666;
  font-size: 16px;
}

.register-button {
  width: 100%;
  margin-top: 20px;
  height: 40px;
  font-size: 16px;
}

.register-links {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.register-links a {
  color: var(--el-color-primary);
  text-decoration: none;
}

.register-links a:hover {
  text-decoration: underline;
}

:deep(.el-form-item__label) {
  font-size: 14px;
  color: #333;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset;
}

:deep(.el-input__inner) {
  height: 40px;
}
</style> 