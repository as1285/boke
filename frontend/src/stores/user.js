import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '../utils/request'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)
  
  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.is_admin || false)
  
  // Actions
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  const setUserInfo = (info) => {
    userInfo.value = info
  }
  
  const login = async (credentials) => {
    const res = await request.post('/auth/login', credentials)
    setToken(res.data.token)
    setUserInfo(res.data.user)
    return res
  }
  
  const register = async (data) => {
    const res = await request.post('/auth/register', data)
    setToken(res.data.token)
    setUserInfo(res.data.user)
    return res
  }
  
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }
  
  const fetchUserInfo = async () => {
    if (!token.value) return
    try {
      const res = await request.get('/auth/me')
      setUserInfo(res.data)
    } catch (error) {
      logout()
    }
  }
  
  // 初始化时获取用户信息
  if (token.value) {
    fetchUserInfo()
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    isAdmin,
    login,
    register,
    logout,
    fetchUserInfo
  }
})
