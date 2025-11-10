const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // 等待页面加载
  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  
  // 检查关键元素的样式
  const header = await page.locator('header').first();
  const headerBg = await header.evaluate(el => window.getComputedStyle(el).backgroundColor);
  console.log('Header background:', headerBg);
  
  const statsCards = await page.locator('[class*="bg-white"]').first();
  const cardBg = await statsCards.evaluate(el => window.getComputedStyle(el).backgroundColor);
  console.log('Card background:', cardBg);
  
  // 检查 primary 颜色
  const primaryButton = await page.locator('[class*="primary"]').first();
  if (await primaryButton.count() > 0) {
    const primaryColor = await primaryButton.evaluate(el => window.getComputedStyle(el).color);
    console.log('Primary color:', primaryColor);
  }
  
  // 截图
  await page.screenshot({ path: 'page-check.png', fullPage: true });
  console.log('Screenshot saved to page-check.png');
  
  await browser.close();
})();
