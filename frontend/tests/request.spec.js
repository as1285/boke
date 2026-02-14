import { describe, it, expect, vi } from 'vitest'
import MockAdapter from 'axios-mock-adapter'
import request from '@/utils/request'

describe('utils/request', () => {
  it('uses /api as baseURL', () => {
    expect(request.defaults.baseURL).toBe('/api')
  })

  it('resolves when backend code===200 and unwraps data', async () => {
    const mock = new MockAdapter(request)
    mock.onGet('/ok').reply(200, { code: 200, msg: 'ok', data: { x: 1 } })
    const res = await request.get('/ok')
    expect(res.data).toEqual({ x: 1 })
    mock.restore()
  })

  it('rejects and shows message when backend code!==200', async () => {
    const mock = new MockAdapter(request)
    const errorSpy = vi.spyOn((await import('element-plus')).ElMessage, 'error')
    mock.onGet('/err').reply(200, { code: 400, msg: 'bad', data: null })
    await expect(request.get('/err')).rejects.toThrow()
    expect(errorSpy).toHaveBeenCalled()
    mock.restore()
    errorSpy.mockRestore()
  })
})
