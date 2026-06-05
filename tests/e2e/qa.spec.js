const { test, expect } = require('@playwright/test');

test('关键静态资源可访问', async ({ request }) => {
  const assets = ['/logo.jpg', '/styles/global.v4.css', '/favicon.svg', '/images/linkx-og.png'];
  for (const url of assets) {
    const res = await request.get(url);
    expect(res.status(), url).toBe(200);
  }
});

test('不存在页面返回 404', async ({ request }) => {
  const res = await request.get('/__not_found__');
  expect(res.status()).toBe(404);
});

test('首页导航链接可跳转', async ({ page }) => {
  await page.goto('/');

  await page.locator('.desktop-nav a[href="/briefings/"]').click();
  await expect(page).toHaveURL(/\/briefings\/$/);
  await expect(page.getByRole('heading', { name: '每日简报', exact: true })).toBeVisible();

  await page.locator('.desktop-nav a[href="/analysis/"]').click();
  await expect(page).toHaveURL(/\/analysis\/$/);
  await expect(page.getByRole('heading', { name: '深度分析', exact: true })).toBeVisible();

  await page.locator('.desktop-nav a[href="/guestbook/"]').click();
  await expect(page).toHaveURL(/\/guestbook\/$/);
  await expect(page.getByRole('heading', { name: '讨论留言', exact: true })).toBeVisible();

  await page.locator('.desktop-nav a[href="/"]').click();
  await expect(page).toHaveURL(/\/$/);
});

test('首页国家入口可进入文章页', async ({ page }) => {
  await page.goto('/');

  const first = page.locator('.country-nav .country-btn').first();
  await first.click();
  await expect(page).toHaveURL(/\/article\/\d+$/);
  await expect(page.locator('main article h1')).toBeVisible();
});

test('轮播图自动切换', async ({ page }) => {
  await page.goto('/');

  const slides = page.locator('.banner-slide');
  await expect(slides).toHaveCount(4);

  const before = await page.locator('.banner-slide.active h2').innerText();
  await page.waitForTimeout(5500);
  const after = await page.locator('.banner-slide.active h2').innerText();
  expect(after).not.toBe(before);
});
