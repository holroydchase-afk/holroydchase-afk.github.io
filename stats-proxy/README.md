# stats-proxy

Serves Umami Cloud from stats.chaseholroyd.com, so the site never loads from another host (Safari "Reduce Protections"). It is a Vercel project with Root Directory `stats-proxy`; it is not part of the Pages deploy.

The rewrite follows Umami's official "Running on Vercel" guide (https://docs.umami.is/docs/guides/running-on-vercel): every path forwards to cloud.umami.is. The page loads `/script.js`, and `data-host-url` makes the tracker post to `/api/send` here, which forwards to `cloud.umami.is/api/send`. Not tested from the cloud session (Umami hosts are blocked there): after setup, open the site and check that a pageview shows in Umami.
