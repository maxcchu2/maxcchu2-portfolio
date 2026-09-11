# Max Chu — portfolio

Plain static site. No framework, no build step, no dependencies.
Editorial-minimal: warm parchment, one typeface (General Sans, self-hosted),
one chromatic moment (the hero sphere), hairline structure.

## Run locally
    cd site && python3 -m http.server 8000
    # open http://localhost:8000

## Deploy
Upload the contents of `site/` to Vercel, Netlify, GitHub Pages, or Cloudflare
Pages. No settings, no build command.

## Files
    index.html            home — hero + work list
    about.html            about + contact
    work/<slug>.html       one page per project
    assets/css/style.css   all styles; design tokens are at the top
    assets/js/main.js      ~12 lines: reveal-on-scroll only
    assets/fonts/          General Sans, self-hosted
    assets/img/<slug>/      project images
    build.py               optional generator (see below)

## Editing
Every .html file is plain and editable by hand. If you'd rather edit project
copy in one place, change `PROJECTS` at the top of `build.py` and run
`python3 build.py`. You never have to.

Accent / palette: top of `assets/css/style.css`.
