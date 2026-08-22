const fs = require('fs');
const path = require('path');
const { chromium } = require('../frontend/node_modules/playwright');

const BASE_URL = 'https://launchgood-ops-copilot.vercel.app';
const SCREENSHOT_DIR = path.join(__dirname, '..', 'docs', 'assets', 'screenshots');

if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

async function captureAll() {
  console.log(`Starting Playwright browser automation for ${BASE_URL}...`);
  const browser = await chromium.launch({ headless: true });

  // 1. Desktop Viewport (1440 x 900)
  const desktopContext = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await desktopContext.newPage();

  // Step 1: Dashboard Baseline
  console.log('1. Capturing Dashboard Baseline (1440x900)...');
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01-command-center-dashboard.png') });

  // Step 2: Case Review Workspace (case-1001)
  console.log('2. Capturing Case Review Workspace (case-1001)...');
  await page.goto(`${BASE_URL}/cases/case-1001`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02-case-1001-review-workspace.png') });

  // Step 3: Conflicting Evidence (case-1003)
  console.log('3. Capturing Conflicting Evidence (case-1003)...');
  await page.goto(`${BASE_URL}/cases/case-1003`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03-case-1003-conflicting-evidence.png') });

  // Step 4: No Policy Found (case-1004)
  console.log('4. Capturing No Policy Found (case-1004)...');
  await page.goto(`${BASE_URL}/cases/case-1004`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '04-case-1004-no-policy-grounding.png') });

  // Step 5: Decision Rail Submission & Audit Trail (case-1001)
  console.log('5. Capturing Decision Rail & Audit Trail (case-1001)...');
  await page.goto(`${BASE_URL}/cases/case-1001`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  // Scroll down to Decision Rail / Audit Trail area
  await page.evaluate(() => window.scrollBy(0, 500));
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '05-decision-rail-submission.png') });

  // Step 6: Evaluation & Benchmarks
  console.log('6. Capturing Evaluation & Benchmarks (/evaluation)...');
  await page.goto(`${BASE_URL}/evaluation`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, '06-evaluation-benchmark.png') });

  await desktopContext.close();

  // 2. Tablet Viewport (1024 x 768)
  console.log('7. Capturing Tablet Viewport (1024x768)...');
  const tabletContext = await browser.newContext({
    viewport: { width: 1024, height: 768 }
  });
  const tabletPage = await tabletContext.newPage();
  await tabletPage.goto(BASE_URL, { waitUntil: 'networkidle' });
  await tabletPage.waitForTimeout(2000);
  await tabletPage.screenshot({ path: path.join(SCREENSHOT_DIR, '07-responsive-tablet-1024x768.png') });
  await tabletContext.close();

  // 3. Mobile Viewport (390 x 844)
  console.log('8. Capturing Mobile Viewport (390x844)...');
  const mobileContext = await browser.newContext({
    viewport: { width: 390, height: 844 }
  });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto(BASE_URL, { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(2000);
  await mobilePage.screenshot({ path: path.join(SCREENSHOT_DIR, '08-responsive-mobile-390x844.png') });
  await mobileContext.close();

  await browser.close();
  console.log('Successfully captured all 8 screenshots under docs/assets/screenshots/!');
}

captureAll().catch(err => {
  console.error('Error during screenshot capture:', err);
  process.exit(1);
});
