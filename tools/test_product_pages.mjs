// Product page tests (WEB-M14): one template, the standard header everywhere, the demo in its frame.
// Plain node + playwright. Starts its own static server and serves a made-up stand-in for each product's demo
// (the real demos live in other repos), so it checks the portfolio side only. External hosts are blocked.
// Run: node tools/test_product_pages.mjs   (exit 1 on any failure)
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp", ".woff2": "font/woff2", ".jpg": "image/jpeg" };
const PRODUCTS = [
  { page: "family-photos.html", demo: "/hearth/", repo: "hearth", phone: true },
  { page: "ccwatts.html", demo: "/ccwatts/", repo: "ccwatts", phone: false },
];
const STUB = `<!doctype html><meta name=viewport content="width=device-width,initial-scale=1"><body style="margin:0">
<section aria-label="Demo" id="stub-bar" style="height:44px;background:#222;color:#fff">Demo bar</section><main id="app">stub app</main>`;
let missing = new Set();
const server = http.createServer((req, res) => {
  const u = new URL(req.url, "http://x");
  const p = decodeURIComponent(u.pathname);
  const prod = PRODUCTS.find(x => p === x.demo || p === x.demo + "index.html");
  if (prod) {
    if (missing.has(prod.demo)) { res.writeHead(404); return res.end("nf"); }
    res.writeHead(200, { "content-type": "text/html" });
    return res.end(STUB + (u.searchParams.has("bar") ? '<script src="/assets/demo-bar.js" defer></script>' : ""));
  }
  let f = path.join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, "index.html");
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const BASE = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();
const results = [];
async function check(name, fn) {
  try { await fn(); results.push([name, true, ""]); console.log("PASS " + name); }
  catch (e) { results.push([name, false, e.message]); console.log("FAIL " + name + "\n     " + e.message.split("\n").join("\n     ")); }
}
const ok = (c, m) => { if (!c) throw new Error(m); };

async function open(url, viewport) {
  const ctx = await browser.newContext({ viewport });
  const external = [], errors = [];
  await ctx.route("**/*", r => {
    const u = new URL(r.request().url());
    if (u.hostname === "127.0.0.1") return r.continue();
    external.push(u.hostname); return r.abort();
  });
  const page = await ctx.newPage();
  page.on("pageerror", e => errors.push(String(e)));
  page.on("console", m => { if (m.type() === "error" && !/404/.test(m.text())) errors.push(m.text()); });
  await page.goto(BASE + url, { waitUntil: "load" });
  await page.waitForTimeout(400);
  return { ctx, page, external, errors };
}
const LAPTOP = { width: 1366, height: 768 }, PHONE = { width: 390, height: 844 };

for (const p of PRODUCTS) {
  await check(`UNI-1 ${p.page}: standard header with all five links on a laptop`, async () => {
    const { ctx, page } = await open("/" + p.page, LAPTOP);
    const labels = await page.$$eval("header.site nav a", as => as.filter(a => a.offsetParent).map(a => a.textContent.trim()));
    ok(JSON.stringify(labels) === JSON.stringify(["Case studies", "Building", "Agents", "Resume", "Contact"]), "header links: " + labels);
    ok(await page.isVisible("header.site .dock"), "name and photo missing");
    ok(await page.isVisible("#tog"), "theme button missing");
    await ctx.close();
  });
  await check(`UNI-2 ${p.page}: demo loads in its frame, its own Demo bar is hidden, three controls`, async () => {
    const { ctx, page, external, errors } = await open("/" + p.page, LAPTOP);
    const fr = page.frames().find(f => f.url().includes(p.demo));
    ok(fr, "no frame at " + p.demo);
    ok(fr.url().includes("embed=1"), "frame url lacks embed=1: " + fr.url());
    await page.waitForFunction(() => document.querySelector(".view .wait")?.hidden, null, { timeout: 4000 });
    const barShown = await fr.$eval("#stub-bar", e => getComputedStyle(e).display);
    ok(barShown === "none", "the product's Demo bar still shows in the frame");
    for (const t of ["Reload", "Open full page", "Code"]) ok(await page.isVisible(`.view .bar >> text=${t}`), "missing control " + t);
    ok(external.length === 0, "external hosts: " + external);
    ok(errors.length === 0, "console errors: " + errors);
    await ctx.close();
  });
  await check(`UNI-3 ${p.page}: ${p.phone ? "phone" : "browser"} frame, phone shows a 390 wide screen`, async () => {
    const { ctx, page } = await open("/" + p.page, LAPTOP);
    ok(await page.isVisible(p.phone ? ".view .phone" : ".view .browser"), "wrong or missing frame");
    ok(!(await page.isVisible(p.phone ? ".view .browser" : ".view .phone")), "both frames present");
    if (p.phone) {
      const w = await page.frames().find(f => f.url().includes(p.demo)).evaluate(() => innerWidth);
      ok(w === 390, "the app sees a " + w + "px wide screen, want 390");
      const box = await page.locator(".view .phone").boundingBox();
      ok(box.y + box.height <= LAPTOP.height, `phone bottom at ${box.y + box.height}, window is ${LAPTOP.height} (WEB14-R3)`);
      const cap = await page.locator(".view .cap").boundingBox();
      ok(cap.y + cap.height <= LAPTOP.height + 40, "caption below the fold (WEB14-R3)");
      const sc = await page.locator(".phone .screen iframe").evaluate(e => getComputedStyle(e).transform);
      ok(sc === "none", "the app is scaled: " + sc + " (WEB14-R2)");
    }
    await ctx.close();
  });
  await check(`UNI-4 ${p.page}: one back link to Building, no sideways scroll at 390 and 1366`, async () => {
    for (const vp of [PHONE, LAPTOP]) {
      const { ctx, page } = await open("/" + p.page, vp);
      ok(await page.locator('a.crumb[href="/building.html"]').count() === 1, "back link to Building missing");
      ok(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)), "sideways scroll at " + vp.width);
      await ctx.close();
    }
  });
  await check(`UNI-5 ${p.page}: on a phone the demo sits right after the intro, before the facts`, async () => {
    const { ctx, page } = await open("/" + p.page, PHONE);
    const demoY = (await page.locator(".view").boundingBox()).y;
    const factsY = (await page.locator(".facts").boundingBox()).y;
    ok(demoY < factsY, `demo at ${demoY}, facts at ${factsY}`);
    await ctx.close();
  });
  await check(`UNI-11 ${p.page}: at 390 the controls share one row, 48px tall; Building is the current nav item`, async () => {
    const { ctx, page } = await open("/" + p.page, PHONE);
    const bs = await page.$$eval(".view .bar .btn", els => els.filter(e => e.offsetParent).map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.height)]; }));
    ok(bs.length >= 2 && new Set(bs.map(b => b[0])).size === 1, "controls wrap: " + JSON.stringify(bs));
    ok(bs.every(b => b[1] >= 48), "controls under 48px: " + JSON.stringify(bs));
    ok(await page.locator('header.site nav a[aria-current=page]').innerText() === "Building", "Building not marked current");
    await ctx.close();
  });
  await check(`UNI-6 try/${p.repo}.html: full screen keeps the header and the demo fills the window`, async () => {
    const { ctx, page } = await open(`/try/${p.repo}.html`, LAPTOP);
    ok(await page.isVisible("header.site .dock") && await page.isVisible("#tog"), "header missing");
    const box = await page.locator(".screen iframe").boundingBox();
    ok(box.width >= 1300 && box.height >= 550, `demo only ${box.width}x${box.height}`);
    ok(await page.locator(`a.crumb[href="/${p.page}"]`).count() === 1, "no way back to the product page");
    await ctx.close();
  });
}

