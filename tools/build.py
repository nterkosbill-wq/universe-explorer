"""Static site builder for Universe Explorer — renders dist/ from content modules."""

ICON_PLANET = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="6.4"/><ellipse cx="12" cy="12" rx="10.4" ry="3.6" transform="rotate(-24 12 12)"/></svg>'
ICON_STAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 3l1.9 5.4L19.3 10l-5.4 1.9L12 17.3l-1.9-5.4L4.7 10l5.4-1.6z"/><path d="M18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/></svg>'
ICON_GALAXY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 12c2.8-2.2 6.4-1.6 7 1.2.5 2.6-2 4.6-4.6 4.1-3.4-.7-5-4.4-3.4-7.4 1.8-3.4 6.2-4 8.3-1.1"/><circle cx="12" cy="12" r="1.4"/></svg>'
ICON_HOLE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="3.2"/><path d="M12 3.2c3.4 1.6 5.2 4.7 5.2 8.8M12 20.8c-3.4-1.6-5.2-4.7-5.2-8.8"/><ellipse cx="12" cy="12" rx="9.4" ry="3.2" transform="rotate(-16 12 12)"/></svg>'
ICON_ROCKET = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M14.5 4.2c2.6-1.5 5.3-1.2 5.3-1.2s.3 2.7-1.2 5.3c-1.5 2.6-5 5.3-7.2 6.8l-3.7-3.7c1.5-2.2 4.2-5.7 6.8-7.2z"/><circle cx="15.5" cy="8.5" r="1.5"/><path d="M7.7 11.4 4.4 12l3.1 2.1M12.6 16.3l-.6 3.3 2.1-3.1M5.2 18.8c1.4-1.4 3-.4 3 1.2 0 1.6-1.6 2.4-3.4 1.9"/></svg>'
ICON_LIFE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="8.6"/><path d="M3.6 12h16.8M12 3.4c2.2 2.3 3.4 5.4 3.4 8.6S14.2 18.3 12 20.6c-2.2-2.3-3.4-5.4-3.4-8.6S9.8 5.7 12 3.4z"/></svg>'
ICON_QUESTION = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.4 9.2a2.7 2.7 0 1 1 3.4 3.2c-.9.4-1.3 1-1.3 2M11.5 17.6h.01"/></svg>'
ICONS = {
    "planet": ICON_PLANET,
    "star": ICON_STAR,
    "galaxy": ICON_GALAXY,
    "hole": ICON_HOLE,
    "rocket": ICON_ROCKET,
    "life": ICON_LIFE,
    "question": ICON_QUESTION,
}


def scene_icon(key):
    return ICONS.get(key, ICON_PLANET)


def bh_widget():
    return """<div class="calc">
          <div class="calc__slider">
            <label class="sr-only" for="bhSlider">Απόσταση από τη μαύρη τρύπα, σε ακτίνες Schwarzschild</label>
            <input type="range" id="bhSlider" min="1.05" max="20" step="0.05" value="3">
            <div class="calc__ticks"><span>1 rₛ — ορίζοντας</span><span>10 rₛ</span><span>20 rₛ</span></div>
            <div class="calc__readout">
              <span>Απόσταση</span>
              <strong class="js-bh-dist">3,00 rₛ</strong>
            </div>
          </div>
          <dl class="calc__results">
            <div class="calc__result"><dt>Χρόνος που περνά</dt><dd class="js-bh-hour">49 λεπτά 29 δευτ.</dd></div>
            <div class="calc__result"><dt>Συντελεστής διαστολής</dt><dd class="js-bh-dilation">0,816</dd></div>
            <div class="calc__result"><dt>Ταχύτητα τροχιάς</dt><dd class="js-bh-orbit">0,50 c</dd></div>
          </dl>
          <p class="calc__note">Για έναν ρολόι σε τροχιά στην επιλεγμένη απόσταση, περνούν τόσα λεπτά όσα θα έδειχνε ένα ρολόι μακριά από τη μαύρη τρύπα μέσα σε μία ώρα. Η τιμή υπολογίζεται από τη μετρική Schwarzschild και αγνοεί την ταχύτητα της τροχιάς.</p>
        </div>"""


def render_block_sections(blocks):
    """Turn content-module blocks into (id, title, inner_html) sections."""
    out = []
    seen = {}
    for i, block in enumerate(blocks):
        kind, ident, title = block[0], block[1], block[2]
        if kind == "note":
            ident = f"note-{i + 1}"
        elif not ident or ident in seen:
            ident = f"block-{i + 1}"
        seen[ident] = True
        if kind in ("prose",):
            inner = f'<div class="prose">{block[3]}</div>'
        elif kind == "interactive":
            inner = f'<div class="prose">{block[3]}</div>' + (bh_widget() if ident == "orizontas" else "")
        elif kind == "note":
            inner = note_block(block[3], block[1])
        elif kind == "cards":
            intro = f'<p class="lead">{block[3]}</p>' if block[3] else ""
            inner = intro + card_grid(block[4])
        elif kind == "gallery":
            inner = gallery(block[3])
        elif kind == "timeline":
            inner = timeline(block[3])
        else:
            continue
        out.append((ident, title, inner))
    return out


def generic_page(page, slug, active, icon_key, scripts, crumb_label=None):
    trail = [("index.html", "Αρχική"), (slug, crumb_label or page["title"])]
    hero = page_hero(
        page["title"],
        page["lead"],
        page["image"],
        trail,
        stats=page["stats"][0],
        kicker=page["kicker"],
        icon=scene_icon(icon_key),
    )
    sections = render_block_sections(page["blocks"])
    toc_extra = f'<a class="toc__cta" href="#main">↑ Επιστροφή στην κορυφή</a>'
    body = (
        hero
        + '\n  <section class="section section--tight">\n    <div class="container">\n      '
        + stat_band(page["stats"])
        + "\n    </div>\n  </section>\n"
        + article_layout(sections, toc_extra=toc_extra)
    )
    return shell.document(
        f'{page["title"]} — Universe Explorer',
        page["lead"][:180],
        "interior",
        active,
        body,
        scripts,
    )


