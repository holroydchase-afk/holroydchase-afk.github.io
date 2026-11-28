/* The standard site header on every demo page (WEB-M14). One script tag per demo:
     <script src="/assets/demo-bar.js" defer></script>
   It draws the same header as every page on chaseholroyd.com (name, Case studies, Building, Agents, Resume, Contact, theme).
   Inside the portfolio's own demo frame (a product page) it does nothing, because the frame's page already has the header.
   Add data-page="white" to also turn the page behind the demo white (light theme only). Same theme choice as the site
   (localStorage "theme"), self-hosted font, no third-party hosts. Never touches the demo's own screens.
   Hearth demo only (path /hearth/): a centered "Demo" chip that asks the demo to toggle its bottom drawer. Click fires
   window event "hearth-demo-drawer"; the demo answers with documentElement.dataset.hearthDemoDrawer = open|closed and
   a "hearth-demo-drawer-state" CustomEvent ({detail:{open}}) on window, which keeps aria-expanded in step. */
(function () {
  if (window.__demoBar) return;
  window.__demoBar = 1;
  try { if (window.top !== window.self) return; } catch (e) { return; }
  if (/[?&]embed=1\b/.test(location.search)) return;
  var me = document.currentScript, white = me && me.getAttribute("data-page") === "white";
  var mode = "light";
  try {
    var m = localStorage.getItem("theme"), q = new URLSearchParams(location.search).get("theme");
    mode = q === "dark" || q === "light" || q === "system" ? q : (m === "dark" || m === "light" || m === "system" ? m : "light");
  } catch (e) {}
  var mq = matchMedia("(prefers-color-scheme: dark)");
  function theme() { return mode === "system" ? (mq.matches ? "dark" : "light") : mode; }

  var SUN = '<svg class="i-sun" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.2M12 19.8V22M2 12h2.2M19.8 12H22M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6"/></g></svg>';
  var MOON = '<svg class="i-moon" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><path d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5a8.5 8.5 0 1 0 10.7 10.7z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>';
  var SYS = '<svg class="i-sys" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></g></svg>';
  var VARS = {
    light: "--bg:#fff;--surface:#fff;--ink:#111;--muted:#4A4A48;--line:#E4E4E0;--band:#F6F6F4;--accent:#0B7A4B",
    dark: "--bg:#0A0A0A;--surface:#141414;--ink:#fff;--muted:#C4C4C0;--line:#2E2E2C;--band:#141414;--accent:#3DDC97"
  };

  function build() {
    if (!document.body) return setTimeout(build, 20);
    var html = document.documentElement;
    html.dataset.mode = mode; html.dataset.theme = theme();
    if (white && theme() === "light") html.className += " sb-white";
    var st = document.createElement("link");
    st.rel = "stylesheet"; st.href = "/assets/header.css"; document.head.appendChild(st);
    var st2 = document.createElement("link");
    st2.rel = "stylesheet"; st2.href = "/assets/demo-bar.css"; document.head.appendChild(st2);
    var f = document.createElement("link");
    f.rel = "stylesheet"; f.href = "/assets/fonts.css"; document.head.appendChild(f);
    var b = document.createElement("header");
    b.id = "site-bar"; b.className = "site";
    function paint() { b.setAttribute("style", VARS[theme()] + ";color-scheme:" + theme()); html.dataset.theme = theme(); }
    paint();
    b.innerHTML =
      '<div class="w"><a class="dock" href="/" aria-label="Chase Holroyd, home"><span class="dk-i"><img src="/assets/chase-400.webp" alt="" width="40" height="40"></span><b>Chase Holroyd</b></a>' +
      '<div class="hr"><nav aria-label="Main"><a href="/#cases">Case studies</a><a class="keep" href="/building.html">Building</a><a href="/agents.html">Agents</a><a href="/resume.html">Resume</a><a class="keep" href="/#contact">Contact</a></nav>' +
      '<div class="thw"><button class="thm" id="sb-tog" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="sb-menu" aria-label="Theme" title="Theme">' + SUN + MOON + SYS + '</button>' +
      '<div class="tmenu" id="sb-menu" hidden role="group" aria-label="Theme"><button type="button" data-m="light" role="menuitemradio" aria-checked="false">Light</button><button type="button" data-m="dark" role="menuitemradio" aria-checked="false">Dark</button><button type="button" data-m="system" role="menuitemradio" aria-checked="false">System</button></div></div></div></div>';
    document.body.insertBefore(b, document.body.firstChild);
    if (/^\/hearth(\/|$)/i.test(location.pathname)) {
      var chip = document.createElement("button");
      chip.type = "button"; chip.className = "demo-chip";
      chip.setAttribute("aria-label", "Demo info"); chip.setAttribute("aria-haspopup", "dialog");
      chip.setAttribute("aria-expanded", html.dataset.hearthDemoDrawer === "open" ? "true" : "false");
      chip.innerHTML = '<span>Demo</span><svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true" focusable="false"><path d="M2 8l4-4 4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      chip.addEventListener("click", function () { window.dispatchEvent(new Event("hearth-demo-drawer")); });
      window.addEventListener("hearth-demo-drawer-state", function (e) { chip.setAttribute("aria-expanded", e && e.detail && e.detail.open ? "true" : "false"); });
      b.querySelector(".w").insertBefore(chip, b.querySelector(".hr"));
    }
    var tog = b.querySelector("#sb-tog"), mn = b.querySelector("#sb-menu");
    function mark() { mn.querySelectorAll("[data-m]").forEach(function (o) { o.setAttribute("aria-checked", o.dataset.m === mode); }); tog.title = "Theme: " + mode; tog.setAttribute("aria-label", "Theme: " + mode); }
    function show(v) { mn.hidden = !v; tog.setAttribute("aria-expanded", v); }
    tog.addEventListener("click", function (e) { e.stopPropagation(); show(mn.hidden); });
    mn.addEventListener("click", function (e) {
      var o = e.target.closest("[data-m]"); if (!o) return;
      mode = o.dataset.m; html.dataset.mode = mode; try { localStorage.setItem("theme", mode); } catch (x) {}
      paint(); mark(); show(false); tog.focus();
    });
    document.addEventListener("click", function (e) { if (!mn.hidden && !mn.contains(e.target)) show(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !mn.hidden) { show(false); tog.focus(); } });
    mark();
  }
  build();
})();
