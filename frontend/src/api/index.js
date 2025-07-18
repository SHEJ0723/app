import axios from 'axios'
import { getToken, setToken, removeToken } from '@/utils/auth'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(config => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器
api.interceptors.response.use(response => {
  return response.data
}, async error => {
  const originalRequest = error.config
  
  // 处理401错误 - token过期
  if (error.response?.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true
    try {
      const refreshResponse = await axios.post('/auth/refresh')
      const newToken = refreshResponse.data.token
      setToken(newToken)
      originalRequest.headers.Authorization = `Bearer ${newToken}`
      return api(originalRequest)
    } catch (refreshError) {
      removeToken()
      window.location.href = '/login'
      return Promise.reject(refreshError)
    }
  }

  // 处理其他错误
  const errorMessage = error.response?.data?.message || error.message
  return Promise.reject(errorMessage)
})

export default api