def planet_page(slug):
    p = PLANETS[slug]
    idx = PLANET_ORDER.index(slug)
    prev_slug = PLANET_ORDER[(idx - 1) % len(PLANET_ORDER)]
    next_slug = PLANET_ORDER[(idx + 1) % len(PLANET_ORDER)]
    facts_dl = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in p["facts"])
    ring = '<span class="body-visual__ring" aria-hidden="true"></span>' if slug in ("saturn", "uranus") else ""
    hero = f"""  <section class="body-hero">
    <div class="body-hero__glow" aria-hidden="true"></div>
    <div class="container body-hero__inner">
      <div>
        {breadcrumb([("index.html", "Αρχική"), ("solar-system.html", "Ηλιακό Σύστημα"), (f"planet-{slug}.html", p["name"])])}
        <h1>{esc(p["name"])}</h1>
        <p class="body-hero__sub">{esc(p["en"])} · {esc(p["type"])}</p>
        <p class="body-hero__lead">{esc(p["tagline"])}</p>
        <dl class="body-hero__facts">{facts_dl}</dl>
      </div>
      <div class="body-visual">
        <div class="body-visual__orb">{img(p["image"], p["name"])}{ring}</div>
        <span class="body-visual__tag">{esc(p["type"])}</span>
      </div>
    </div>
  </section>
"""
    sections = [(sid, stitle, f'<div class="prose">{shtml}</div>') for sid, stitle, shtml in p["sections"]]
    did_items = "".join(f"<li>{item}</li>" for item in p["did"])
    extra = (
        '\n  <section class="section section--tight">\n    <div class="container">\n'
        '      <div class="section-head reveal"><div><p class="eyebrow"><span class="dot"></span>Πέντε πράγματα</p>'
        '<h2 class="h2">Ήξερες ότι…</h2></div>'
        f'<p class="lead">Μικρές λεπτομέρειες για τον {esc(p["name"])} που συχνά ξαφνιάζουν.</p></div>'
        f'<ul class="two-col-list reveal">{did_items}</ul>\n    </div>\n  </section>\n'
    )
    nav = (
        '  <section class="section section--tight">\n    <div class="container">\n      <div class="planet-nav">'
        + link_arrow(f"planet-{prev_slug}.html", PLANETS[prev_slug]["name"], back=True)
        + '<a class="chip" href="solar-system.html">Όλο το ηλιακό σύστημα</a>'
        + link_arrow(f"planet-{next_slug}.html", PLANETS[next_slug]["name"])
        + "</div>\n    </div>\n  </section>\n"
    )
    toc_extra = '<a class="toc__cta" href="solar-system.html#orrery">Διαδραστικό μοντέλο</a>'
    body = hero + article_layout(sections, toc_extra=toc_extra) + extra + nav
    return shell.document(
        f'{p["name"]} — Universe Explorer',
        f'{p["name"]}: {p["tagline"]}'[:180],
        "planet",
        "solar-system.html",
        body,
        ("core.js", "search-data.js", "search.js", "music.js"),
    )


