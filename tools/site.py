"""Shared layout, navigation and document shell for Universe Explorer."""

# Προαιρετικό: βάλε εδώ το email επικοινωνίας για θέματα απορρήτου (GDPR).
# Αν μείνει κενό, η σελίδα απορρήτου εμφανίζει γενική διατύπωση χωρίς email.
CONTACT_EMAIL = ""

NAV = [
    ("index.html", "Αρχική"),
    ("solar-system.html", "Ηλιακό Σύστημα"),
    ("stars.html", "Άστρα"),
    ("galaxies.html", "Γαλαξίες"),
    ("black-holes.html", "Μαύρες Τρύπες"),
    ("exploration.html", "Εξερεύνηση"),
    ("life.html", "Ζωή στο Σύμπαν"),
    ("mysteries.html", "Μυστήρια"),
    ("quiz.html", "Κουίζ"),
]

CHAT_AI_NOTE = """  <div class="ai-note" role="note">
    <span class="ai-note__badge">AI</span>
    <span class="ai-note__text">Ψηφιακός βοηθός AI — όχι άνθρωπος</span>
  </div>"""

CHATLING_EMBED = """  <!-- ==== Chatling chatbot — αντικαταστήστε μόνο το chatbotId αν αλλάξει το bot ==== -->
  <script>
  window.chtlConfig = {
      chatbotId: "3978654878"
  }
  </script>
  <script
      async
      data-id="3978654878"
      id="chtl-script"
      type="text/javascript"
      src="https://chatling.ai/js/embed.js">
  </script>
  <!-- ==== τέλος Chatling embed ==== -->"""

BRAND_MARK = """<svg class="brand__mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">
        <circle cx="20" cy="20" r="7" fill="url(#bm1)"/>
        <ellipse cx="20" cy="20" rx="17.5" ry="6.4" stroke="url(#bm2)" stroke-width="1.1" transform="rotate(-24 20 20)"/>
        <circle cx="33" cy="27" r="1.7" fill="#8fe3ff"/>
        <defs>
          <radialGradient id="bm1" cx=".35" cy=".3" r=".8">
            <stop offset="0" stop-color="#fff3d8"/>
            <stop offset=".5" stop-color="#ffc978"/>
            <stop offset="1" stop-color="#8b5cf6"/>
          </radialGradient>
          <linearGradient id="bm2" x1="2" y1="20" x2="38" y2="20">
            <stop offset="0" stop-color="#6ad7ff" stop-opacity=".1"/>
            <stop offset=".5" stop-color="#b9a6ff"/>
            <stop offset="1" stop-color="#6ad7ff" stop-opacity=".1"/>
          </linearGradient>
        </defs>
      </svg>"""

def brand_mark(suffix: str) -> str:
    """Brand SVG with unique gradient ids, since it appears in header and footer."""
    return BRAND_MARK.replace("bm1", "bm1" + suffix).replace("bm2", "bm2" + suffix)


ICON_SEARCH = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>"""

ICON_MUSIC = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.6"/><circle cx="17.5" cy="16" r="2.6"/></svg>"""

ICON_MENU = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3.5 7h17M3.5 12h17M3.5 17h17"/></svg>"""

ICON_CLOSE = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>"""

ICON_CLOCK = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>"""

ICON_PLAY = """<svg class="icon-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>"""

ICON_PAUSE = """<svg class="icon-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" hidden><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z"/></svg>"""

ICON_VOLUME = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9.5h3.5L12 5.5v13L7.5 14.5H4z"/><path d="M16 9a4.5 4.5 0 0 1 0 6"/></svg>"""

BASE_HEAD = """<!DOCTYPE html>
<html lang="el">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#04030f">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <link rel="stylesheet" href="assets/css/fonts.css">
  <link rel="stylesheet" href="assets/css/base.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/pages.css">
  <link rel="stylesheet" href="assets/css/responsive.css">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
</head>
<body class="page-{page}">
  <a class="skip-link" href="#main">Μετάβαση στο περιεχόμενο</a>
  <div class="scroll-progress" aria-hidden="true"></div>
  <div class="page-veil" aria-hidden="true"></div>
  <div class="preloader" id="preloader" aria-hidden="true">
    <div class="preloader__orbit"><span></span><span></span><span></span><i></i></div>
    <p class="preloader__text">Ευθυγράμμιση με τα άστρα</p>
    <div class="preloader__bar"><i></i></div>
  </div>

  <div class="space-bg" aria-hidden="true">
    <canvas id="starfield"></canvas>
    <div class="space-bg__nebula"></div>
    <div class="space-bg__nebula space-bg__nebula--two"></div>
    <div class="space-bg__grain"></div>
  </div>
"""

