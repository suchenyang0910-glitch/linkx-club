const { test, expect } = require('@playwright/test');

test('首页关键元素存在', async ({ page }) => {
  await page.goto('/');

  await expect(page.locator('header.site-header a.logo')).toBeVisible();
  await expect(page.locator('header.site-header a.logo img.logo-img')).toHaveAttribute('src', '/logo.jpg');

  const banner = page.locator('.banner-carousel');
  await expect(banner).toBeVisible();
  await expect(page.locator('.banner-slide')).toHaveCount(4);
  await expect(page.locator('.banner-slide.active')).toHaveCount(1);

  await expect(page.locator('.banner-dots .dot')).toHaveCount(4);

  const countryBtns = page.locator('.country-nav .country-btn');
  await expect(countryBtns).toHaveCount(5);

  const cards = page.locator('.article-grid > a.card');
  await expect(cards.first()).toBeVisible();
});

test('轮播图可手动切换', async ({ page }) => {
  await page.goto('/');

  const slides = page.locator('.banner-slide');
  const dots = page.locator('.banner-dots .dot');

  await expect(slides).toHaveCount(4);
  await expect(dots).toHaveCount(4);

  await expect(slides.nth(0)).toHaveClass(/active/);
  await dots.nth(1).click();
  await expect(slides.nth(1)).toHaveClass(/active/);
});
