import api from './index'

export const getOrders = async (params = {}) => {
  return api.get('/api/orders', { params })
}

export const createOrder = async (data) => {
  return api.post('/api/orders', data)
}

export const deleteOrder = async (orderId) => {
  return api.delete(`/api/orders/${orderId}`)
}

export const payOrder = async (orderId, pay_method) => {
  return api.post(`/api/orders/${orderId}/pay`, { pay_method })
} 