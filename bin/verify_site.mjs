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

async function auditDarkContrast(page, name) {
  const issues = await page.evaluate(() => {
    const parseColor = value => {
      const text = value.trim().toLowerCase();
      if (text === 'transparent') return { r: 0, g: 0, b: 0, a: 0 };
      let match = text.match(/^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+))?\s*\)$/);
      if (match) return { r: +match[1], g: +match[2], b: +match[3], a: match[4] == null ? 1 : +match[4] };
      match = text.match(/^color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\)$/);
      if (match) return { r: +match[1] * 255, g: +match[2] * 255, b: +match[3] * 255, a: match[4] == null ? 1 : +match[4] };
      match = text.match(/^#([0-9a-f]{6})$/i);
      if (match) return { r: parseInt(match[1].slice(0, 2), 16), g: parseInt(match[1].slice(2, 4), 16), b: parseInt(match[1].slice(4, 6), 16), a: 1 };
      return null;
    };
    const composite = (front, back) => {
      const alpha = front.a + back.a * (1 - front.a);
      if (!alpha) return { r: 0, g: 0, b: 0, a: 0 };
      return {
        r: (front.r * front.a + back.r * back.a * (1 - front.a)) / alpha,
        g: (front.g * front.a + back.g * back.a * (1 - front.a)) / alpha,
        b: (front.b * front.a + back.b * back.a * (1 - front.a)) / alpha,
        a: alpha,
      };
    };
    const luminance = color => {
      const channel = value => {
        const v = value / 255;
        return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4;
      };
      return .2126 * channel(color.r) + .7152 * channel(color.g) + .0722 * channel(color.b);
    };
    const ratio = (left, right) => {
      const a = luminance(left), b = luminance(right);
      return (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
    };
    const effectiveBackground = element => {
      const chain = [];
      for (let node = element; node; node = node.parentElement) chain.unshift(node);
      let background = { r: 255, g: 255, b: 255, a: 1 };
      for (const node of chain) {
        const parsed = parseColor(getComputedStyle(node).backgroundColor);
        if (parsed && parsed.a > 0) background = composite(parsed, background);
      }
      return background;
    };
    const hasOwnText = element => [...element.childNodes].some(node => node.nodeType === Node.TEXT_NODE && node.textContent.trim());
    const scope = document.querySelectorAll('.app-bar *, #TOC *, main .chapter *, main .standalone-subguide > *');
    const found = [];
    for (const element of scope) {
      if (!(element instanceof HTMLElement) || !hasOwnText(element) || !element.getClientRects().length) continue;
      if (element.closest('[aria-hidden="true"]')) continue;
      const style = getComputedStyle(element);
      if (style.visibility === 'hidden' || style.display === 'none') continue;
      const foreground = parseColor(style.color);
      if (!foreground) continue;
      let opacity = 1;
      for (let node = element; node; node = node.parentElement) opacity *= Number.parseFloat(getComputedStyle(node).opacity || '1');
      foreground.a *= opacity;
      const background = effectiveBackground(element);
      const visibleForeground = composite(foreground, background);
      const contrast = ratio(visibleForeground, background);
      const size = Number.parseFloat(style.fontSize);
      const weight = Number.parseInt(style.fontWeight, 10) || 400;
      const required = size >= 24 || (size >= 18.66 && weight >= 700) ? 3 : 4.5;
      if (contrast + .02 < required) {
        found.push({
          tag: element.tagName.toLowerCase(),
          classes: element.className,
          text: element.textContent.replace(/\s+/g, ' ').trim().slice(0, 90),
          contrast: Number(contrast.toFixed(2)),
          required,
          color: style.color,
          background: style.backgroundColor,
        });
      }
    }
    return found.slice(0, 30);
  });
  if (issues.length) failures.push(`${name}: dark-mode contrast failures: ${JSON.stringify(issues)}`);
}

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
  const landingRepo = mobilePage.locator('.site-header .repository-link');
  const landingRepoBox = await landingRepo.boundingBox();
  if (!(await landingRepo.isVisible()) || !landingRepoBox || landingRepoBox.height < 43.5) {
    failures.push(`landing-narrow: prominent repository link is missing or below 44px touch height: ${JSON.stringify(landingRepoBox)}`);
  }
  if (await landingRepo.getAttribute('href') !== 'https://github.com/fkr-0/bathroom-emergency') {
    failures.push(`landing-narrow: repository link points to ${await landingRepo.getAttribute('href')}`);
  }
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
  await readerPage.waitForTimeout(80);
  const guideBrandMark = (await readerPage.locator('.brand-guide').textContent())?.trim();
  if (guideBrandMark !== 'BE') failures.push(`guide-mobile: expected visible product mark BE, found ${guideBrandMark}`);
  const guideBrandLabel = await readerPage.locator('.reader-identity .brand').getAttribute('aria-label');
  if (!guideBrandLabel?.startsWith('Bathroom Emergency Guide — ')) failures.push(`guide-mobile: product mark does not expand accessibly: ${guideBrandLabel}`);
  const initialGuideAddress = (await readerPage.locator('[data-reader-address]').textContent())?.trim();
  if (initialGuideAddress !== 'Shelf') failures.push(`guide-mobile: expected top-left address Shelf, found ${initialGuideAddress}`);
  const initialGuideIdentity = (await readerPage.locator('.reader-identity .brand').textContent())?.replace(/\s+/g, '').trim();
  if (initialGuideIdentity !== 'BE/Shelf') failures.push(`guide-mobile: expected BE/Shelf identity, found ${initialGuideIdentity}`);
  const readerRepo = readerPage.locator('.app-bar .repository-link');
  const readerRepoBox = await readerRepo.boundingBox();
  if (!(await readerRepo.isVisible()) || !readerRepoBox || readerRepoBox.height < 43.5) {
    failures.push(`guide-mobile: prominent repository link is missing or below 44px touch height: ${JSON.stringify(readerRepoBox)}`);
  }
  if (await readerRepo.getAttribute('href') !== 'https://github.com/fkr-0/bathroom-emergency') {
    failures.push(`guide-mobile: repository link points to ${await readerRepo.getAttribute('href')}`);
  }
  const orangeMobileSection = readerPage.locator('main .standalone-subguide[data-subguide="H"] h2[id^="beg-"]').first();
  await orangeMobileSection.evaluate(node => window.scrollTo({ top: node.getBoundingClientRect().top + window.scrollY - 72, behavior: 'instant' }));
  await readerPage.waitForTimeout(120);
  const orangeGuideAddress = (await readerPage.locator('[data-reader-address]').textContent())?.trim() || '';
  if (!orangeGuideAddress.startsWith('dis.')) failures.push(`guide-mobile: Orange scroll did not update top-left address, found ${orangeGuideAddress}`);
  const orangeGuideIdentity = (await readerPage.locator('.reader-identity .brand').textContent())?.replace(/\s+/g, '').trim() || '';
  if (!orangeGuideIdentity.startsWith('BE/dis.') || orangeGuideIdentity === initialGuideIdentity) failures.push(`guide-mobile: BE identity did not track Orange scroll, found ${orangeGuideIdentity}`);
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

  await readerPage.goto(`${origin}/routes/O/green-book-body-owners-manual.html`, { waitUntil: 'networkidle' });
  await readerPage.waitForTimeout(80);
  const greenInitialAddress = (await readerPage.locator('[data-reader-address]').textContent())?.trim();
  if (greenInitialAddress !== 'O') failures.push(`green-book-mobile: expected top-left address O, found ${greenInitialAddress}`);
  const greenInitialIdentity = (await readerPage.locator('.reader-identity .brand').textContent())?.replace(/\s+/g, '').trim();
  if (greenInitialIdentity !== 'BE/O') failures.push(`green-book-mobile: expected BE/O identity, found ${greenInitialIdentity}`);
  const greenMobileSection = readerPage.locator('main h2[id^="beg-"]').first();
  await greenMobileSection.evaluate(node => window.scrollTo({ top: node.getBoundingClientRect().top + window.scrollY - 72, behavior: 'instant' }));
  await readerPage.waitForTimeout(120);
  const greenSectionAddress = (await readerPage.locator('[data-reader-address]').textContent())?.trim() || '';
  if (greenSectionAddress === 'O' || !greenSectionAddress.includes('.')) failures.push(`green-book-mobile: section scroll did not expose a short stable address, found ${greenSectionAddress}`);
  const greenSectionIdentity = (await readerPage.locator('.reader-identity .brand').textContent())?.replace(/\s+/g, '').trim() || '';
  if (!greenSectionIdentity.startsWith('BE/') || greenSectionIdentity === greenInitialIdentity) failures.push(`green-book-mobile: BE identity did not change with section scroll, found ${greenSectionIdentity}`);
  await readerContext.close();

  const context = await browser.newContext({ viewport: { width: 1024, height: 900 } });
  const page = await context.newPage();
  await page.goto(`${origin}/guide/`, { waitUntil: 'networkidle' });
  if (await page.locator('#TOC a[aria-current="location"]').count() !== 1) {
    failures.push('guide-desktop: scroll-aware TOC did not expose exactly one current location');
  }
  const tocBefore = await page.locator('#TOC').boundingBox();
  const guideBefore = await page.locator('#guide').boundingBox();
  if (!tocBefore || !guideBefore || tocBefore.x + tocBefore.width >= guideBefore.x) {
    failures.push(`guide-desktop: floating TOC is not positioned to the left of the reader: ${JSON.stringify({ tocBefore, guideBefore })}`);
  }
  await page.evaluate(() => window.scrollTo({ top: 900, behavior: 'instant' }));
  await page.waitForTimeout(80);
  const tocPinned = await page.locator('#TOC').boundingBox();
  const copperSection = page.locator('main .standalone-subguide[data-subguide="R"] h2[id^="beg-"]').first();
  await copperSection.evaluate(node => window.scrollTo({ top: node.getBoundingClientRect().top + window.scrollY - 90, behavior: 'instant' }));
  await page.waitForTimeout(120);
  const tocAfter = await page.locator('#TOC').boundingBox();
  if (!tocPinned || !tocAfter || Math.abs(tocPinned.y - tocAfter.y) > 2) {
    failures.push(`guide-desktop: floating TOC did not stay pinned while scrolling: ${JSON.stringify({ tocPinned, tocAfter })}`);
  }
  const currentBook = await page.locator('#TOC .reader-toc-book.is-current-book > a').textContent();
  if (!currentBook?.trim().startsWith('R ·')) failures.push(`guide-desktop: expected Copper parent state after scroll, found ${currentBook}`);
  const copperAddress = (await page.locator('[data-reader-address]').textContent())?.trim() || '';
  if (!copperAddress.startsWith('ref.')) failures.push(`guide-desktop: Copper scroll did not update top-left address, found ${copperAddress}`);
  const activeTocLink = page.locator('#TOC a[aria-current="location"]');
  const activeTocBox = await activeTocLink.boundingBox();
  if (!tocAfter || !activeTocBox || activeTocBox.top < tocAfter.top - 1 || activeTocBox.bottom > tocAfter.bottom + 1) {
    failures.push(`guide-desktop: active TOC entry did not auto-follow into view: ${JSON.stringify({ tocAfter, activeTocBox })}`);
  }

  await page.goto(`${origin}/guide/#BEG:H:G:003`, { waitUntil: 'networkidle' });
  if (page.url().split('#')[1] !== 'BEG:H:G:003') failures.push(`guide-desktop: literal stable fragment was not preserved in URL: ${page.url()}`);
  const stableTarget = page.locator('[id="BEG:H:G:003"]');
  if (await stableTarget.count() !== 1) failures.push(`guide-desktop: expected one #BEG:H:G:003 target, found ${await stableTarget.count()}`);
  const stableLinks = page.locator('a[href$="#BEG:H:G:003"]');
  if (await stableLinks.count() < 1) failures.push('guide-desktop: no rendered permalink points to #BEG:H:G:003');

  await page.goto(`${origin}/routes/O/green-book-body-owners-manual.html`, { waitUntil: 'networkidle' });
  const routeCanonical = await page.locator('link[rel="canonical"]').getAttribute('href');
  if (routeCanonical !== 'https://be.fkr.dev/routes/O/green-book-body-owners-manual.html') failures.push(`green-book: unexpected canonical URL ${routeCanonical}`);
  const routePdf = await page.locator('.reader-links a').filter({ hasText: 'A4 PDF' }).getAttribute('href');
  if (routePdf !== 'https://be.fkr.dev/routes/O/green-book-body-owners-manual.pdf') failures.push(`green-book: unexpected PDF link ${routePdf}`);

  const releaseMeta = JSON.parse(await readFile(join(SITE, 'meta', 'release.json'), 'utf8'));
  for (const [label, path] of [['landing', '/'], ['guide', '/guide/'], ['green-book', '/routes/O/green-book-body-owners-manual.html']]) {
    await page.goto(`${origin}${path}`, { waitUntil: 'networkidle' });
    const provenance = page.locator(path === '/guide/' || path.includes('/routes/') ? '.reader-provenance a' : '.site-provenance a');
    if (await provenance.count() !== 3) failures.push(`${label}: expected three build provenance links, found ${await provenance.count()}`);
    const hrefs = await provenance.evaluateAll(nodes => nodes.map(node => node.getAttribute('href')));
    const expected = [
      `https://github.com/fkr-0/bathroom-emergency/tree/v${releaseMeta.release}`,
      `https://github.com/fkr-0/bathroom-emergency/commit/${releaseMeta.revision}`,
      path === '/' ? 'meta/release.json' : (path === '/guide/' || path.includes('/routes/') ? 'https://be.fkr.dev/meta/release.json' : '../meta/release.json'),
    ];
    if (JSON.stringify(hrefs) !== JSON.stringify(expected)) failures.push(`${label}: provenance hrefs drifted: ${JSON.stringify(hrefs)}`);
    const repoLink = page.locator(path === '/guide/' || path.includes('/routes/') ? '.app-bar .repository-link' : '.site-header .repository-link');
    if (!(await repoLink.isVisible())) failures.push(`${label}: prominent repository control is not visible`);
    if (await repoLink.getAttribute('href') !== 'https://github.com/fkr-0/bathroom-emergency') failures.push(`${label}: prominent repository control drifted`);
  }

  await page.goto(`${origin}/guide/`, { waitUntil: 'networkidle' });
  await page.locator('#theme-toggle').click();
  if (await page.locator('html').getAttribute('data-theme') !== 'dark') failures.push('guide-dark: theme toggle did not enter dark mode');
  await auditDarkContrast(page, 'guide-dark');
  await page.screenshot({ path: join(QA, 'guide-dark.png'), fullPage: false });

  await page.goto(`${origin}/routes/H/orange-book-hazards-disasters.html`, { waitUntil: 'networkidle' });
  if (await page.locator('html').getAttribute('data-theme') !== 'dark') {
    await page.locator('#theme-toggle').click();
  }
  await auditDarkContrast(page, 'orange-book-dark');
  await page.screenshot({ path: join(QA, 'orange-book-dark.png'), fullPage: false });

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
