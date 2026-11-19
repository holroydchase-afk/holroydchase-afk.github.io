# stats-proxy

Serves Umami Cloud's tracker script and data endpoint from stats.chaseholroyd.com, so the site never loads from another host (Safari "Reduce Protections"). It is a Vercel project with Root Directory `stats-proxy`; it is not part of the Pages deploy. The destination hosts follow Umami's "bypass ad blockers" docs and were not checked from the cloud session: confirm them at https://docs.umami.is/docs/bypass-ad-blockers if events do not arrive.
