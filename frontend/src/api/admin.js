import request from '../utils/request'

// 日志模块
export const getLogs = (params) => request.get('/admin/logs', { params })
export const getLogsStats = () => request.get('/admin/logs/stats')

// 接口文档模块
export const getApiDocs = () => request.get('/admin/api-docs')

// 用户管理模块
export const getUsers = (params) => request.get('/admin/users', { params })
export const getUsersStats = () => request.get('/admin/users/stats')
export const deleteUser = (id) => request.delete(`/admin/users/${id}`)
export const toggleUserAdmin = (id) => request.put(`/admin/users/${id}/toggle-admin`)
