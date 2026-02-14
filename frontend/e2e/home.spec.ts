import { test, expect } from '@playwright/test'

test('首页展示文章列表并可进入详情页', async ({ page }) => {
  await page.goto('/')

  // 等待列表或空状态
  const postList = page.locator('.post-card')
  const emptyState = page.getByText('暂无文章')
  await Promise.race([
    postList.first().waitFor({ state: 'visible', timeout: 15000 }),
    emptyState.waitFor({ state: 'visible', timeout: 15000 })
  ])

  const hasPosts = await postList.first().isVisible().catch(() => false)
  if (hasPosts) {
    await postList.first().click()
    await expect(page).toHaveURL(/\/post\//)
    await expect(page.locator('.post-title')).toBeVisible()
    await expect(page.locator('.markdown-body')).toBeVisible()
  } else {
    await expect(emptyState).toBeVisible()
  }
})

