import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// 创建axios实例
const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true  // 允许跨域请求携带cookie
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 检查响应中是否包含预期的数据结构
    const data = response.data
    if (data && typeof data === 'object') {
      if (data.success === false) {
        return Promise.reject(new Error(data.message || '请求失败'))
      }
      return data
    }
    return Promise.reject(new Error('Invalid response format'))
  },
  error => {
    if (error.response) {
      // 处理401未授权错误
      if (error.response.status === 401) {
        // 清除所有认证信息
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        localStorage.removeItem('userType')
        
        // 如果不是在登录页，则重定向到登录页
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login'
        }
        return Promise.reject(new Error(error.response.data?.message || '登录已过期，请重新登录'))
      }
      
      // 处理400错误（包括验证码错误）
      if (error.response.status === 400) {
        const message = error.response.data?.message || '请求参数错误'
        return Promise.reject(new Error(message))
      }
      
      // 处理404错误
      if (error.response.status === 404) {
        return Promise.reject(new Error('请求的资源不存在'))
      }
      
      // 处理其他HTTP错误
      const message = error.response.data?.message || '请求失败'
      return Promise.reject(new Error(message))
    }
    return Promise.reject(new Error('网络错误，请检查您的网络连接'))
  }
)

export const authAPI = {
  // 获取验证码
  async getCaptcha() {
    try {
      const response = await api.get('/api/captcha')
      return response
    } catch (error) {
      console.error('获取验证码失败:', error)
      throw error
    }
  },

  // 用户登录
  async userLogin(data) {
    try {
      const response = await api.post('/api/user-login', data)
      return response
    } catch (error) {
      console.error('用户登录失败:', error)
      throw error
    }
  },

  // 管理员登录
  async adminLogin(data) {
    try {
      const response = await api.post('/api/admin-login', data)
      return response
    } catch (error) {
      console.error('管理员登录失败:', error)
      throw error
    }
  },

  // 用户注册
  async register(data) {
    try {
      const response = await api.post('/api/register', data)
      return response
    } catch (error) {
      console.error('用户注册失败:', error)
      throw error
    }
  },

  // 退出登录
  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    localStorage.removeItem('userType')
    return Promise.resolve()
  }
}

export default api 