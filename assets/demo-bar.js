/* Shared site header for every demo on chaseholroyd.com (portfolio demos and each product's own demo).
   One script tag per demo: <script src="/assets/demo-bar.js" defer></script>
   Add data-page="white" to also turn the page behind the demo white (light theme only).
   Same white / ink / emerald look as the home page, same theme choice (localStorage "theme"), self-hosted font,
   no third-party hosts. Adds a way back to the site; never touches the demo's own screens. */
(function () {
  if (window.__demoBar) return;
  window.__demoBar = 1;
  var path = location.pathname.replace(/\/+$/, "");
  var seg = path.split("/").filter(Boolean);
  if (seg[0] === "demo" && seg[1]) seg = seg.slice(1);
  var NAMES = { hearth: "Hearth", ccwatts: "ccwatts", "role-radar": "Role Radar", charlie: "Charlie", "crew-clock": "Crew Clock",
    "energy-scanner": "Energy Scanner", "font-tester": "Font tester", "fruit-palettes": "Fruit palettes", "share-start-tester": "Share start tester" };
  var CASE = { hearth: "family-photos.html", ccwatts: "ccwatts.html", "role-radar": "role-radar.html", charlie: "charlie.html",
    "crew-clock": "crew-clock.html", "energy-scanner": "energy-scanner.html" };
  var me = document.currentScript, white = me && me.getAttribute("data-page") === "white";
  var key = seg[0] || "";
  var label = NAMES[key] || "";

  var dark = false;
  try {
    var m = localStorage.getItem("theme"), q = new URLSearchParams(location.search).get("theme");
    m = q === "dark" || q === "light" || q === "system" ? q : (m === "dark" || m === "light" || m === "system" ? m : "light");
    dark = m === "dark" || (m === "system" && matchMedia("(prefers-color-scheme: dark)").matches);
  } catch (e) {}


  function build() {
    if (!document.body) return setTimeout(build, 20);
    if (white && !dark) document.documentElement.className += " sb-white";
    var st = document.createElement("link");
    st.rel = "stylesheet";
    st.href = "/assets/demo-bar.css";
    document.head.appendChild(st);
    var b = document.createElement("header");
    b.id = "site-bar";
    if (dark) b.className = "dk";
    var cs = CASE[key] ? '<a class="cs hide-s" href="/' + CASE[key] + '">Case study</a>' : "";
    b.innerHTML =
      '<a class="nm" href="/" aria-label="Chase Holroyd, back to the portfolio"><i aria-hidden="true">&larr;</i> Chase Holroyd</a>' +
      '<nav aria-label="Site" style="display:contents"><a class="hide-s" href="/building.html">Building</a>' +
      '<a class="hide-s" href="/agents.html">Agents</a></nav>' +
      '<span class="sp"></span>' + (label ? '<span class="lb">' + label + " demo</span>" : "") + cs;
    document.body.insertBefore(b, document.body.firstChild);
  }
  build();
})();
