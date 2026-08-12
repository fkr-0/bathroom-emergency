#!/usr/bin/env node
/** Browser-level responsive and interaction verification for the Pages package. */
import { createServer } from 'node:http';
import { readFile, stat, mkdir } from 'node:fs/promises';
import { extname, join, normalize, resolve } from 'node:path';
import { chromium } from 'playwright';

const ROOT = resolve(import.meta.dirname, '..');
const SITE = join(ROOT, 'build', 'site');
const QA = join(ROOT, 'build', 'qa', 'site');
const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml', '.pdf': 'application/pdf', '.md': 'text/markdown; charset=utf-8',
  '.webmanifest': 'application/manifest+json', '.txt': 'text/plain; charset=utf-8',
};

function safePath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split('?')[0]);
  const relative = normalize(decoded).replace(/^[/\\]+/, '');
  const candidate = resolve(SITE, relative || 'index.html');
  if (!candidate.startsWith(SITE)) return null;
  return candidate;
}

const server = createServer(async (request, response) => {
  try {
    let file = safePath(request.url || '/');
    if (!file) throw new Error('invalid path');
    const info = await stat(file).catch(() => null);
    if (info?.isDirectory()) file = join(file, 'index.html');
    const body = await readFile(file);
    response.writeHead(200, { 'content-type': MIME[extname(file)] || 'application/octet-stream' });
    response.end(body);
  } catch {
    const body = await readFile(join(SITE, '404.html'));
    response.writeHead(404, { 'content-type': 'text/html; charset=utf-8' });
    response.end(body);
  }
});

await mkdir(QA, { recursive: true });
await new Promise(resolveReady => server.listen(0, '127.0.0.1', resolveReady));
const address = server.address();
const port = typeof address === 'object' && address ? address.port : 0;
const origin = `http://127.0.0.1:${port}`;
const browser = await chromium.launch({ headless: true });
const failures = [];

