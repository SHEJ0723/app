import api from './index'

export const getBills = async (params = {}) => {
  return api.get('/api/bills', { params })
}

export const createBill = async (data) => {
  return api.post('/api/bills', data)
}

export const deleteBill = async (billId) => {
  return api.delete(`/api/bills/${billId}`)
} 