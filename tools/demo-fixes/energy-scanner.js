// Demo-only: a one-tap Scan button next to the press-and-hold pad (UX-R2).
$("scanBtn").addEventListener("click",()=>{
  if(holding)return;
  holding=true;pad.classList.remove("done");pad.classList.add("scanning");
  $("hint").textContent="Scanning…";$("reading").hidden=true;
  const t=performance.now();
  (function go(){const p=Math.min(1,(performance.now()-t)/900);prog.style.strokeDashoffset=C*(1-p);if(p<1)requestAnimationFrame(go);else finish()})();
});