def solar_page():
    page = cs.SOLAR
    hero = page_hero(
        page["title"],
        page["lead"],
        page["image"],
        [("index.html", "Αρχική"), ("solar-system.html", "Ηλιακό Σύστημα")],
        stats=page["stats"][0],
        kicker=page["kicker"],
        icon=scene_icon("planet"),
    )
    orbits_html = []
    for i, (slug2, frac, period) in enumerate(cpe.ORBITS):
        o = cpe.ORRERY[slug2]
        ring_cls = " planet-dot--ring" if slug2 == "saturn" else ""
        orbits_html.append(
            f'        <div class="orbit" data-r="{frac}" data-period="{period}"'
            f'{" style=\"--dur: 60s\"" if False else ""}>'
            f'<div class="orbit__rotor"><button type="button" class="planet-dot{ring_cls}"'
            f' data-planet="{slug2}" aria-pressed="false" aria-label="{esc(o["name"])}"'
            f' style="--size:{o["size"]}px;--dot-bg:{o["color"]};--dot-glow:{o["color"]}88"></button></div></div>'
        )
    orbit_table = "".join(
        f'<tr><td><span class="orbit-swatch" style="--dot-bg:{cpe.ORRERY[s]["color"]}"></span>'
        f'<a href="planet-{s}.html">{esc(cpe.ORRERY[s]["name"])}</a></td>'
        f'<td>{(period / 365.25) ** (2 / 3):.2f} AU</td><td>{period:,.0f} ημέρες</td></tr>'.replace(",", ".")
        for s, frac, period in cpe.ORBITS
    )
    legend = "".join(
        f'<a class="chip" href="planet-{s}.html">{esc(cpe.ORRERY[s]["name"])}</a>'
        for s in PLANET_ORDER if s != "sun"
    )
    orrery = f"""  <section class="section section--tight" id="orrery">
    <div class="container">
      <div class="section-head reveal">
        <div><p class="eyebrow"><span class="dot"></span>Διαδραστικό</p><h2 class="h2">Το ηλιακό σύστημα σε κίνηση</h2></div>
        <p class="lead">Επίλεξε έναν πλανήτη για να δεις τα βασικά του στοιχεία. Οι αποστάσεις και οι ταχύτητες είναι σχηματικές, όχι σε κλίμακα.</p>
      </div>
      <div class="solar-wrap reveal">
        <div class="solar" id="solar">
          <div class="solar__stage">
            <div class="solar__center">
              <button type="button" class="solar__sun" aria-label="Ήλιος"></button>
              <span class="solar__label">Ήλιος</span>
            </div>
{chr(10).join(orbits_html)}
          </div>
          <p class="solar__hint"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M9 11V5.5a1.5 1.5 0 0 1 3 0V11m0-1.5a1.5 1.5 0 0 1 3 0V12m0-1a1.5 1.5 0 0 1 3 0v5.5A5.5 5.5 0 0 1 12.5 22h-1a5 5 0 0 1-3.8-1.8L5 16.4a1.6 1.6 0 0 1 2.4-2.1L9 16"/></svg>Πάτησε έναν πλανήτη</p>
          <aside class="solar__info" id="solarInfo">
            <span class="badge badge--violet js-solar-type">Βραχώδης πλανήτης</span>
            <h3 class="js-solar-title">Γη</h3>
            <p class="js-solar-desc"></p>
            <dl class="js-solar-facts"></dl>
            <a class="link-arrow js-solar-link" href="planet-earth.html">Άνοιξε τη σελίδα της Γης</a>
          </aside>
          <div class="solar__controls">
            <div class="solar__speed">
              <label for="solarSpeed">Ταχύτητα</label>
              <input type="range" id="solarSpeed" min="0" max="100" value="45" step="1">
            </div>
            <button type="button" class="icon-btn" id="solarPause" aria-pressed="false"><span>Παύση κίνησης</span></button>
          </div>
        </div>
        <div class="solar__legend">{legend}</div>
      </div>
    </div>
  </section>
"""
    planet_cards = []
    for s in PLANET_ORDER:
        if s == "sun":
            continue
        p = PLANETS[s]
        planet_cards.append(
            f'<a class="card" href="planet-{s}.html"><div class="media media--wide media--bleed media--zoom">'
            f'{img(p["image"], p["name"])}</div><div class="card__body">'
            f'<div class="card__meta"><span>{esc(p["type"])}</span></div>'
            f'<h3 class="card__title">{esc(p["name"])}</h3>'
            f'<p class="card__text">{esc(p["tagline"])}</p></div></a>'
        )
    grid = (
        '\n  <section class="section section--tight" id="planetes">\n    <div class="container">\n'
        '      <div class="sec-head-row reveal"><div><p class="eyebrow"><span class="dot"></span>Οι οκτώ</p>'
        '<h2 class="h2">Πλανήτες, ένας ένας</h2></div>'
        '<a class="link-arrow" href="planet-sun.html">Ξεκίνα από τον Ήλιο<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a></div>'
        '<div class="grid grid--3 reveal">' + "".join(planet_cards) + "</div>\n    </div>\n  </section>\n"
    )
    table = (
        '\n  <section class="section section--tight" id="stoicheia">\n    <div class="container">\n'
        '      <div class="section-head reveal"><div><p class="eyebrow"><span class="dot"></span>Σε αριθμούς</p>'
        '<h2 class="h2">Τροχιές και περίοδοι</h2></div>'
        '<p class="lead">Η μέση απόσταση από τον Ήλιο υπολογίζεται από τον τρίτο νόμο του Kepler, με βάση την περίοδο περιφοράς.</p></div>'
        '<div class="table-wrap reveal"><table><thead><tr><th>Πλανήτης</th><th>Μέση απόσταση</th><th>Περίοδος περιφοράς</th></tr></thead>'
        f"<tbody>{orbit_table}</tbody></table></div>\n    </div>\n  </section>\n"
    )
    sections = render_block_sections(page["blocks"])
    body = (
        hero
        + '\n  <section class="section section--tight">\n    <div class="container">\n      '
        + stat_band(page["stats"])
        + "\n    </div>\n  </section>\n"
        + article_layout(sections, toc_extra='<a class="toc__cta" href="#orrery">Διαδραστικό μοντέλο</a>')
        + orrery
        + grid
        + table
    )
    return shell.document(
        "Το Ηλιακό μας Σύστημα — Universe Explorer",
        "Ο Ήλιος, οι οκτώ πλανήτες, οι νάνοι πλανήτες, οι δορυφόροι και τα μικρά σώματα του ηλιακού μας συστήματος."[:180],
        "interior",
        "solar-system.html",
        body
        + data_script("UE_SOLAR", cpe.ORRERY),
        ("core.js", "search-data.js", "search.js", "music.js", "solar.js"),
    )


import html
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location("ue_site", ROOT / "tools/site.py")
shell = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shell)
import content_home as home  # noqa: E402
import content_planets as cp  # noqa: E402
import content_planets_extra as cpe  # noqa: E402
import content_quiz as cq  # noqa: E402
import content_space as cs  # noqa: E402
import content_topics as ct  # noqa: E402

SRC = ROOT / "src"
DIST = ROOT / "dist"

