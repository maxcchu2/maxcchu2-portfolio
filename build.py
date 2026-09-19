#!/usr/bin/env python3
"""
build.py — regenerates the static HTML from the content below.
Not required to run the site; every .html file is plain and editable.
Run: python3 build.py   (no dependencies)
"""
import pathlib, time

ROOT = pathlib.Path(__file__).parent
IMG = ROOT / "assets" / "img"
NAME = "Max Chu"
VER = str(int(time.time()))   # cache-buster, refreshed on every build

INTRO = [
    'Hey, I’m <strong>Max Chu</strong>. I’m a designer, but mostly I just like poking at things to '
    'see how they work: a brand’s voice, a campaign’s timing, why one poster makes you stop and the '
    'next one doesn’t.',
    'Most of it lands as campaigns and brand systems. The rest is me getting curious about '
    'something and not stopping in time.',
    'Right now I’m a design fellow at <a href="https://interbrand.com">Interbrand</a> in New York. '
    'Before that, SavoirFaire, and four years at Parsons studying something called Strategic Design '
    'and Management.',
]

EXPERIENCE = [
    ("Since 2026", "Design Fellow", "Interbrand, New York"),
    ("2025", "Intern Graphic Designer", "SavoirFaire"),
    ("2022–2025", "BBA, Strategic Design &amp; Management", "Parsons School of Design"),
    ("2024", "Exchange semester", "University of the Arts London"),
]

