// Energy Scanner demo UX tests (UX-R1, R2, R3, R4, R6, R11 + no horizontal scroll).
// Plain node + playwright. Starts its own static server, blocks external hosts.
// Run: node tools/test_energy_demo.mjs   (exit 1 on any failure)
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, "http://x").pathname);
  let f = path.join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end(); }
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, "index.html");
  if (!fs.existsSync(f)) { res.writeHead(404); return res.end("nf"); }
  res.writeHead(200, { "content-type": MIME[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const BASE = `http://127.0.0.1:${server.address().port}/demo/energy-scanner/`;

const browser = await chromium.launch();
const results = [];
async function check(name, fn) {
  try { await fn(); results.push([name, true, ""]); console.log("PASS " + name); }
  catch (e) { results.push([name, false, e.message]); console.log("FAIL " + name + "\n     " + e.message.split("\n").join("\n     ")); }
}
const ok = (c, m) => { if (!c) throw new Error(m); };

async function open(viewport) {
  const ctx = await browser.newContext({ viewport, hasTouch: false });
  await ctx.route("**/*", r => {
    const u = new URL(r.request().url());
    return u.hostname === "127.0.0.1" ? r.continue() : r.abort();
  });
  const page = await ctx.newPage();
  await page.goto(BASE, { waitUntil: "load" });
  await page.waitForSelector("#pad");
  await page.waitForSelector(".demo-bar");
  return { ctx, page };
}

// In-page helpers: effective opaque colour, WCAG contrast.
const HELPERS = `
window.__eff = (el) => {
  const parse = s => { const m = s.match(/rgba?\\(([^)]+)\\)/); if(!m) return [0,0,0,0]; const p = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return [p[0],p[1],p[2],p.length>3?p[3]:1]; };
  let layers = [];
  for (let n = el; n; n = n.parentElement) { const c = parse(getComputedStyle(n).backgroundColor); if (c[3] > 0) layers.push(c); if (c[3] >= 1) break; }
  let base = [255,255,255];
  for (const c of layers.reverse()) base = base.map((b,i)=>c[i]*c[3]+b*(1-c[3]));
  return base;
};
window.__fg = (el, bg) => { const m = getComputedStyle(el).color.match(/rgba?\\(([^)]+)\\)/)[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); const a = m.length>3?m[3]:1; return [0,1,2].map(i=>m[i]*a+bg[i]*(1-a)); };
window.__lum = c => { const f = v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); }; return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]); };
window.__contrast = (el, bgEl) => { const bg = window.__eff(bgEl); const fg = window.__fg(el, bg); const a = window.__lum(fg), b = window.__lum(bg); return (Math.max(a,b)+0.05)/(Math.min(a,b)+0.05); };
`;

for (const vp of [{ width: 390, height: 844 }, { width: 1280, height: 800 }]) {
  const tag = `${vp.width}px`;
  const { ctx, page } = await open(vp);
  await page.evaluate(HELPERS);

  await check(`UX-R1 demo bar "← Portfolio" and "Details" contrast >= 4.5 and >= 48px tall [${tag}]`, async () => {
    const r = await page.evaluate(() => {
      const bar = document.querySelector(".demo-bar");
      const home = bar.querySelector(".demo-bar__home");
      const more = bar.querySelector(".demo-bar__more");
      const tog = bar.querySelector(".demo-bar__toggle");
      return {
        homeText: home.textContent.trim(), homeC: window.__contrast(home, bar), homeH: home.getBoundingClientRect().height,
        moreC: window.__contrast(more, bar), togH: tog.getBoundingClientRect().height,
      };
    });
    const bad = [];
    if (r.homeC < 4.5) bad.push(`Portfolio link contrast ${r.homeC.toFixed(2)} < 4.5`);
    if (r.homeH < 48) bad.push(`Portfolio link height ${r.homeH}px < 48`);
    if (r.moreC < 4.5) bad.push(`Details text contrast ${r.moreC.toFixed(2)} < 4.5`);
    if (r.togH < 48) bad.push(`Details toggle height ${r.togH}px < 48`);
    ok(!bad.length, bad.join("; "));
  });

  await check(`UX-R2 visible "Scan my energy" button under pad, >= 48x48, one click shows reading in 3.5s [${tag}]`, async () => {
    const btn = page.locator("button:not(#pad)", { hasText: /^\s*Scan my energy\s*$/ });
    ok((await btn.count()) === 1, `expected 1 plain button with text "Scan my energy", found ${await btn.count()}`);
    const b = await btn.boundingBox(), p = await page.locator("#pad").boundingBox();
    ok(b.height >= 48 && b.width >= 48, `button is ${b.width}x${b.height}, need >= 48x48`);
    ok(b.y >= p.y + p.height - 1, "button is not under the pad");
    await btn.click();
    await page.waitForFunction(() => !document.getElementById("reading").hidden, null, { timeout: 3500 });
  });

  await check(`UX-R2b press-and-hold on #pad still shows the reading [${tag}]`, async () => {
    const { page: p2, ctx: c2 } = await open(vp);
    try {
      const box = await p2.locator("#pad").boundingBox();
      await p2.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
      await p2.mouse.down();
      await p2.waitForFunction(() => !document.getElementById("reading").hidden, null, { timeout: 5000 });
      await p2.mouse.up();
    } finally { await c2.close(); }
  });

  await check(`UX-R3 releasing the pad early does not show "Too fast" [${tag}]`, async () => {
    const { page: p2, ctx: c2 } = await open(vp);
    try {
      const box = await p2.locator("#pad").boundingBox();
      await p2.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
      await p2.mouse.down();
      await p2.waitForTimeout(300);
      await p2.mouse.up();
      await p2.waitForTimeout(200);
      const txt = await p2.evaluate(() => document.body.innerText);
      ok(!/too fast/i.test(txt), 'page shows "Too fast" after an early release');
    } finally { await c2.close(); }
  });

  await check(`UX-R4 step chips >= 48x48, name font >= 17px, "Bedtime steps" label >= 17px [${tag}]`, async () => {
    const r = await page.evaluate(() => {
      const chips = [...document.querySelectorAll("#steps > *")].map(c => {
        const b = c.getBoundingClientRect();
        return { t: c.textContent.trim(), w: b.width, h: b.height, fs: parseFloat(getComputedStyle(c).fontSize) };
      });
      const lbl = [...document.querySelectorAll(".steplbl span")].find(s => /Bedtime steps/.test(s.textContent));
      return { chips, lblFs: lbl ? parseFloat(getComputedStyle(lbl).fontSize) : 0 };
    });
    const bad = [];
    ok(r.chips.length === 5, `expected 5 step chips, found ${r.chips.length}`);
    for (const c of r.chips) {
      if (c.h < 48 || c.w < 48) bad.push(`chip "${c.t}" is ${c.w.toFixed(0)}x${c.h.toFixed(0)} (< 48)`);
      if (c.fs < 17) bad.push(`chip "${c.t}" font ${c.fs}px < 17`);
    }
    if (r.lblFs < 17) bad.push(`"Bedtime steps" font ${r.lblFs}px < 17`);
    ok(!bad.length, bad.join("; "));
  });

  await check(`UX-R6 Grown-ups controls >= 48px tall once opened; summary says Grown-ups [${tag}]`, async () => {
    const sum = page.locator("details > summary");
    ok(/grown-ups/i.test(await sum.textContent()), "summary text lacks 'Grown-ups'");
    await sum.click();
    const r = await page.evaluate(() => {
      const d = document.querySelector("details");
      const out = [];
      const h = (name, el) => { const b = el.getBoundingClientRect(); out.push({ name, h: b.height, w: b.width }); };
      h("summary", d.querySelector("summary"));
      d.querySelectorAll("input[type=time],input[type=range],button").forEach(el => h(el.id ? "#" + el.id : el.tagName.toLowerCase(), el));
      const cb = d.querySelector("input[type=checkbox]");
      h("checkbox", cb);
      const row = cb.closest("label") || document.querySelector(`label[for="${cb.id}"]`);
      h("checkbox label row", row);
      return out;
    });
    const bad = [];
    for (const c of r) {
      if (c.name === "checkbox") { if (c.h < 24 || c.w < 24) bad.push(`checkbox ${c.w}x${c.h} (< 24)`); }
      else if (c.h < 48) bad.push(`${c.name} height ${c.h.toFixed(0)}px < 48`);
    }
    ok(!bad.length, bad.join("; "));
  });

  await check(`UX-R11 pad aria-label is "Scan my energy" [${tag}]`, async () => {
    const v = await page.locator("#pad").getAttribute("aria-label");
    ok(v === "Scan my energy", `aria-label is "${v}"`);
  });

  await check(`NOSCROLL no horizontal scroll [${tag}]`, async () => {
    const r = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    ok(r.sw <= r.cw, `scrollWidth ${r.sw} > clientWidth ${r.cw}`);
  });

  await ctx.close();
}

await browser.close();
server.close();
const failed = results.filter(r => !r[1]);
console.log(`\n${results.length - failed.length}/${results.length} passed`);
process.exit(failed.length ? 1 : 0);