PLANETS = {**cp.PLANETS, **cpe.EXTRA_PLANETS}
PLANET_ORDER = ["sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]

CAT = {
    "index.html": "Αρχική",
    "solar-system.html": "Ηλιακό Σύστημα",
    "stars.html": "Άστρα",
    "galaxies.html": "Γαλαξίες",
    "black-holes.html": "Μαύρες Τρύπες",
    "exploration.html": "Εξερεύνηση",
    "life.html": "Ζωή στο Σύμπαν",
    "mysteries.html": "Μυστήρια",
    "quiz.html": "Κουίζ",
}


def esc(value):
    return html.escape(str(value), quote=True)


def img(key, alt, cls="", lazy=True, sizes=None):
    attrs = [
        f'src="assets/img/{esc(key)}.jpg"',
        f'alt="{esc(alt)}"',
        'decoding="async"',
    ]
    if lazy:
        attrs.append('loading="lazy"')
    if cls:
        attrs.append(f'class="{cls}"')
    if sizes:
        attrs.append(f'sizes="{esc(sizes)}"')
    return "<img " + " ".join(attrs) + ">"


def badge(label, kind="violet"):
    return f'<span class="badge badge--{esc(kind)}">{esc(label)}</span>'


def link_arrow(href, text, back=False):
    arrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M19 12H5M11 5l-7 7 7 7"/></svg>'
    if not back:
        arrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'
    return f'<a class="link-arrow" href="{esc(href)}">{esc(text)}{arrow}</a>'


def breadcrumb(trail):
    parts = []
    for i, (href, label) in enumerate(trail):
        if href:
            parts.append(f'<a href="{esc(href)}">{esc(label)}</a>')
        else:
            parts.append(f"<span>{esc(label)}</span>")
        if i < len(trail) - 1:
            parts.append('<span aria-hidden="true">/</span>')
    return '<nav class="breadcrumb" aria-label="Διαδρομή">' + "".join(parts) + "</nav>"


def page_hero(title, lead, image, trail, stats=None, kicker=None, icon=None):
    side = ""
    if stats:
        label, value = stats[0], stats[1]
        side = (
            '<div class="page-hero__side"><span>' + esc(label) + "</span><strong>"
            + esc(value) + "</strong></div>"
        )
    icon_html = f'<span class="page-hero__icon">{icon}</span>' if icon else ""
    kicker_html = f'<p class="eyebrow">{esc(kicker)}</p>' if kicker else ""
    return f"""  <section class="page-hero">
    <div class="page-hero__bg" style="background-image:url('assets/img/{esc(image)}.jpg')"></div>
    <div class="container page-hero__inner">
      <div>
        {breadcrumb(trail)}
        {icon_html}
        {kicker_html}
        <h1>{esc(title)}</h1>
        <p class="page-hero__lead">{esc(lead)}</p>
      </div>
      {side}
    </div>
  </section>
"""


def stat_band(stats):
    cells = "".join(
        f'<div class="stat"><span class="stat__value">{esc(v)}</span>'
        f'<span class="stat__label">{esc(k)}</span></div>'
        for k, v in stats
    )
    return f'<div class="stat-band reveal">{"".join(cells)}</div>'


def article_layout(sections, toc_label="Σε αυτή τη σελίδα", toc_extra=""):
    """sections: list of (id, title, inner_html)."""
    toc_items = "".join(f'<a href="#{esc(i)}">{esc(t)}</a>' for i, t, _ in sections if t)
    toc = (
        f'<aside class="toc" aria-label="{esc(toc_label)}">'
        f'<span class="toc__label">{esc(toc_label)}</span>{toc_items}{toc_extra}</aside>'
    )
    body = "".join(sections_html(s) for s in sections)
    return f'  <div class="container article-layout">\n    <div class="article">\n{body}\n    </div>\n    {toc}\n  </div>\n'


def sections_html(section):
    ident, title, inner = section
    heading = f"<h2>{esc(title)}</h2>" if title else ""
    return f'      <section class="block reveal" id="{esc(ident)}">{heading}\n{inner}\n      </section>'


def prose(inner, ident=None, title=None):
    return (ident or "", title or "", f'<div class="prose">{inner}</div>')


def gallery(items):
    figs = "".join(
        f'<figure>{img(key, cap)}<figcaption>{esc(cap)}</figcaption></figure>'
        for key, cap in items
    )
    return f'<div class="gallery">{figs}</div>'


def timeline(items, compact=True):
    rows = "".join(
        f'<div class="timeline__item"><div class="timeline__year">{esc(year)}</div>'
        f'<div class="timeline__body"><h3>{esc(title)}</h3><p>{esc(text)}</p></div></div>'
        for year, title, text in items
    )
    cls = "timeline timeline--compact" if compact else "timeline"
    return f'<div class="{cls}">{rows}</div>'


def card_grid(items, cols=3):
    cards = []
    for it in items:
        media = ""
        if it.get("img"):
            media = (
                f'<div class="media media--wide media--bleed media--zoom">'
                f'{img(it["img"], it["title"])}</div>'
            )
        tags = []
        if it.get("badge"):
            tags.append(badge(it["badge"], it.get("badge_kind", "violet")))
        meta = ""
        if tags or it.get("meta"):
            meta = '<div class="card__meta">' + "".join(tags) + (f'<span>{esc(it["meta"])}</span>' if it.get("meta") else "") + "</div>"
        cards.append(
            f'<article class="card">\n{media}\n<div class="card__body">'
            f'<h3 class="card__title">{esc(it["title"])}</h3>'
            f'<p class="card__text">{esc(it["text"])}</p>{meta}</div></article>'
        )
    return f'<div class="grid grid--{cols}">' + "".join(cards) + "</div>"


def note_block(inner, kind="confirmed"):
    kind = {"confirmed": "note--confirmed", "open": "note--unknown", "unknown": "note--unknown"}.get(kind, "")
    icon = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">'
        '<circle cx="12" cy="12" r="8.4"/><path d="M12 8v4.6M12 16h.01"/></svg>'
    )
    return f'<div class="note {kind}"><span class="note__icon">{icon}</span><div>{inner}</div></div>'


# ==========================================================================
# HOME PAGE
# ==========================================================================
HERO_PLANET = """<svg viewBox="0 0 460 460" role="img" aria-label="Σχηματική απεικόνιση γίγαντα αερίων με δακτυλίους">
        <defs>
          <radialGradient id="pg" cx="34%" cy="28%" r="82%">
            <stop offset="0%" stop-color="#f6e0c2"/>
            <stop offset="38%" stop-color="#d9b083"/>
            <stop offset="72%" stop-color="#8a6a9e"/>
            <stop offset="100%" stop-color="#241a44"/>
          </radialGradient>
          <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#cbb8ff" stop-opacity=".15"/>
            <stop offset="35%" stop-color="#f0dcb8" stop-opacity=".8"/>
            <stop offset="65%" stop-color="#9fd8ff" stop-opacity=".55"/>
            <stop offset="100%" stop-color="#8b5cf6" stop-opacity=".1"/>
          </linearGradient>
          <clipPath id="pgClip"><circle cx="230" cy="230" r="132"/></clipPath>
          <clipPath id="ringFront"><rect x="0" y="236" width="460" height="224"/></clipPath>
        </defs>
        <g class="planet-spin">
          <circle cx="230" cy="230" r="132" fill="url(#pg)"/>
          <g clip-path="url(#pgClip)" fill="#fff">
            <ellipse cx="230" cy="168" rx="150" ry="13" opacity=".12"/>
            <ellipse cx="230" cy="204" rx="150" ry="9" opacity=".08"/>
            <ellipse cx="230" cy="246" rx="150" ry="16" opacity=".14"/>
            <ellipse cx="230" cy="284" rx="150" ry="10" opacity=".09"/>
            <ellipse cx="230" cy="312" rx="150" ry="7" opacity=".07"/>
          </g>
          <circle cx="230" cy="230" r="132" fill="none" stroke="rgba(255,255,255,.16)" stroke-width="1"/>
        </g>
        <ellipse cx="230" cy="242" rx="206" ry="48" fill="none" stroke="url(#ring)" stroke-width="11" transform="rotate(-15 230 242)" opacity=".55"/>
        <g clip-path="url(#ringFront)">
          <ellipse cx="230" cy="242" rx="206" ry="48" fill="none" stroke="url(#ring)" stroke-width="11" transform="rotate(-15 230 242)" opacity=".9"/>
        </g>
      </svg>"""