PROJECTS = [
    dict(slug="nude-project", title="Made on Concrete", client="Nude Project",
         discipline="Campaign", year="2025", hero=4, modal_skip=[10, 16],
         desc=["Made on Concrete is a conceptual project for Nude Project that celebrates the culture "
               "of street basketball. Instead of the spectacle of professional sport, it focuses on "
               "the raw, social energy of pickup games: friends gathering on the court, and the "
               "playful competition that lives between shots.",
               "The project frames basketball not as a performance but as a mood: a place to hang "
               "out, connect, and share the rhythm of the game."],
         facts=[("Role", "Campaign design, art direction"), ("Scope", "Identity, key art, ticketing, apparel")]),
    dict(slug="arden-jones", title="Age Tape Tour", client="Arden Jones",
         discipline="Campaign", year="2024", hero=1,
         desc=["A conceptual promotional campaign for Arden Jones and the Age Tape Tour, built around "
               "a raw, vintage-inspired aesthetic. Abstract visuals and subtle pops of colour "
               "translate the atmosphere of the music into an expressive promotional identity."],
         facts=[("Role", "Campaign design"), ("Scope", "Tour key art, announce, setlist, social")]),
    dict(slug="scuffers", title="Scuffers Marketing Proposal", client="Scuffers",
         discipline="Strategy", year="2024", hero=1, pair_shots=False,
         desc=["This marketing proposal presents a case for Scuffers’ strategic entry into the U.S. "
               "market. Through a brand audit and analysis of trends in both global and local "
               "contexts, it outlines how Scuffers can anchor its brand identity and strengths to "
               "meet the needs of an American audience.",
               "It also suggests flexible marketing strategies and positioning to ensure long-term "
               "success in a highly competitive landscape."],
         facts=[("Role", "Brand strategy, editorial design"), ("Scope", "Market analysis, positioning, go-to-market")]),
    dict(slug="76x", title="76X", client="76X",
         discipline="Branding", year="2025", hero=3,
         desc=["76X, located at historic Pier 76 along the Hudson River, is a cultural hub that "
               "transforms underutilised space into a premier destination for young artists to "
               "showcase their talents and gain exposure.",
               "The brand symbolises exploration and innovation, emphasising creative artistic "
               "expression. 76X aims to nurture emerging talent and foster community engagement "
               "through arts and culture."],
         facts=[("Role", "Brand identity, art direction"), ("Scope", "Logomark system, posters, type, signage")]),
    dict(slug="kona", title="Kona Coffee Roasters", client="Kona Coffee Roasters",
         discipline="Rebrand", year="2025", hero=1,
         desc=["Conceptual rebranding of New York City’s Kona Coffee Roasters. Established in 2017, "
               "Kona Coffee Roasters is the only coffee shop that brings Hawaii’s premium Kona "
               "coffee to New York City."],
         facts=[("Role", "Rebrand, identity, packaging"), ("Scope", "Wordmark, brand mark, packaging, signage")]),
    dict(slug="proper-company", title="Proper Company", client="Proper Company",
         discipline="Branding", year="2026", hero=4,
         desc=["Proper Company is a conceptual social bar based in Hong Kong, designed for young "
               "creatives seeking connection without the pressures of performative networking.",
               "Positioned between a bar, members’ club, and creative space, it reframes social "
               "interaction as something more intentional, where conversation becomes the primary "
               "medium."],
         facts=[("Role", "Brand identity, art direction"), ("Scope", "Wordmark, monogram, collateral, photography")]),
    dict(slug="akaro", title="Akaro", client="Akaro",
         discipline="Product", year="2025", hero=1,
         desc=["Akaro is a desk-based light and sound object designed to guide your day through "
               "subtle shifts in atmosphere. Inspired by the logic of a traffic signal, it "
               "translates moments of focus, pause, and rest into a system of ambient cues.",
               "With a simple, tactile interface, Akaro lets users move seamlessly between states, "
               "turning light and sound into a quiet, continuous rhythm that supports both "
               "productivity and ease."],
         facts=[("Role", "Industrial design, brand"), ("Scope", "Hardware, UI, packaging, spec drawings")]),
    dict(slug="layr", title="Layr", client="Layr",
         discipline="Interface", year="2026", hero=1, slide_groups=[(4, 5)],
         desc=["LAYR reframes weather as a system of influence, turning environmental data and "
               "context into actionable guidance.",
               "Weather apps are designed to inform, not to guide. While they provide accurate data "
               "(temperature, conditions, forecasts), they fail to translate it into meaningful, "
               "everyday decisions. Users are left to interpret how weather affects what they wear, "
               "how they move, or how they plan their day. Information exists, but usability stays "
               "passive: a gap between environmental data and lived experience.",
               "The design prioritises interpretation over presentation, shifting from “what the "
               "weather is” to “what the weather means.” Through a modular visual system and "
               "simplified decision cues, LAYR helps users navigate their day more intuitively, "
               "aligning data with behaviour, comfort, and routine."],
         facts=[("Role", "Product design, UI"), ("Scope", "Concept, iOS app, widgets, design system")]),
    dict(slug="designing-confidence-through-space", title="Designing Confidence Through Space",
         client="Designing Confidence Through Space", discipline="Research", year="2024", hero=1, pair_shots=False,
         desc=["This study examines how architectural and aesthetic design affects self-confidence "
               "and workplace satisfaction. Using surveys, self-esteem scales, and qualitative "
               "feedback, it compares employees in enhanced versus standard workspaces.",
               "Findings highlight the role of design in shaping well-being and performance, with "
               "implications for architecture, fashion, and workplace practice."],
         facts=[("Role", "Author, research, design"), ("Scope", "Original study, analysis, 9-page paper")]),
]

# ---------------------------------------------------------------------------
def n_images(slug):
    d = IMG / slug
    return len(list(d.glob("*.jpg"))) if d.exists() else 0

