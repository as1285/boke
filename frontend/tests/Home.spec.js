import { describe, it, expect, vi } from 'vitest'
import { mount, shallowMount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'

vi.mock('@/api/posts', () => {
  return {
    getPosts: vi.fn().mockResolvedValue({
      code: 200,
      msg: 'ok',
      data: { items: [], total: 0 }
    })
  }
})

const routes = [{ path: '/', component: Home }]
const router = createRouter({ history: createWebHistory(), routes })

describe('Home.vue', () => {
  it('renders empty state when no posts', async () => {
    const wrapper = shallowMount(Home, {
      global: {
        plugins: [router],
        stubs: {
          'el-input': true,
          'el-button': true,
          'el-icon': true,
          'el-skeleton': true,
          'el-empty': true,
          'el-card': true,
          'el-tag': true,
          'el-pagination': true
        }
      }
    })
    await router.isReady?.()
    // wait microtasks for onMounted fetchPosts
    await Promise.resolve()
    expect(wrapper.html()).toContain('暂无文章')
  })
})