SEARCH_OVERLAY = """  <div class="search" id="search" role="dialog" aria-modal="true" aria-label="Αναζήτηση στο Universe Explorer" aria-hidden="true">
    <div class="search__panel">
      <div class="search__bar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/></svg>
        <label class="sr-only" for="searchInput">Αναζήτηση πλανητών, άστρων, γαλαξιών, αποστολών</label>
        <input class="search__input" id="searchInput" type="search" placeholder="Αναζήτησε πλανήτη, άστρο, γαλαξία, αποστολή…" autocomplete="off" spellcheck="false">
        <button type="button" class="search__close" aria-label="Κλείσιμο αναζήτησης">Esc</button>
      </div>
      <div class="search__body" id="searchResults"></div>
      <div class="search__foot">
        <span>Πλοήγηση με <kbd>↑</kbd> <kbd>↓</kbd> · άνοιγμα με <kbd>Enter</kbd></span>
        <span><kbd>/</kbd> ή <kbd>Ctrl</kbd>+<kbd>K</kbd> για γρήγορη αναζήτηση</span>
      </div>
    </div>
  </div>
"""

MUSIC_PLAYER = """  <div class="music" id="musicPlayer" aria-label="Ατμοσφαιρική μουσική" aria-hidden="true">
    <div class="music__head">
      <span class="music__label">Ambient · Cosmic Drift</span>
      <span class="music__eq" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
      <button type="button" class="search__close js-music-close" aria-label="Κλείσιμο μουσικής">✕</button>
    </div>
    <p class="music__track">Ταξίδι στο άπειρο</p>
    <div class="music__row">
      <button type="button" class="music__play" aria-pressed="false" aria-label="Αναπαραγωγή μουσικής">
        {play}{pause}
      </button>
      <div class="music__vol">
        {vol}
        <label class="sr-only" for="musicVolume">Ένταση μουσικής</label>
        <input type="range" id="musicVolume" min="0" max="100" value="45">
      </div>
    </div>
    <p class="music__note">Ατμοσφαιρικός ήχος συνθεμένος στη στιγμή. Δεν ξεκινά ποτέ αυτόματα — μόνο με τη δική σου επιλογή.</p>
  </div>
  <button type="button" class="music-fab" aria-controls="musicPlayer" aria-label="Άνοιγμα μουσικής">
    <span class="music-fab__icon">{note}</span>
    <span class="music-fab__label">Μουσική</span>
  </button>
"""

ICON_NOTE = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.4"/><circle cx="17.5" cy="16" r="2.4"/></svg>"""


def header(active: str) -> str:
    items = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == active else ""
        items.append(f'          <li><a href="{href}"{current}>{label}</a></li>')
    nav_html = "\n".join(items)

    mobile = []
    for i, (href, label) in enumerate(NAV, start=1):
        current = ' aria-current="page"' if href == active else ""
        mobile.append(
            f'          <li><a href="{href}"{current}><span>{i:02d}</span>{label}</a></li>'
        )
    mobile_html = "\n".join(mobile)

    return f"""  <header class="site-header" id="siteHeader">
    <div class="container site-header__inner">
      <a class="brand" href="index.html" aria-label="Universe Explorer — αρχική">
        {brand_mark("h")}
        <span class="brand__text">
          <span class="brand__name">Universe</span>
          <span class="brand__sub">Explorer</span>
        </span>
      </a>
      <nav class="main-nav" aria-label="Κύρια πλοήγηση">
        <ul>
{nav_html}
        </ul>
      </nav>
      <div class="header-tools">
        <button type="button" class="icon-btn js-search-open" aria-label="Αναζήτηση" title="Αναζήτηση (/)">{ICON_SEARCH}</button>
        <button type="button" class="icon-btn js-music-toggle" aria-label="Μουσική" aria-controls="musicPlayer" title="Μουσική">{ICON_MUSIC}</button>
        <button type="button" class="icon-btn nav-toggle" aria-label="Άνοιγμα μενού" aria-expanded="false" aria-controls="mobileNav">{ICON_MENU}</button>
      </div>
    </div>
  </header>

  <div class="mobile-nav" id="mobileNav" aria-label="Μενού πλοήγησης">
    <div class="mobile-nav__top">
      <a class="brand" href="index.html" aria-label="Universe Explorer — αρχική">
        {brand_mark("m")}
        <span class="brand__text"><span class="brand__name">Universe</span><span class="brand__sub">Explorer</span></span>
      </a>
      <button type="button" class="icon-btn js-nav-close" aria-label="Κλείσιμο μενού">{ICON_CLOSE}</button>
    </div>
    <ul class="mobile-nav__list">
{mobile_html}
    </ul>
    <div class="mobile-nav__foot">
      <p>Ένα ταξίδι στα βάθη του σύμπαντος, με επιστημονικά τεκμηριωμένο περιεχόμενο στα ελληνικά.</p>
    </div>
  </div>
"""