def hero_section():
    meta = "".join(f"<li>{esc(m)}</li>" for m in home.HERO["meta"])
    return f"""  <section class="hero">
    <div class="hero__bg" aria-hidden="true"></div>
    <div class="container hero__inner">
      <div class="hero__copy">
        <p class="eyebrow"><span class="dot"></span>{esc(home.HERO["eyebrow"])}</p>
        <h1>{home.HERO["title"]}</h1>
        <p class="hero__lead">{esc(home.HERO["lead"])}</p>
        <div class="hero__actions">
          <a class="btn" href="#journey">Ξεκίνα την εξερεύνηση
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </a>
          <a class="btn btn--ghost" href="quiz.html">Δοκίμασε το κουίζ</a>
        </div>
        <ul class="hero__meta">{meta}</ul>
      </div>
      <div class="hero__planet">{HERO_PLANET}</div>
    </div>
    <a class="hero__scroll" href="#journey">Κύλισε<i aria-hidden="true"></i></a>
  </section>
"""


def journey_section():
    cards = []
    for item in home.JOURNEY:
        cards.append(
            f'<a class="card" href="{esc(item["href"])}">'
            f'<div class="card__media">{img(item["img"], item["title"])}'
            f'<span class="card__index">{esc(item["n"])}</span></div>'
            '<div class="card__body">'
            f'<h3 class="card__title">{esc(item["title"])}</h3>'
            f'<p class="card__text">{esc(item["text"])}</p>'
            f'<span class="card__meta">{esc(item["meta"])}</span>'
            '<span class="card__arrow">Εξερεύνησε'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'
            "</span></div></a>"
        )
    return f"""  <section class="section" id="journey">
    <div class="container">
      <div class="section-head reveal">
        <div><p class="eyebrow"><span class="dot"></span>Ο χάρτης του ταξιδιού</p>
        <h2 class="h2">Οκτώ σταθμοί στο άπειρο</h2></div>
        <p class="lead">Από τον Ήλιο και τους γείτονές μας μέχρι τις μαύρες τρύπες και τα όρια της γνώσης. Διάλεξε από πού θα ξεκινήσεις.</p>
      </div>
      <div class="journey reveal">{"".join(cards)}</div>
    </div>
  </section>
"""


def cosmic_section():
    steps = "".join(
        f'<button type="button" class="cosmic-step" role="tab" aria-selected="false" data-step="{i}">'
        f'<span class="cosmic-step__time">{esc(s["time"])}</span>'
        f'<span class="cosmic-step__label">{esc(s["label"])}</span></button>'
        for i, s in enumerate(home.COSMIC)
    )
    first = home.COSMIC[0]
    return f"""  <section class="section" id="cosmos">
    <div class="container">
      <div class="section-head reveal">
        <div><p class="eyebrow"><span class="dot"></span>13,8 δισεκατομμύρια χρόνια</p>
        <h2 class="h2">Η ιστορία του σύμπαντος σε έξι στιγμές</h2></div>
        <p class="lead">Πάτησε έναν σταθμό της χρονογραμμής. Κάθε σημείο κρύβει μια διαφορετική εποχή — και μια διαφορετική βεβαιότητα.</p>
      </div>
      <div class="reveal" id="cosmic">
        <div class="cosmic-timeline" role="tablist" aria-label="Χρονογραμμή του σύμπαντος">{steps}</div>
        <div class="cosmic-detail is-visible">
          <span class="badge badge--cyan js-cosmic-badge">{esc(first["badge"])}</span>
          <h3 class="js-cosmic-title">{esc(first["title"])}</h3>
          <p class="js-cosmic-text">{esc(first["text"])}</p>
        </div>
      </div>
    </div>
  </section>
"""


def fact_section():
    return f"""  <section class="section section--tight">
    <div class="container container--narrow">
      <div class="fact-card reveal" id="factCard">
        <div class="fact-card__head">
          <span class="fact-card__tag js-fact-tag">{esc(home.FACTS[0]["tag"])}</span>
          <span class="badge badge--violet">Τυχαίο επιστημονικό γεγονός</span>
        </div>
        <p class="fact-card__text js-fact-text">{esc(home.FACTS[0]["text"])}</p>
        <div class="fact-card__foot">
          <span>Πάτησε για το επόμενο γεγονός</span>
          <button type="button" class="btn btn--ghost js-fact-next">Επόμενο γεγονός
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>
    </div>
  </section>
"""


def feature_section():
    return f"""  <section class="section section--tight">
    <div class="container">
      <div class="feature-band reveal">
        {img("galaxy-milkyway", "Ο Γαλαξίας μας σε οπτικό και υπέρυθρο φως")}
        <div class="feature-band__content">
          <span class="badge badge--violet">Ο οίκος μας</span>
          <h2>Είμαστε ένα αστέρι ανάμεσα σε δισεκατομμύρια</h2>
          <p>Ο Ήλιος βρίσκεται σε έναν από τους βραχίονες του Γαλαξία, περίπου 26.000 έτη φωτός από το κέντρο του. Ταξιδεύει γύρω του με 220 χλμ./δευτ. και χρειάζεται 230 εκατομμύρια χρόνια για έναν κύκλο.</p>
          <div class="hero__actions">{link_arrow("galaxies.html", "Γνώρισε τους γαλαξίες")}</div>
        </div>
      </div>
    </div>
  </section>
"""


