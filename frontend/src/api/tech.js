import request from '../utils/request'

export const getTestTechResources = (params) => request.get('/test-tech-resources', { params })
export const getTechCategories = () => request.get('/test-tech-resources/categories')