def footer() -> str:
    return """  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="brand" href="index.html" aria-label="Universe Explorer — αρχική">
            {brand}
            <span class="brand__text"><span class="brand__name">Universe</span><span class="brand__sub">Explorer</span></span>
          </a>
          <p>Μια διαδραστική πλατφόρμα εξερεύνησης του σύμπαντος: πλανήτες, άστρα, γαλαξίες, μαύρες τρύπες και τα μεγάλα ερωτήματα που ακόμη περιμένουν απάντηση.</p>
        </div>
        <div class="footer-col">
          <h4>Εξερεύνηση</h4>
          <ul>
            <li><a href="solar-system.html">Ηλιακό Σύστημα</a></li>
            <li><a href="stars.html">Άστρα &amp; Αστρική Εξέλιξη</a></li>
            <li><a href="galaxies.html">Γαλαξίες</a></li>
            <li><a href="black-holes.html">Μαύρες Τρύπες</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Ανακάλυψε</h4>
          <ul>
            <li><a href="exploration.html">Εξερεύνηση του Διαστήματος</a></li>
            <li><a href="life.html">Ζωή πέρα από τη Γη</a></li>
            <li><a href="mysteries.html">Τα Μεγάλα Μυστήρια</a></li>
            <li><a href="quiz.html">Κουίζ Γνώσεων</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Σχετικά</h4>
          <ul>
            <li><a href="index.html#journey">Οι ενότητες</a></li>
            <li><a href="index.html#timeline">Χρονολόγιο σύμπαντος</a></li>
            <li><a href="solar-system.html#orrery">Διαδραστικό ηλιακό σύστημα</a></li>
            <li><a href="exploration.html#credits">Πηγές εικόνων</a></li>
            <li><a href="privacy.html">Απόρρητο &amp; χρήση AI</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-disclosure">
        <p><strong>Διαφάνεια AI:</strong> Το κείμενο, η σχεδίαση και ο κώδικας της ιστοσελίδας δημιουργήθηκαν με τη βοήθεια συστημάτων τεχνητής νοημοσύνης (AI). Ο ψηφιακός βοηθός στο κουμπί συνομιλίας είναι επίσης σύστημα AI, όχι άνθρωπος, και οι απαντήσεις του μπορεί να περιέχουν ανακρίβειες. Το περιεχόμενο έχει εκπαιδευτικό χαρακτήρα και δεν αποτελεί επαγγελματική συμβουλή.</p>
        <p><strong>Εικόνες &amp; ανεξαρτησία:</strong> Οι εικόνες προέρχονται από δημόσια αρχεία της NASA, ESA και STScI και χρησιμοποιούνται με αναφορά πηγής για εκπαιδευτικούς σκοπούς. Η ιστοσελίδα είναι ανεξάρτητο εκπαιδευτικό project και δεν συνδέεται ούτε εγκρίνεται από τη NASA, την ESA ή άλλον οργανισμό. <a href="privacy.html">Απόρρητο &amp; χρήση AI</a></p>
      </div>
      <div class="footer-bottom">
        <p>© <span class="js-year">2026</span> Universe Explorer · Εκπαιδευτικό project αστρονομίας</p>
        <p class="credits">Χωρίς διαφημίσεις και χωρίς εργαλεία παρακολούθησης (analytics).</p>
      </div>
    </div>
  </footer>
""".replace("{brand}", brand_mark("f"))


def document(title: str, desc: str, page: str, active: str, body: str, scripts=("core.js", "search.js", "music.js")) -> str:
    head = BASE_HEAD.format(title=title, desc=desc, page=page)
    script_tags = "\n".join(f'  <script src="assets/js/{name}" defer></script>' for name in scripts)
    return (
        head
        + header(active)
        + '\n  <main id="main">\n'
        + body
        + "\n  </main>\n"
        + footer()
        + "\n"
        + SEARCH_OVERLAY
        + MUSIC_PLAYER.replace("{play}", ICON_PLAY).replace("{pause}", ICON_PAUSE).replace("{vol}", ICON_VOLUME).replace("{note}", ICON_NOTE)
        + "\n"
        + script_tags
        + "\n"
        + CHAT_AI_NOTE
        + "\n"
        + CHATLING_EMBED
        + "\n</body>\n</html>\n"
    )