def home_page():
    body = (
        hero_section()
        + '\n  <div class="ticker" aria-hidden="true"><div class="ticker__track">'
        + "".join(f"<span>{esc(x)}</span>" for x in ["13,8 δισ. έτη", "93 δισ. έτη φωτός", "2 τρισ. γαλαξίες", "8 πλανήτες", "1 γαλαξίας", "10²⁴ αστέρια"])
        + "</div></div>\n"
        + journey_section()
        + cosmic_section()
        + feature_section()
        + fact_section()
        + """  <section class="section">
    <div class="container">
      <div class="cta-band reveal">
        <p class="eyebrow"><span class="dot"></span>Έτοιμος;</p>
        <h2>Πόσο καλά γνωρίζεις το σύμπαν;</h2>
        <p>Δέκα ερωτήσεις, εξηγήσεις για κάθε απάντηση και μια βαθμολογία στο τέλος. Χωρίς χρόνο, χωρίς πίεση.</p>
        <div class="btn-row"><a class="btn" href="quiz.html">Ξεκίνα το κουίζ</a><a class="btn btn--ghost" href="solar-system.html">Πρώτα το ηλιακό σύστημα</a></div>
      </div>
    </div>
  </section>
"""
        + data_script("UE_COSMIC", home.COSMIC)
        + data_script("UE_FACTS", home.FACTS)
    )
    return shell.document(
        "Universe Explorer — Εξερεύνησε το Άπειρο",
        "Ένα ταξίδι στα βάθη του σύμπαντος: πλανήτες, άστρα, γαλαξίες, μαύρες τρύπες και τα μεγάλα μυστήρια που ξεπερνούν τη φαντασία.",
        "home",
        "index.html",
        body,
        ("core.js", "search-data.js", "search.js", "music.js", "interactive.js"),
    )


# ==========================================================================
# QUIZ PAGE
# ==========================================================================
def quiz_page():
    hero = page_hero(
        "Κουίζ Γνώσεων",
        "Δέκα τυχαίες ερωτήσεις από όλες τις ενότητες. Κάθε απάντηση συνοδεύεται από σύντομη εξήγηση — ώστε το κουίζ να είναι και μάθημα.",
        "hero-nebula",
        [("index.html", "Αρχική"), ("quiz.html", "Κουίζ")],
        stats=("Ερωτήσεις", f"{len(cq.QUIZ)} στη δεξαμενή"),
        kicker="Δοκίμασε τον εαυτό σου",
        icon=scene_icon("question"),
    )
    body = (
        hero
        + """  <section class="section section--tight">
    <div class="container">
      <div class="quiz" id="quizApp">
        <div class="quiz__top"><span class="quiz__score">Φόρτωση ερωτήσεων…</span></div>
        <p class="quiz__q">Το κουίζ χρειάζεται JavaScript. Ενεργοποίησέ την για να παίξεις.</p>
      </div>
    </div>
  </section>
  <section class="section section--tight">
    <div class="container">
      <div class="grid grid--3 reveal">
        <article class="card"><div class="card__body">
          <h3 class="card__title">Πώς λειτουργεί</h3>
          <p class="card__text">Κάθε φορά επιλέγονται 10 ερωτήσεις από διαφορετικές ενότητες, με τυχαία σειρά και τυχαία σειρά απαντήσεων.</p>
        </div></article>
        <article class="card"><div class="card__body">
          <h3 class="card__title">Με εξηγήσεις</h3>
          <p class="card__text">Δεν μαθαίνεις μόνο αν έπεσες μέσα: κάθε απάντηση εξηγεί το «γιατί» πίσω από το σωστό αποτέλεσμα.</p>
        </div></article>
        <article class="card"><div class="card__body">
          <h3 class="card__title">Χωρίς πίεση</h3>
          <p class="card__text">Δεν υπάρχει χρονόμετρο. Μπορείς να ξαναδοκιμάσεις όσες φορές θέλεις και να δεις διαφορετικές ερωτήσεις.</p>
        </div></article>
      </div>
      <div class="cta-band reveal mt-4">
        <h2>Θέλεις να διαβάσεις πρώτα;</h2>
        <p>Όλες οι απαντήσεις βρίσκονται στις ενότητες του site — από το ηλιακό σύστημα μέχρι τη σκοτεινή ενέργεια.</p>
        <div class="btn-row"><a class="btn" href="solar-system.html">Ηλιακό Σύστημα</a><a class="btn btn--ghost" href="mysteries.html">Τα Μεγάλα Μυστήρια</a></div>
      </div>
    </div>
  </section>
"""
        + data_script("UE_QUIZ", cq.QUIZ)
    )
    return shell.document(
        "Κουίζ Γνώσεων — Universe Explorer",
        "Δοκίμασε τις γνώσεις σου για το σύμπαν με δέκα τυχαίες ερωτήσεις, εξηγήσεις και βαθμολογία.",
        "interior",
        "quiz.html",
        body,
        ("core.js", "search-data.js", "search.js", "music.js", "interactive.js"),
    )


