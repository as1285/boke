import { vi } from 'vitest'

// Mock Element Plus message to avoid DOM noise
const noop = () => {}
vi.mock('element-plus', () => {
  return {
    ElMessage: {
      success: noop,
      warning: noop,
      error: noop
    }
  }
})

// Mock Pinia user store used in request interceptors
vi.mock('@/stores/user', () => {
  return {
    useUserStore: () => ({
      token: '',
      logout: noop
    })
  }
})