async function inspect(name, path, viewport, targetSelectors = [], fullPage = true) {
  const context = await browser.newContext({ viewport, colorScheme: 'light' });
  const page = await context.newPage();
  const consoleErrors = [];
  const externalRequests = [];
  page.on('console', message => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('pageerror', error => consoleErrors.push(String(error)));
  page.on('request', request => {
    const url = new URL(request.url());
    if (!['data:', 'blob:'].includes(url.protocol) && url.origin !== origin) externalRequests.push(request.url());
  });
  const response = await page.goto(`${origin}${path}`, { waitUntil: 'networkidle' });
  if (!response?.ok()) failures.push(`${name}: HTTP ${response?.status()}`);
  if (!(await page.locator('main').isVisible())) failures.push(`${name}: main content not visible`);
  const overflow = await page.evaluate(() => ({
    body: document.body.scrollWidth,
    root: document.documentElement.scrollWidth,
    viewport: document.documentElement.clientWidth,
  }));
  if (Math.max(overflow.body, overflow.root) > overflow.viewport + 1) {
    failures.push(`${name}: horizontal overflow ${JSON.stringify(overflow)}`);
  }
  for (const selector of targetSelectors) {
    const targets = page.locator(selector);
    for (let index = 0; index < await targets.count(); index += 1) {
      const target = targets.nth(index);
      if (!(await target.isVisible())) continue;
      const box = await target.boundingBox();
      if (!box || box.width < 43.5 || box.height < 43.5) {
        failures.push(`${name}: touch target ${selector}[${index}] is ${box ? `${box.width.toFixed(1)}x${box.height.toFixed(1)}` : 'unmeasurable'}`);
      }
    }
  }
  if (consoleErrors.length) failures.push(`${name}: console errors: ${consoleErrors.join(' | ')}`);
  if (externalRequests.length) failures.push(`${name}: external runtime requests: ${externalRequests.join(', ')}`);
  await page.screenshot({ path: join(QA, `${name}.png`), fullPage });
  await context.close();
}

try {
  const siteMobileTargets = ['.nav-toggle', '.theme-toggle', '.emergency-strip a', '.button'];
  for (const [name, path] of [['landing', '/'], ['deployment', '/deploy/'], ['downloads', '/downloads/']]) {
    await inspect(`${name}-desktop`, path, { width: 1440, height: 1000 });
    await inspect(`${name}-mobile`, path, { width: 390, height: 844 }, siteMobileTargets);
    await inspect(`${name}-narrow`, path, { width: 320, height: 844 }, siteMobileTargets);
  }
  await inspect('guide-mobile', '/guide/', { width: 390, height: 844 }, ['.app-bar .brand', '.app-bar button'], false);
  await inspect('guide-narrow', '/guide/', { width: 320, height: 844 }, ['.app-bar .brand', '.app-bar button'], false);
  await inspect('green-book-narrow', '/routes/O/green-book-body-owners-manual.html', { width: 320, height: 844 }, ['.app-bar .brand', '.app-bar button'], false);

  const mobileContext = await browser.newContext({ viewport: { width: 320, height: 844 } });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto(`${origin}/`, { waitUntil: 'networkidle' });
  await mobilePage.locator('.nav-toggle').click();
  const mobileMenu = await mobilePage.locator('#site-nav').boundingBox();
  const mobileViewport = await mobilePage.evaluate(() => document.documentElement.clientWidth);
  if (!mobileMenu || mobileMenu.x < 0 || mobileMenu.x + mobileMenu.width > mobileViewport + 1) {
    failures.push(`landing-narrow: open mobile menu escapes viewport: ${JSON.stringify({ mobileMenu, mobileViewport })}`);
  }
  const mobileLinks = mobilePage.locator('#site-nav a');
  for (let index = 0; index < await mobileLinks.count(); index += 1) {
    const box = await mobileLinks.nth(index).boundingBox();
    if (!box || box.height < 43.5) failures.push(`landing-narrow: nav link ${index} is below 44px touch height`);
  }
  await mobilePage.keyboard.press('Escape');
  if (await mobilePage.locator('#site-nav').evaluate(node => node.classList.contains('open'))) {
    failures.push('landing-narrow: Escape did not close the mobile navigation');
  }
  if (!(await mobilePage.locator('.nav-toggle').evaluate(node => node === document.activeElement))) {
    failures.push('landing-narrow: closing mobile navigation did not restore focus to Menu');
  }
  await mobileContext.close();

  const readerContext = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const readerPage = await readerContext.newPage();
  await readerPage.goto(`${origin}/guide/`, { waitUntil: 'networkidle' });
  const guideCanonical = await readerPage.locator('link[rel="canonical"]').getAttribute('href');
  if (guideCanonical !== 'https://be.fkr.dev/guide/') failures.push(`guide: unexpected canonical URL ${guideCanonical}`);
  await readerPage.locator('#toc-toggle').click();
  const readerLinks = readerPage.locator('.reader-links a');
  if (await readerLinks.count() !== 2) failures.push(`guide-mobile: expected 2 online edition links, found ${await readerLinks.count()}`);
  const expectedReaderLinks = ['https://be.fkr.dev/', 'https://be.fkr.dev/files/guide.pdf'];
  for (let index = 0; index < Math.min(2, await readerLinks.count()); index += 1) {
    const href = await readerLinks.nth(index).getAttribute('href');
    if (href !== expectedReaderLinks[index]) failures.push(`guide-mobile: reader link ${index} is ${href}`);
    const box = await readerLinks.nth(index).boundingBox();
    if (!box || box.height < 43.5) failures.push(`guide-mobile: reader link ${index} is below 44px touch height`);
  }
  await readerPage.keyboard.press('Escape');
  if (await readerPage.locator('body').evaluate(node => node.classList.contains('toc-open'))) failures.push('guide-mobile: Escape did not close Contents');
  if (!(await readerPage.locator('#toc-toggle').evaluate(node => node === document.activeElement))) failures.push('guide-mobile: closing Contents did not restore focus');
  await readerContext.close();

  const context = await browser.newContext({ viewport: { width: 1024, height: 900 } });
  const page = await context.newPage();
  await page.goto(`${origin}/guide/`, { waitUntil: 'networkidle' });
  if (await page.locator('#TOC a[aria-current="location"]').count() !== 1) {
    failures.push('guide-desktop: scroll-aware TOC did not expose exactly one current location');
  }

  await page.goto(`${origin}/routes/O/green-book-body-owners-manual.html`, { waitUntil: 'networkidle' });
  const routeCanonical = await page.locator('link[rel="canonical"]').getAttribute('href');
  if (routeCanonical !== 'https://be.fkr.dev/routes/O/green-book-body-owners-manual.html') failures.push(`green-book: unexpected canonical URL ${routeCanonical}`);
  const routePdf = await page.locator('.reader-links a').filter({ hasText: 'A4 PDF' }).getAttribute('href');
  if (routePdf !== 'https://be.fkr.dev/routes/O/green-book-body-owners-manual.pdf') failures.push(`green-book: unexpected PDF link ${routePdf}`);

  await page.goto(`${origin}/deploy/`, { waitUntil: 'networkidle' });
  const beforeTheme = await page.locator('html').getAttribute('data-theme');
  await page.locator('[data-theme-toggle]').click();
  const afterTheme = await page.locator('html').getAttribute('data-theme');
  if (beforeTheme === afterTheme) failures.push('theme toggle did not change the document theme');

  const boxes = page.locator('[data-deployment-planner] input[type="checkbox"]');
  const plannerItems = page.locator('.planner-item');
  await plannerItems.nth(0).click({ force: true });
  await plannerItems.nth(1).click({ force: true });
  const progress = await page.locator('[data-progress-number]').textContent();
  if (progress !== '33%') failures.push(`deployment planner expected 33%, found ${progress}`);
  await page.reload({ waitUntil: 'networkidle' });
  if (!(await boxes.nth(0).isChecked()) || !(await boxes.nth(1).isChecked())) {
    failures.push('deployment planner did not persist local checklist state');
  }

  await page.goto(`${origin}/downloads/`, { waitUntil: 'networkidle' });
  await page.locator('[data-download-filter="routes"]').click();
  if (!(await page.locator('section[data-download-group="routes"]').first().isVisible())) {
    failures.push('route download filter did not reveal route section');
  }
  if (await page.locator('section[data-download-group="master"]').isVisible()) {
    failures.push('route download filter did not hide master section');
  }
  await context.close();
} finally {
  await browser.close();
  await new Promise(resolveClosed => server.close(resolveClosed));
}

if (failures.length) {
  console.error(`Site browser verification failed:\n- ${failures.join('\n- ')}`);
  process.exit(1);
}
console.log('Site browser verification passed: desktop, 390px, and 320px responsive coverage including the complete guide and a standalone book; no overflow or remote runtime requests; 44px mobile controls; and working navigation, theme, planner persistence, and download filters.');