# ==========================================================================
# SEARCH INDEX
# ==========================================================================
PAGE_BLURB = {
    "index.html": ("Αρχική", "Η αφετηρία του ταξιδιού: το σύμπαν σε μία ματιά, η χρονογραμμή του και τα βασικά μεγέθη του.", "star"),
    "solar-system.html": ("Ηλιακό Σύστημα", "Ήλιος, οκτώ πλανήτες, νάνοι πλανήτες, δορυφόροι, αστεροειδείς και κομήτες — με διαδραστικό μοντέλο τροχιών.", "planet"),
    "stars.html": ("Άστρα", "Γέννηση, λειτουργία και θάνατος των άστρων: ερυθροί γίγαντες, λευκοί νάνοι, σουπερνόβα και αστρικά κατάλοιπα.", "star"),
    "galaxies.html": ("Γαλαξίες", "Τι είναι οι γαλαξίες, ο Γαλαξίας μας, οι μορφές τους, το Τοπικό Σμήνος και οι συγκρούσεις γαλαξιών.", "star"),
    "black-holes.html": ("Μαύρες Τρύπες", "Ορίζοντας γεγονότων, αστρικές και υπερμεγέθεις μαύρες τρύπες, και η διαστολή του χρόνου.", "planet"),
    "exploration.html": ("Εξερεύνηση", "Από το Σπούτνικ και το Apollo 11 μέχρι το James Webb, το Voyager και τον Διεθνή Διαστημικό Σταθμό.", "star"),
    "life.html": ("Ζωή στο Σύμπαν", "Εξωπλανήτες, ζώνες κατοικησιμότητας και η επιστημονική αναζήτηση ζωής έξω από τη Γη.", "planet"),
    "mysteries.html": ("Μυστήρια", "Σκοτεινή ύλη, σκοτεινή ενέργεια, διαστολή του σύμπαντος και τα ερωτήματα που μένουν ανοιχτά.", "star"),
    "quiz.html": ("Κουίζ", "Δέκα τυχαίες ερωτήσεις για το σύμπαν, με εξηγήσεις και βαθμολογία.", "star"),
}


def search_items():
    items = []
    for slug, (title, desc, icon) in PAGE_BLURB.items():
        items.append({"title": title, "desc": desc, "url": slug, "cat": "Ενότητες", "icon": icon})
    for slug in PLANET_ORDER:
        p = PLANETS[slug]
        items.append({
            "title": p["name"],
            "desc": f'{p["en"]} · {p["type"]}. {p["tagline"]}',
            "url": f"planet-{slug}.html",
            "cat": "Πλανήτες & Ήλιος",
            "icon": "planet",
        })
    topic_pages = [("stars", "stars.html"), ("galaxies", "galaxies.html"), ("black-holes", "black-holes.html")]
    for key, slug in topic_pages:
        page = ct.TOPICS[key]
        for block in page["blocks"]:
            if block[0] in ("prose", "note") or not block[2]:
                continue
            ident = block[1] if block[0] != "note" else ""
            if not ident:
                continue
            items.append({
                "title": block[2],
                "desc": f'{page["title"]} · {block[0] == "timeline" and "χρονογραμμή" or "θεματική ενότητα"}',
                "url": f"{slug}#{ident}",
                "cat": page["title"],
                "icon": page["icon"],
            })
    for page, slug in ((cs.SOLAR, "solar-system.html"), (cs.EXPLORATION, "exploration.html"), (cs.LIFE, "life.html"), (cs.MYSTERIES, "mysteries.html")):
        for block in page["blocks"]:
            if not block[2]:
                continue
            items.append({
                "title": block[2],
                "desc": f'{page["title"]} · θεματική ενότητα',
                "url": f'{slug}#{block[1]}',
                "cat": page["title"],
                "icon": page["icon"],
            })
    return items


def data_script(name, payload):
    return (
        "\n  <script>window."
        + name
        + " = "
        + json.dumps(payload, ensure_ascii=False)
        + ";</script>\n"
    )


# ==========================================================================
# BUILD
# ==========================================================================
GENERIC_PAGES = [
    (ct.TOPICS["stars"], "stars.html", "star"),
    (ct.TOPICS["galaxies"], "galaxies.html", "galaxy"),
    (ct.TOPICS["black-holes"], "black-holes.html", "hole"),
    (cs.EXPLORATION, "exploration.html", "rocket"),
    (cs.LIFE, "life.html", "life"),
    (cs.MYSTERIES, "mysteries.html", "galaxy"),
]
CONTENT_SCRIPTS = ("core.js", "search-data.js", "search.js", "music.js", "interactive.js")


