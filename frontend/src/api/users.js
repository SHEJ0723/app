import api from './index'
import { message } from 'ant-design-vue'

// 设置用户API的基础URL
api.defaults.baseURL = 'http://localhost:5000'

// 添加JWT认证头
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 统一响应处理
const handleResponse = (response) => {
  if (response.code !== 200) {
    throw new Error(response.message || '操作失败')
  }
  return response.data
}

const getUsers = async (params = {}) => {
  try {
    const response = await api.get('/api/users', { 
      params: {
        page: params.page || 1,
        pageSize: params.pageSize || 10,
        keyword: params.keyword || '',
        ...params
      }
    })
    // 直接返回后端的 data 字段
    return response.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
    throw new Error(error.response?.data?.message || '获取用户列表失败')
  }
}

const addUser = async (userData) => {
  try {
    const response = await api.post('/api/users', {
      ...userData,
      role: userData.role || 'user',
      email: userData.email || ''
    })
    return handleResponse({
      code: 200,
      data: response.data,
      message: '用户添加成功'
    })
  } catch (error) {
    console.error('添加用户失败:', error)
    throw new Error(error.response?.data?.message || '添加用户失败')
  }
}

const updateUser = async (id, userData) => {
  try {
    const response = await api.put(`/api/users/${id}`, {
      ...userData,
      email: userData.email || ''
    })
    return handleResponse({
      code: 200,
      data: response.data,
      message: '用户更新成功'
    })
  } catch (error) {
    console.error('更新用户失败:', error)
    throw new Error(error.response?.data?.message || '更新用户失败')
  }
}

const deleteUser = async (id) => {
  try {
    const response = await api.delete(`/api/users/${id}`)
    return handleResponse({
      code: 200,
      data: response.data,
      message: '用户删除成功'
    })
  } catch (error) {
    console.error('删除用户失败:', error)
    throw new Error(error.response?.data?.message || '删除用户失败')
  }
}

export { getUsers, addUser, updateUser, deleteUser }