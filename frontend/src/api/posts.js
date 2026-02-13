import request from '../utils/request'

export const getPosts = (params) => request.get('/posts', { params })
export const getPost = (slug) => request.get(`/posts/${slug}`)
export const createPost = (data) => request.post('/posts', data)
export const updatePost = (id, data) => request.put(`/posts/${id}`, data)
export const deletePost = (id) => request.delete(`/posts/${id}`)

export const getCategories = () => request.get('/categories')
export const getTags = () => request.get('/tags')

export const getComments = (postId, params) => request.get(`/posts/${postId}/comments`, { params })
export const createComment = (postId, data) => request.post(`/posts/${postId}/comments`, data)
export const deleteComment = (id) => request.delete(`/comments/${id}`)
