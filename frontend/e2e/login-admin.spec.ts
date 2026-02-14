import { test, expect } from '@playwright/test'

test('管理员登录并访问后台', async ({ page }) => {
  await page.goto('/login')

  await page.getByLabel('用户名').fill('admin')
  await page.getByLabel('密码').fill('Admin@123456')
  await page.getByRole('button', { name: '登录' }).click()

  await expect(page).toHaveURL(/\/$/)

  await page.goto('/admin')
  await expect(page).toHaveURL(/\/admin/)
  await expect(page.getByText('后台管理')).toBeVisible()
  await expect(page.getByText('返回前台')).toBeVisible()
})