HOOPS = """<div class="hoops" id="hoops" hidden>
  <div class="hoops__rig">
    <div class="hoops__board" aria-hidden="true"></div>
    <svg viewBox="0 0 120 96" fill="none" stroke="currentColor"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <defs>
        <linearGradient id="rimGrad" x1="0" y1="0" x2="0" y2="1">
          <stop class="hoops__rim-stop" offset="0%" stop-opacity="0.9"/>
          <stop class="hoops__rim-stop" offset="100%" stop-opacity="0.45"/>
        </linearGradient>
      </defs>
      <ellipse class="hoops__rim" cx="60" cy="54" rx="22" ry="5.5" stroke="url(#rimGrad)" stroke-width="2.4"/>
      <ellipse class="hoops__rim-inner" cx="60" cy="54" rx="17.5" ry="4.2" stroke-width="1"/>
      <path class="hoops__net" stroke-width="1.3" opacity="0.55"
            d="M43 56 L48 88 M51.5 56.5 L54.5 88 M60 57 L60 90 M68.5 56.5 L65.5 88 M77 56 L72 88"/>
      <path class="hoops__net" stroke-width="1.3" opacity="0.55"
            d="M45.5 67 Q60 72.5 74.5 67 M47.5 78 Q60 83 72.5 78"/>
    </svg>
    <span class="hoops__score" id="hoopScore">0</span>
  </div>
  <button class="hoops__ball" id="hoopBall" type="button" aria-label="Basketball, drag to shoot">
    <svg viewBox="0 0 44 44" fill="none" stroke-width="2" stroke-linecap="round" aria-hidden="true">
      <circle class="hoops__seam hoops__seam--edge" cx="22" cy="22" r="20.3"/>
      <path class="hoops__seam" d="M22 1.7v40.6M1.7 22h40.6M7 8c8 6.5 22 6.5 30 0M7 36c8-6.5 22-6.5 30 0"/>
    </svg>
    <span class="hoops__reticle" aria-hidden="true"></span>
  </button>
  <p class="hoops__hint" id="hoopHint">drag and release to shoot</p>
  <svg class="hoops__aim" id="hoopAim" aria-hidden="true"><line x1="0" y1="0" x2="0" y2="0"/></svg>
</div>"""

BUNNY = """<div class="bunny" id="bunny" aria-hidden="true">
  <svg viewBox="0 0 120 150" fill="none" stroke="currentColor" stroke-width="1.7"
       stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="43" cy="41" rx="11" ry="19" transform="rotate(-16 43 41)"/>
    <ellipse cx="77" cy="41" rx="11" ry="19" transform="rotate(16 77 41)"/>
    <ellipse class="bunny__inner" cx="43" cy="42" rx="5.2" ry="12" transform="rotate(-16 43 42)" stroke-width="1.3"/>
    <ellipse class="bunny__inner" cx="77" cy="42" rx="5.2" ry="12" transform="rotate(16 77 42)" stroke-width="1.3"/>
    <circle cx="60" cy="104" r="37"/>
    <circle cx="46" cy="100" r="3.6" fill="currentColor" stroke="none"/>
    <circle cx="74" cy="100" r="3.6" fill="currentColor" stroke="none"/>
    <circle class="bunny__blush" cx="38" cy="110" r="4.6" stroke="none"/>
    <circle class="bunny__blush" cx="82" cy="110" r="4.6" stroke="none"/>
    <circle class="bunny__nose" cx="60" cy="111" r="3.4" stroke="none"/>
    <path class="bunny__scarf" d="M29 131c10 9 24 13 31 13s21-4 31-13" stroke-width="7"/>
    <path class="bunny__scarf" d="M57 141l4 12" stroke-width="6"/>
    <ellipse cx="42" cy="146" rx="12.5" ry="8"/>
    <ellipse cx="78" cy="146" rx="12.5" ry="8"/>
  </svg>
</div>"""

ZOOM = """<div class="zoom" id="zoom" role="dialog" aria-modal="true" aria-label="Enlarged image" hidden>
    <div class="zoom__scrim" data-close></div>
    <button class="zoom__nav zoom__prev" type="button" aria-label="Previous image">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>
    </button>
    <button class="zoom__nav zoom__next" type="button" aria-label="Next image">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>
    </button>
    <figure class="zoom__fig"><img alt="" class="shown"><img alt=""></figure>
  </div>"""

