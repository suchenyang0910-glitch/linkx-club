const { test, expect } = require('@playwright/test');

test('分析页关键元素与内容渲染', async ({ page }) => {
  await page.goto('/analysis/');

  await expect(page.locator('header.site-header a.logo img.logo-img')).toHaveAttribute('src', '/logo.jpg');
  await expect(page.getByRole('heading', { name: '深度分析', exact: true })).toBeVisible();

  const grid = page.locator('#analysis-grid');
  await expect(grid).toBeVisible();
  await page.waitForSelector('#analysis-grid a.card', { timeout: 15000 });
  const count = await grid.locator('a.card').count();
  expect(count).toBeGreaterThan(0);
});

test('简报页关键元素与内容渲染', async ({ page }) => {
  await page.goto('/briefings/');

  await expect(page.locator('header.site-header a.logo img.logo-img')).toHaveAttribute('src', '/logo.jpg');
  await expect(page.getByRole('heading', { name: '每日简报', exact: true })).toBeVisible();

  const grid = page.locator('#briefing-grid');
  await expect(grid).toBeVisible();
  await page.waitForSelector('#briefing-grid a.card', { timeout: 15000 });
  const count = await grid.locator('a.card').count();
  expect(count).toBeGreaterThan(0);
});

test('文章页核心结构/分享/评论挂载', async ({ page }) => {
  await page.goto('/article/55');

  await expect(page.locator('header.site-header a.logo img.logo-img')).toHaveAttribute('src', '/logo.jpg');
  await expect(page.locator('main article h1')).toBeVisible();

  await expect(page.locator('.share-section')).toBeVisible();
  await expect(page.locator('.share-buttons .share-btn')).toHaveCount(4);

  await expect(page.locator('#comment-widget')).toBeVisible();
});

test('移动端菜单可打开与关闭', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');

  const hamburger = page.locator('button.hamburger');
  await expect(hamburger).toBeVisible();

  const sidebar = page.locator('#sidebar');
  const overlay = page.locator('#sidebarOverlay');

  await hamburger.click();
  await expect(sidebar).toHaveClass(/open/);
  await expect(overlay).toHaveClass(/open/);

  await overlay.click();
  await expect(sidebar).not.toHaveClass(/open/);
  await expect(overlay).not.toHaveClass(/open/);
});