def privacy_page():
    contact = shell.CONTACT_EMAIL.strip()
    contact_line = (
        f'Για οποιοδήποτε αίτημα σχετικά με τα δεδομένα σου, γράψε στο '
        f'<a href="mailto:{esc(contact)}">{esc(contact)}</a>.'
        if contact
        else "Για οποιοδήποτε αίτημα σχετικά με τα δεδομένα σου, χρησιμοποίησε τα στοιχεία επικοινωνίας "
        "που δημοσιεύονται στη σελίδα προέλευσης της ιστοσελίδας."
    )
    body = f"""  <section class="section legal">
    <div class="container container--narrow">
      <p class="eyebrow"><span class="dot"></span>Νομικές πληροφορίες</p>
      <h1>Απόρρητο &amp; χρήση τεχνητής νοημοσύνης</h1>
      <p class="lead">Πώς λειτουργεί η ιστοσελίδα, τι δεδομένα υπάρχουν και σε ποιο βαθμό το περιεχόμενο και ο βοηθός δημιουργούνται με AI. Τελευταία ενημέρωση: 21 Νοεμβρίου 2026.</p>
      <div class="prose">
        <h2>1. Ποιοι είμαστε</h2>
        <p>Το <strong>Universe Explorer</strong> είναι ένα ανεξάρτητο, μη εμπορικό εκπαιδευτικό project αστρονομίας. Δεν συνδέεται, δεν χρηματοδοτείται και δεν εγκρίνεται από τη NASA, την ESA, το STScI ή άλλον διαστημικό οργανισμό. Οι αναφορές σε αποστολές και όργανα γίνονται μόνο για εκπαιδευτικούς σκοπούς.</p>

        <h2>2. Χρήση τεχνητής νοημοσύνης — διαφάνεια</h2>
        <ul>
          <li><strong>Περιεχόμενο και κώδικας:</strong> το κείμενο, η σχεδίαση και ο κώδικας της ιστοσελίδας δημιουργήθηκαν με τη βοήθεια συστημάτων AI και ελέγχθηκαν πριν τη δημοσίευση.</li>
          <li><strong>Ψηφιακός βοηθός:</strong> το κουμπί συνομιλίας κάτω δεξιά ανοίγει σύστημα AI (Chatling), όχι άνθρωπο. Οι απαντήσεις παράγονται αυτόματα και μπορεί να είναι ελλιπείς ή λανθασμένες. Μην τις χρησιμοποιείς ως επαγγελματική, ιατρική, νομική ή οικονομική συμβουλή.</li>
          <li><strong>Επιστημονική ακρίβεια:</strong> το περιεχόμενο βασίζεται σε δημόσια επιστημονικά δεδομένα, αλλά η εκπαιδευτική σύνοψη ενδέχεται να μην καλύπτει τις τελευταίες εξελίξεις. Επιβεβαίωσε κρίσιμα στοιχεία σε επίσημες πηγές (NASA, ESA, επιστημονικά περιοδικά).</li>
        </ul>

        <h2>3. Τι δεδομένα υπάρχουν</h2>
        <ul>
          <li><strong>Μηνύματα συνομιλίας:</strong> ό,τι γράφεις στον βοηθό αποστέλλεται στην πλατφόρμα Chatling για να παραχθεί απάντηση. Μην κοινοποιείς προσωπικά δεδομένα, κωδικούς ή ευαίσθητες πληροφορίες.</li>
          <li><strong>Τεχνικά δεδομένα:</strong> ο πάροχος φιλοξενίας της ιστοσελίδας μπορεί να καταγράφει διεύθυνση IP, τύπο browser και χρόνο επίσκεψης για λόγους ασφαλείας, σύμφωνα με τη δική του πολιτική.</li>
          <li><strong>Τοπική αποθήκευση:</strong> η ένταση της μουσικής αποθηκεύεται τοπικά στον browser σου. Δεν δημιουργούμε προφίλ, δεν ζητάμε λογαριασμό και δεν χρησιμοποιούμε διαφημίσεις ή analytics.</li>
        </ul>

        <h2>4. Cookies και εξωτερικές υπηρεσίες</h2>
        <p>Η ιστοσελίδα δεν χρησιμοποιεί δικά της cookies παρακολούθησης. Η ενσωμάτωση του Chatling μπορεί να αποθηκεύσει cookies ή τοπικά δεδομένα για τη λειτουργία της συνομιλίας· δες την <a href="https://chatling.ai/privacy-policy" rel="noopener">πολιτική απορρήτου του Chatling</a>. Η μουσική παράγεται στη συσκευή σου και δεν στέλνεται πουθενά.</p>

        <h2>5. Νομική βάση και διάρκεια</h2>
        <p>Η επεξεργασία για τη λειτουργία της συνομιλίας στηρίζεται στη συγκατάθεσή σου, την οποία δίνεις όταν ανοίγεις τον βοηθό και στέλνεις μήνυμα. Τα μηνύματα διατηρούνται σύμφωνα με τις ρυθμίσεις του λογαριασμού Chatling του διαχειριστή και όχι περισσότερο από όσο απαιτείται για την εξυπηρέτηση του σκοπού.</p>

        <h2>6. Τα δικαιώματά σου (GDPR)</h2>
        <p>Αν βρίσκεσαι στην Ευρωπαϊκή Ένωση, έχεις δικαίωμα πρόσβασης, διόρθωσης, διαγραφής, περιορισμού και εναντίωσης στην επεξεργασία, καθώς και δικαίωμα καταγγελίας στην Αρχή Προστασίας Δεδομένων Προσωπικού Χαρακτήρα (<a href="https://www.dpa.gr" rel="noopener">dpa.gr</a>). {contact_line}</p>

        <h2>7. Ηλικίες</h2>
        <p>Η ιστοσελίδα απευθύνεται σε ευρύ κοινό με εκπαιδευτικό σκοπό. Αν είσαι κάτω των 15 ετών, χρησιμοποίησε τον βοηθό μόνο με τη συνοδεία ενήλικα.</p>

        <h2>8. Αλλαγές</h2>
        <p>Η παρούσα σελίδα μπορεί να ενημερώνεται όταν αλλάζει η λειτουργία της ιστοσελίδας. Η ημερομηνία στην κορυφή δείχνει την τελευταία αναθεώρηση.</p>

        <p class="note"><strong>Σύνοψη:</strong> εκπαιδευτικό site, περιεχόμενο και βοηθός με AI, χωρίς διαφημίσεις και χωρίς δικά μας cookies. Το μόνο που φεύγει από τη συσκευή σου είναι ό,τι γράφεις στη συνομιλία.</p>
      </div>
    </div>
  </section>"""
    return shell.document(
        "Απόρρητο & χρήση AI — Universe Explorer",
        "Πολιτική απορρήτου, cookies και διαφάνεια χρήσης τεχνητής νοημοσύνης στο Universe Explorer.",
        "interior",
        "",
        body,
        ("core.js", "search-data.js", "search.js", "music.js"),
    )


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(SRC / "assets", DIST / "assets")

    pages = {"index.html": home_page()}
    for slug in PLANET_ORDER:
        pages[f"planet-{slug}.html"] = planet_page(slug)
    pages["solar-system.html"] = solar_page()
    for page, slug, icon in GENERIC_PAGES:
        pages[slug] = generic_page(page, slug, slug, icon, CONTENT_SCRIPTS)
    pages["quiz.html"] = quiz_page()
    pages["privacy.html"] = privacy_page()

    search_js = "window.UE_SEARCH = " + json.dumps(search_items(), ensure_ascii=False) + ";\n"
    (DIST / "assets/js/search-data.js").write_text(search_js, encoding="utf-8")

    for name, markup in pages.items():
        (DIST / name).write_text(markup, encoding="utf-8")

    total = sum(1 for _ in DIST.rglob("*") if _.is_file())
    print(f"Built {len(pages)} pages, {total} files in {DIST}")
    print("Search items:", len(json.loads(search_js.split("=", 1)[1].rsplit(";", 1)[0])))


if __name__ == "__main__":
    main()