await check("UNI-7 a demo that is down shows a plain message and a link to the code", async () => {
  missing = new Set(["/ccwatts/"]);
  const { ctx, page } = await open("/ccwatts.html", LAPTOP);
  ok(await page.isVisible(".view .down"), "no fallback message");
  ok(await page.locator('.view .down a[href*="github.com/holroydchase-afk/ccwatts"]').count() === 1, "no code link");
  await ctx.close(); missing = new Set();
});

await check("UNI-8 demo-bar.js draws the standard header on a direct visit, and nothing inside the product page frame", async () => {
  const { ctx, page } = await open("/hearth/?bar=1", LAPTOP);
  ok(await page.isVisible("#site-bar"), "no header on a direct visit");
  const labels = await page.$$eval("#site-bar nav a", as => as.filter(a => a.offsetParent).map(a => a.textContent.trim()));
  ok(JSON.stringify(labels) === JSON.stringify(["Case studies", "Building", "Agents", "Resume", "Contact"]), "links: " + labels);
  await ctx.close();
  const b = await open("/family-photos.html", LAPTOP);
  ok(b.page.frames().length > 1, "no frame");
  await b.ctx.close();
});

await check("UNI-12 Energy Scanner, Charlie, Crew Clock and Role Radar are off the portfolio: stubs redirect to Building, no try pages, no links, not in the sitemap", async () => {
  const fs = await import("node:fs");
  for (const slug of ["energy-scanner", "charlie", "crew-clock", "role-radar"]) {
    const stub = fs.readFileSync(path.join(ROOT, slug + ".html"), "utf8");
    ok(/http-equiv="refresh"[^>]*url=\/building\.html/.test(stub) && /noindex/.test(stub), slug + " stub should redirect to /building.html and be noindex");
    ok(!fs.existsSync(path.join(ROOT, "try/" + slug + ".html")), slug + " try page should be gone");
  }
  for (const f of ["index.html", "building.html", "agents.html", "resume.html", "sitemap.xml", "ccwatts.html", "family-photos.html"]) {
    // drop HTML comments with a plain scan (the hidden cards live in comments)
    const parts = fs.readFileSync(path.join(ROOT, f), "utf8").split("<!--");
    const t = parts[0] + parts.slice(1).map(p => p.slice(p.indexOf("-->") + 3)).join("");
    for (const slug of ["energy-scanner", "charlie", "crew-clock", "role-radar"]) ok(!t.includes(slug), f + " still mentions " + slug);
  }
});

await check("UNI-9 the theme choice carries into the page, and dark has no unreadable header", async () => {
  const { ctx, page } = await open("/ccwatts.html?theme=dark", LAPTOP);
  ok(await page.evaluate(() => document.documentElement.dataset.theme) === "dark", "dark not applied");
  const bg = await page.$eval("header.site", e => getComputedStyle(e).backgroundColor);
  ok(bg === "rgb(10, 10, 10)", "header background " + bg);
  await ctx.close();
});

await check("UNI-10 About, Studio and Console are moved stubs, not pages", async () => {
  for (const f of ["about.html", "studio.html", "pm-tools.html"]) {
    const t = fs.readFileSync(path.join(ROOT, f), "utf8");
    ok(t.includes('http-equiv="refresh"') && t.includes("noindex"), f + " is still a page");
  }
});

await browser.close();
server.close();
const failed = results.filter(r => !r[1]);
console.log(`\n${results.length - failed.length}/${results.length} passed`);
process.exit(failed.length ? 1 : 0);
