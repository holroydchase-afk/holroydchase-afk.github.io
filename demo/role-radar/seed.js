/* Sample data for the Role Radar demo. Every company, person and job here is made up,
 * for a made-up job seeker ("Sam"). Dates are relative to today so the demo never goes stale. */
(function () {
  const day = 864e5;
  const iso = (n) => new Date(Date.now() + n * day).toISOString();
  const date = (n) => iso(n).slice(0, 10);
  const url = "https://example.com/jobs";
  // Public demo shows the radar only. A link ending in ?full also shows the resume
  // intake and recruiter tracker, for people Chase shares it with (WEB-M3.4).
  const FULL = new URLSearchParams(location.search).has("full");

  const job = (id, o) => {
    const d = Object.assign({ ats: "greenhouse", tags: [], source: "board",
      firstSeen: iso(-1), statusAt: iso(-1), url: url + "/" + id }, o);
    d.postedAt = d.postedAt || new Date(Date.parse(d.firstSeen) - day).toISOString().slice(0, 10);
    return [id, d];
  };

  const jobs = Object.fromEntries([
    job("sunfield-senior-pm-storage", { company: "Sunfield Energy", title: "Senior Product Manager, Home Storage", status: "new",
      lane: "Geospatial / clean energy", sector: "Solar, storage & distributed energy", fit: "strong", score: 90,
      comp: "$185K–$215K", location: "Remote, US",
      fitNote: "Battery and solar install workflows are the core of Sam's last two roles. Gap: no hardware launch experience." }),
    job("orbitline-staff-pm-imagery", { company: "Orbitline Maps", title: "Staff Product Manager, Imagery Platform", status: "new",
      lane: "Geospatial / clean energy", sector: "Space & geospatial", fit: "maybe", score: 60, ats: "ashby",
      comp: "$190K–$230K", location: "Remote, US",
      fitNote: "Platform PM for a satellite imagery API. Strong on platform work; light on remote-sensing domain." }),
    job("northwind-sr-pm-checkout", { company: "Northwind Pay", title: "Senior Product Manager, Checkout", status: "viewed",
      lane: "Checkout", sector: "General fintech & payments", fit: "strong", score: 60, ats: "lever",
      comp: "$175K–$205K", location: "Remote, US", viewedAt: iso(-0.5), source: "ziprecruiter",
      fitNote: "Checkout conversion and payment methods; matches the pricing and payments work." }),
    job("canopy-pm-carbon", { company: "Canopy Ledger", title: "Principal Product Manager, Carbon Accounting", status: "saved",
      lane: "AI platform", sector: "Climate & sustainability software", fit: "maybe", score: 75, ats: "ashby",
      comp: "$200K–$240K", location: "Remote, US", statusAt: iso(-3), firstSeen: iso(-4),
      fitNote: "Emissions data platform with an AI assistant. Principal scope is a stretch, but the domain is a priority.",
      nextStep: "Ask Priya for a referral before applying" }),
    job("trailhead-sr-pm-app", { company: "Trailhead Outfitters", title: "Senior Product Manager, Member App", status: "applying",
      lane: "Other", sector: "Adventure & outdoor brands", fit: "strong", score: 75,
      comp: "$170K–$195K", location: "Remote, US", statusAt: iso(-1), firstSeen: iso(-5),
      fitNote: "Loyalty and mobile app for an outdoor co-op. Good culture signals in the posting.",
      resumeName: FULL ? "Sam – Trailhead – tailored" : "", nextStep: "Finish the two short-answer questions" }),
    job("cumulus-sr-pm-agents", { company: "Cumulus AI", title: "Senior Product Manager, Agent Workflows", status: "applied",
      lane: "AI platform", sector: "AI tooling & automation", fit: "strong", score: 60,
      comp: "$180K–$210K", location: "Remote, US", appliedAt: iso(-8), statusAt: iso(-8), firstSeen: iso(-10),
      followUpDue: date(-1), fitNote: "Agent orchestration for ops teams. Direct match to recent AI workflow projects.",
      resumeName: FULL ? "Sam – Cumulus – tailored" : "", nextStep: "Follow up with the recruiter" }),
    job("brightgrid-pm-vpp", { company: "BrightGrid", title: "Senior Product Manager, Virtual Power Plant", status: "interviewing",
      lane: "Geospatial / clean energy", sector: "Solar, storage & distributed energy", fit: "strong", score: 90,
      comp: "$195K–$225K", location: "Remote, US", appliedAt: iso(-15), statusAt: iso(-2), firstSeen: iso(-18),
      referral: "Jordan Lee (former teammate)", resumeName: FULL ? "Sam – BrightGrid – tailored" : "",
      fitNote: "Utility programs and home batteries. Best fit on the board.", nextStep: "Panel interview: prep the pricing case study",
      followUpDue: date(2) }),
    job("ledgerly-pm-billing", { company: "Ledgerly", title: "Product Manager, Billing", status: "skipped",
      lane: "Pricing & payments", sector: "General fintech & payments", fit: "stretch", score: 20,
      comp: "$140K–$160K", location: "Hybrid, New York", statusAt: iso(-6), firstSeen: iso(-7),
      skipReason: "Not remote", fitNote: "Hybrid three days a week in New York." }),
    job("harbor-sr-pm-claims", { company: "Harbor Mutual", title: "Senior Product Manager, Claims Automation", status: "rejected",
      lane: "Ops & processing", sector: "Large stable companies", fit: "strong", score: 50,
      comp: "$165K–$190K", location: "Remote, US", appliedAt: iso(-25), statusAt: iso(-9), firstSeen: iso(-28),
      fitNote: "Claims workflow automation at a large insurer." }),
  ]);

  const co = (name, slug, ats, industry, status, via) => ["" + ats + "-" + slug,
    { name, slug, ats, industry, status, via, lastChecked: status === "active" ? iso(-0.2) : undefined }];
  const companies = Object.fromEntries([
    co("Sunfield Energy", "sunfield", "greenhouse", "home solar and storage", "active", "seed"),
    co("BrightGrid", "brightgrid", "greenhouse", "virtual power plants", "active", "seed"),
    co("Canopy Ledger", "canopyledger", "ashby", "carbon accounting", "active", "scan"),
    co("Orbitline Maps", "orbitline", "ashby", "satellite imagery", "active", "seed"),
    co("Trailhead Outfitters", "trailhead", "greenhouse", "outdoor retail", "active", "seed"),
    co("Northwind Pay", "northwindpay", "lever", "payments", "active", "scan"),
    co("Cumulus AI", "cumulus", "greenhouse", "AI automation", "active", "seed"),
    co("Riverstone Bank", "riverstone", "lever", "banking", "unverified", "scan"),
    co("QuickCash Now", "quickcash", "lever", "payday lending", "vetoed", "seed"),
  ].map(([id, d]) => [id, JSON.parse(JSON.stringify(d))]));

  // The recruiter tracker only shows in the full view (WEB-M3.4).
  const recruiters = !FULL ? {} : {
    "priya-shah-canopy-ledger": { name: "Priya Shah", company: "Canopy Ledger", title: "Product lead", type: "referral",
      roles: "Principal PM, Carbon Accounting", sector: "Climate & sustainability software", lastContact: date(-12),
      lastNote: "Met at a climate meetup. Offered to pass a resume along.", nextStep: "Ask for a referral to the principal role",
      nextStepDue: date(0), source: "manual" },
    "marcus-webb-cumulus-ai": { name: "Marcus Webb", company: "Cumulus AI", title: "Technical recruiter", type: "in-house",
      roles: "Senior PM, Agent Workflows", sector: "AI tooling & automation", lastContact: date(-8),
      lastNote: "Confirmed the application came through.", nextStep: "Send a short follow-up note", nextStepDue: date(-1), source: "email" },
    "dana-ortiz-brightgrid": { name: "Dana Ortiz", company: "BrightGrid", title: "Recruiting partner", type: "in-house",
      roles: "Senior PM, Virtual Power Plant", sector: "Solar, storage & distributed energy", lastContact: date(-2),
      lastNote: "Scheduled the panel. Four interviewers, 3 hours.", nextStep: "Send thank-you notes after the panel",
      nextStepDue: date(3), source: "email" },
  };

  const spec = `# ─────────────────────────────────────────────────────────────
#  Role Radar · search criteria  (sample seeker: Sam)
#  The weekday scan reads this before every run.
#  Score 0–100: sector (weight × 15) + fit (strong 35 · maybe 20 · stretch 5)
#  + culture (+10 good, −10 per red flag) + comp (+10 if the top of the range ≥ stretch target)
# ─────────────────────────────────────────────────────────────

version: 1
owner: Sam (sample)

role:
  track: individual_contributor
  levels: [senior, staff, principal]
  title_include: [Senior Product Manager, Staff Product Manager, Principal Product Manager, Product Manager]
  title_exclude: [Director, VP, Head of, Associate, Intern, Engineer, Designer]

work:
  remote: fully_remote_us
  hybrid_ok_near: [Denver, CO]
  reject: [hybrid, in_office, relocation]

comp:
  base_floor_usd: 160000
  priority_sector_floor_usd: 150000
  stretch_target_usd: 200000

culture:
  good_signals: [async, four-day week, sustainable pace, remote-first]
  red_flags: [work hard play hard, 60+ hours, always on]

sectors:
  - id: solar_energy
    label: Solar, storage & distributed energy
    weight: 3
    keywords: [solar, storage, battery, grid, virtual power plant, EV charging]
    examples: [Sunfield Energy, BrightGrid]
  - id: climate_tech
    label: Climate & sustainability software
    weight: 3
    keywords: [climate, carbon, emissions, sustainability]
    examples: [Canopy Ledger]
  - id: space_geo
    label: Space & geospatial
    weight: 2
    keywords: [satellite, geospatial, mapping, imagery]
    examples: [Orbitline Maps]
  - id: outdoor_brands
    label: Adventure & outdoor brands
    weight: 2
    examples: [Trailhead Outfitters]
  - id: big_corp
    label: Large stable companies
    weight: 1
    examples: [Harbor Mutual]
  - id: fintech
    label: General fintech & payments
    weight: 1
    examples: [Northwind Pay, Ledgerly]
  - id: ai_tooling
    label: AI tooling & automation
    weight: 1
    examples: [Cumulus AI]

default_sector_weight: 1

hard_exclude:
  companies: [QuickCash Now]
  business_models: [payday or cash-advance apps]

values_penalty: [fossil fuel extraction, gambling or sports betting]

scoring:
  min_score_to_add: 45
  digest_max_items: 8
  per_sector_cap: { fintech: 2, ai_tooling: 2 }
`;

  const meta = {
    config: {
      owner: "Sam (sample)", followUpBusinessDays: 5, staleAppliedDays: 14, staleSavedDays: 7,
      lanes: ["Pricing & payments", "Checkout", "Ops & processing", "AI platform", "Geospatial / clean energy", "Other"],
      skipReasons: ["Comp too low", "Not remote", "Wrong level", "Wrong domain", "Culture", "Other"],
      intakeCommand: "/job-intake", intakeWhere: "a new Claude chat",
      intakeInstructions: "Screen the posting, map its requirements to my experience, and draft a tailored resume. Then set this role to \"applying\" in Role Radar.",
    },
    criteria: { spec, updatedAt: iso(-2) },
    scan: { lastRun: iso(-0.3), boardsChecked: 7, newMatches: 2,
      note: "Weekday run (sample). 7 company boards read, plus ZipRecruiter and job-alert email. 2 new matches: Sunfield Energy (90) and Orbitline Maps (60). Ledgerly's new billing role was left out as hybrid." },
    filters: { notes: "Superseded by Criteria. Kept as a fallback." },
  };

  window.DEMO_FULL = FULL;
  window.DEMO = { back: "../../role-radar.html", backLabel: "← Back to Role Radar", key: FULL ? "role-radar-full" : "role-radar-v2", seed: { jobs, companies, recruiters, meta } };
})();