THEME_INIT = ("<script>(function(){try{var t=localStorage.getItem('theme');"
              "if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);"
              "}catch(e){}})();</script>")

I_MODE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
          '<path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.6 6.6 0 0 0 9.8 9.8Z"/></svg>')
I_STAR = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<path d="M12 1.5 14.6 9.4 22.5 12 14.6 14.6 12 22.5 9.4 14.6 1.5 12 9.4 9.4Z"/></svg>')
I_PREV = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>')
I_NEXT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
          'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>')

def head(title, desc, prefix):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<meta name="color-scheme" content="light dark">
{THEME_INIT}
<link rel="preload" as="font" type="font/woff2" crossorigin href="{prefix}assets/fonts/PPNeueMontreal-Book.woff2">
<link rel="stylesheet" href="{prefix}assets/css/style.css?v={VER}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def top():
    return (f'<div class="top">\n'
            f'    <button type="button" class="mark" aria-label="Play basketball" aria-expanded="false"></button>\n'
            f'    <div class="tools">\n'
            f'      <button type="button" data-act="special" aria-pressed="false" aria-label="Special mode">{I_STAR}</button>\n'
            f'      <button type="button" data-act="mode" aria-label="Switch theme">{I_MODE}</button>\n'
            f'    </div>\n'
            f'  </div>')

def scripts(prefix):
    return (f'<script src="{prefix}assets/js/lenis.min.js" defer></script>\n'
            f'<script src="{prefix}assets/js/main.js?v={VER}" defer></script>\n</body>\n</html>\n')

# ---------------------------------------------------------------------------
def build_index():
    # the first slide is the first thing anyone sees: load it eagerly, the rest lazily
    def load_attr(n):
        return 'fetchpriority="high"' if n == 0 else 'loading="lazy"'
    slides = "".join(
        f'<a class="slide" href="work/{p["slug"]}.html" data-project="{p["slug"]}" aria-label="Open {p["title"]}">'
        f'<img {load_attr(n)} src="assets/img/{p["slug"]}/{p["hero"]:02d}.jpg" '
        f'alt="{p["client"]} — {p["title"]}"></a>'
        for n, p in enumerate(PROJECTS)
    )
    wrows = "".join(
        f'    <a class="wrow" href="work/{p["slug"]}.html" data-project="{p["slug"]}" '
        f'data-img="assets/img/{p["slug"]}/{p["hero"]:02d}.jpg">'
        f'<span class="wrow__lead"><span class="wrow__title">{p["title"]}</span>'
        f'<span class="wrow__yr">{p["year"]}</span></span>'
        f'<span class="wrow__cat">{p["discipline"]}</span></a>\n'
        for p in sorted(PROJECTS, key=lambda x: x["year"], reverse=True)
    )
    import json
    # the modal opens from the filmstrip, so step prev/next in that same
    # curated order — not the year-sorted order the list view/case pages use
    ordered_slugs = [p["slug"] for p in PROJECTS]
    data = {p["slug"]: {"title": p["title"], "cat": p["discipline"], "year": p["year"],
                        "desc": p["desc"], "n": n_images(p["slug"]),
                        "skip": p.get("modal_skip", [])} for p in PROJECTS}
    data_js = ("<script>window.MC_PROJECTS=" + json.dumps(data, ensure_ascii=False) + ";"
               "window.MC_ORDER=" + json.dumps(ordered_slugs) + ";</script>")
    I_GRID = ('<svg viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">'
              '<rect x="2" y="2" width="7" height="7" rx="1"/><rect x="11" y="2" width="7" height="7" rx="1"/>'
              '<rect x="2" y="11" width="7" height="7" rx="1"/><rect x="11" y="11" width="7" height="7" rx="1"/></svg>')
    I_LIST = ('<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" '
              'stroke-linecap="round" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14"/></svg>')
    modal = """<div class="modal" id="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title" hidden>
    <div class="modal__scrim" data-close></div>
    <button class="modal__close" type="button" aria-label="Close" data-close>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <button class="modal__nav modal__prev" type="button" aria-label="Previous project">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>
    </button>
    <button class="modal__nav modal__next" type="button" aria-label="Next project">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>
    </button>
    <div class="modal__card" data-lenis-prevent><div class="modal__body"></div></div>
  </div>
  """ + ZOOM
    rows = "".join(
        f'      <div class="row"><time>{w}</time><div><b>{r}</b> <span>{o}</span></div></div>\n'
        for w, r, o in EXPERIENCE
    )
    intro = "\n    ".join(f"<p>{line}</p>" for line in INTRO)

    html = head(f"{NAME} · campaign & brand design",
                f"{NAME}. Campaigns and brands, made in New York.", "")
    html += f"""<main id="main" class="sheet">
  <div class="bay">
  {top()}
  <h1 class="sr-only">{NAME}, campaign and brand designer</h1>

  <div class="intro fade">
    {intro}
  </div>

  <section class="work fade" data-view="grid">
    <div class="work__bar">
      <h2 class="eyebrow">selected work</h2>
      <div class="viewtoggle" role="group" aria-label="View">
        <button type="button" data-view="grid" aria-pressed="true" aria-label="Image view">{I_GRID}</button>
        <button type="button" data-view="list" aria-pressed="false" aria-label="List view">{I_LIST}</button>
      </div>
    </div>
    <div class="rail" tabindex="0" role="region" aria-label="Selected work" data-lenis-prevent>
      {slides}
    </div>
    <div class="worklist">
{wrows}    </div>
  </section>

  <section class="exp fade">
    <h2 class="eyebrow">experiences</h2>
{rows}  </section>

  <footer class="foot">
    <span>{NAME}</span>
    <a href="mailto:MaxCChu2@gmail.com">MaxCChu2@gmail.com</a>
    <a href="https://www.instagram.com/maxcchu2/" target="_blank" rel="noopener">Instagram</a>
    <a href="https://www.linkedin.com/in/maxcchu2/" target="_blank" rel="noopener">LinkedIn</a>
  </footer>
  </div>
</main>
<div class="peek" aria-hidden="true"><img alt=""><img alt=""></div>
<div class="ambient" aria-hidden="true"></div>
{HOOPS}
{BUNNY}
{modal}
{data_js}
"""
    html += scripts("")
    (ROOT / "index.html").write_text(html)

