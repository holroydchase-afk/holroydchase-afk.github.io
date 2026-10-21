// Renders tools/share-card.html to assets/share-card.png with the preinstalled Playwright.
// Run from the repo root: node tools/make_share_card.mjs
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
await page.goto(pathToFileURL(resolve('tools/share-card.html')).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: 'assets/share-card.png' });
await browser.close();
console.log('Wrote assets/share-card.png');
