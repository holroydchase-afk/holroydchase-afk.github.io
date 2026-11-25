/* Shared behavior for the generated pages: the theme menu in the standard header and the demo controls on product
   pages. Same theme choice as the home page (localStorage "theme": light | dark | system, light by default).
   No third-party hosts, no network calls except a same-origin HEAD check that the demo is up. */
(function () {
  var r = document.documentElement;

  /* Theme menu (same markup and behavior as the home page). */
  var b = document.getElementById("tog"), mn = document.getElementById("tmenu");
  if (b && mn) {
    var mq = matchMedia("(prefers-color-scheme: dark)");
    var mark = function () {
      var m = r.dataset.mode;
      mn.querySelectorAll("[data-m]").forEach(function (o) { o.setAttribute("aria-checked", o.dataset.m === m); });
      b.title = "Theme: " + m; b.setAttribute("aria-label", "Theme: " + m);
    };
    var show = function (v) { mn.hidden = !v; b.setAttribute("aria-expanded", v); };
    var apply = function (m) {
      r.dataset.mode = m; r.dataset.theme = m === "system" ? (mq.matches ? "dark" : "light") : m;
      try { localStorage.setItem("theme", m); } catch (e) {}
      mark(); sendTheme();
    };
    b.addEventListener("click", function (e) { e.stopPropagation(); show(mn.hidden); });
    mn.addEventListener("click", function (e) { var o = e.target.closest("[data-m]"); if (o) { apply(o.dataset.m); show(false); b.focus(); } });
    document.addEventListener("click", function (e) { if (!mn.hidden && !mn.contains(e.target)) show(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !mn.hidden) { show(false); b.focus(); } });
    mq.addEventListener("change", function () { if (r.dataset.mode === "system") r.dataset.theme = mq.matches ? "dark" : "light"; });
    mark();
  }

  /* Product pages: one demo frame with three controls (Reload, Full screen, Code). */
  var view = document.querySelector(".view[data-demo]");
  var frame = view && view.querySelector("iframe");
  var wait = view && view.querySelector(".wait"), down = view && view.querySelector(".down");
  function sendTheme() {
    try { if (frame && frame.contentWindow) frame.contentWindow.postMessage({ type: "site-theme", theme: r.dataset.theme }, location.origin); } catch (e) {}
  }
  if (frame) {
    var src = view.dataset.demo;
    /* The page the demo shows is the same site, so the wrapper owns the header: hide the product's own "Demo" bar
       inside the frame (never its working controls). Products can also read ?embed=1 and skip it themselves. */
    var mo;
    var HIDE = '[aria-label="Demo"],[data-testid="demo-bar"],#site-bar,.demo-banner a[href*="chaseholroyd.com"]{display:none!important}';
    function tidy() {
      try {
        var d = frame.contentDocument;
        if (!d || !d.head || d.getElementById("embed-tidy")) return;
        var s = d.createElement("style"); s.id = "embed-tidy"; s.textContent = HIDE; d.head.appendChild(s);
      } catch (e) {}
    }
    function load() {
      wait.hidden = false; down.hidden = true;
      fetch(src, { method: "HEAD", cache: "no-store" }).then(function (res) {
        if (!res.ok) throw 0;
        frame.src = src + (src.indexOf("?") < 0 ? "?" : "&") + "embed=1";
      }).catch(function () { wait.hidden = true; down.hidden = false; });
    }
    frame.addEventListener("load", function () {
      if (!frame.getAttribute("src")) return;
      wait.hidden = true; tidy(); sendTheme();
      try { if (mo) mo.disconnect(); mo = new MutationObserver(tidy); mo.observe(frame.contentDocument.documentElement, { childList: true, subtree: true }); } catch (e) {}
    });
    var rb = view.querySelector("[data-reload]");
    if (rb) rb.addEventListener("click", function () { frame.removeAttribute("src"); load(); });
    load();
  }
})();