def build_project(i, p):
    prefix = "../"
    ordered = sorted(PROJECTS, key=lambda x: x["year"], reverse=True)
    pos = ordered.index(p)
    prev = ordered[pos - 1] if pos > 0 else None
    nxt = ordered[pos + 1] if pos + 1 < len(ordered) else None

    facts = ""
    if p["title"] != p["client"]:
        facts += f"<dt>Client</dt><dd>{p['client']}</dd>"
    facts += "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in p["facts"])
    facts += f"<dt>Year</dt><dd>{p['year']}</dd><dt>Discipline</dt><dd>{p['discipline']}</dd>"

    n = n_images(p["slug"])
    hero_img = p["hero"]
    extra = [k for k in range(1, n + 1) if k != hero_img]

    def img_tag(k, cls=""):
        alt = p["title"] if k == hero_img else f'{p["title"]}, detail'
        c = f' class="{cls}"' if cls else ""
        load = 'fetchpriority="high"' if k == hero_img else 'loading="lazy"'
        return f'<img {load} src="{prefix}assets/img/{p["slug"]}/{k:02d}.jpg" alt="{alt}"{c}>'

    # solo/pair rhythm for the shots below the hero — not every row shares,
    # so a paired row reads as a deliberate choice rather than a default.
    # a project can also mark a fixed run of images as "slide_groups" —
    # near-identical shots that auto-crossfade in one slot instead of
    # each getting their own row.
    ROW_PATTERN = [1, 2, 1, 2, 2, 1, 2, 1]
    slide_groups = [list(g) for g in p.get("slide_groups", [])]
    slide_starts = {
        idx: g for idx in range(len(extra)) for g in slide_groups
        if extra[idx:idx + len(g)] == g
    }

    if p.get("pair_shots", True):
        rows = [("single", [hero_img])]
        pos, step = 0, 0
        while pos < len(extra):
            g = slide_starts.get(pos)
            if g:
                rows.append(("slide", g))
                pos += len(g)
                continue
            size = ROW_PATTERN[step % len(ROW_PATTERN)]
            for k in range(1, size):
                if (pos + k) in slide_starts:
                    size = k  # don't let a pair swallow an upcoming slide group
                    break
            size = min(size, len(extra) - pos)
            rows.append(("row" if size > 1 else "single", extra[pos:pos + size]))
            pos += size
            step += 1
    else:
        rows = [("single", [k]) for k in [hero_img] + extra]

    def render_row(kind, imgs):
        if kind == "single":
            return img_tag(imgs[0])
        if kind == "row":
            return f'<div class="case__row">{"".join(img_tag(k) for k in imgs)}</div>'
        slide_imgs = "".join(img_tag(k, "shown" if idx == 0 else "") for idx, k in enumerate(imgs))
        return (f'<div class="case__slide" data-slide tabindex="0" role="group" '
                f'aria-label="Screens that cycle on their own; hover or focus to pause">{slide_imgs}</div>')

    shots = "".join(render_row(kind, imgs) for kind, imgs in rows)

    prev_a = (f'<a class="case__step case__step--prev" href="{prev["slug"]}.html" rel="prev" '
              f'aria-label="Previous project, {prev["title"]}">{I_PREV}<span>{prev["title"]}</span></a>'
              if prev else '<span></span>')
    nxt_a = (f'<a class="case__step case__step--next" href="{nxt["slug"]}.html" rel="next" '
             f'aria-label="Next project, {nxt["title"]}"><span>{nxt["title"]}</span>{I_NEXT}</a>'
             if nxt else f'<a class="case__step case__step--next" href="{prefix}index.html">'
             f'<span>Index</span>{I_NEXT}</a>')
    nxt_top = (f'<a class="tools__next" href="{nxt["slug"]}.html" rel="next" '
               f'aria-label="Next project, {nxt["title"]}">{I_NEXT}</a>'
               if nxt else f'<a class="tools__next" href="{prefix}index.html" '
               f'aria-label="Back to index">{I_NEXT}</a>')

    desc_txt = " ".join(p["desc"])
    desc_html = "".join(f'<p>{para}</p>' for para in p["desc"])
    html = head(f"{p['title']} · {NAME}", desc_txt[:150], prefix)
    html += f"""<main id="main" class="sheet sheet--case">
  <div class="bay">
    <div class="top">
      <a class="mark" href="{prefix}index.html" aria-label="Back to {NAME}"></a>
      <div class="tools">
        <button type="button" data-act="special" aria-pressed="false" aria-label="Special mode">{I_STAR}</button>
        <button type="button" data-act="mode" aria-label="Switch theme">{I_MODE}</button>
        {nxt_top}
      </div>
    </div>
    <article class="case__body">
      <h1>{p['title']}</h1>
      <p class="case__meta">{p['discipline']}, {p['year']}</p>
      <div class="case__text">{desc_html}</div>
      <dl class="case__facts">{facts}</dl>
      <div class="case__shots">{shots}</div>
      <nav class="case__nav">{prev_a}{nxt_a}</nav>
    </article>
  </div>
  {ZOOM}
</main>
"""
    html += scripts(prefix)
    (ROOT / "work" / f"{p['slug']}.html").write_text(html)

if __name__ == "__main__":
    (ROOT / "work").mkdir(exist_ok=True)
    build_index()
    for i, p in enumerate(PROJECTS):
        build_project(i, p)
    print(f"built index + {len(PROJECTS)} project pages")
