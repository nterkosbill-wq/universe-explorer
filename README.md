# Universe Explorer — «Εξερεύνησε το Άπειρο»

Διαδραστική, στατική ιστοσελίδα εξερεύνησης του σύμπαντος στα ελληνικά: 19 σελίδες,
αυτο-φιλοξενούμενες διαστημικές εικόνες NASA, διαδραστικό ηλιακό σύστημα, κουίζ,
αναζήτηση, ambient μουσική και το πραγματικό Chatling chatbot.

## Δομή

```
dist/                     # Έτοιμη, έτοιμη-για-ανέβασμα ιστοσελίδα (αυτό ανεβάζεις)
  index.html              # Αρχική
  solar-system.html       # Ηλιακό σύστημα (ορέρι, νάνοι, δορυφόροι, κομήτες)
  planet-*.html           # 9 ξεχωριστές σελίδες: Ήλιος + 8 πλανήτες
  stars.html              # Άστρα και αστρική εξέλιξη
  galaxies.html           # Γαλαξίες
  black-holes.html        # Μαύρες τρύπες (+ υπολογιστής χρόνου)
  exploration.html        # Ιστορία & αποστολές
  life.html               # Ζωή πέρα από τη Γη
  mysteries.html          # Σκοτεινή ύλη/ενέργεια, διαστολή, όρια
  quiz.html               # Κουίζ γνώσεων με βαθμολογία
  privacy.html            # Απόρρητο, cookies και διαφάνεια χρήσης AI
  assets/{css,js,img,fonts}
src/                      # Πηγαία assets (CSS/JS/εικόνες/γραμματοσειρές)
tools/                    # Γεννήτρια σελίδων (Python 3, μόνο stdlib + Pillow για τις εικόνες)
```

## Διαφάνεια AI & απόρρητο

- Το footer κάθε σελίδας δηλώνει ότι το περιεχόμενο/σχεδίαση έγιναν με βοήθεια AI και ότι
  ο βοηθός συνομιλίας είναι AI, όχι άνθρωπος.
- Δίπλα στο κουμπί του chatbot υπάρχει μόνιμη ετικέτα «AI — Ψηφιακός βοηθός».
- Η σελίδα `privacy.html` καλύπτει δεδομένα συνομιλίας, cookies του Chatling, δικαιώματα GDPR
  και το δικαίωμα καταγγελίας στην ελληνική Αρχή Προστασίας Δεδομένων.
- Για email επικοινωνίας απόρρητου, όρισε τη μεταβλητή `CONTACT_EMAIL` στην αρχή του
  `tools/site.py` και ξανατρέξε `python3 tools/build.py`.

## Δημόσιος σύνδεσμος (GitHub Pages)

https://nterkosbill-wq.github.io/universe-explorer/

Το site δημοσιεύεται από το branch `gh-pages` του repo
[`nterkosbill-wq/universe-explorer`](https://github.com/nterkosbill-wq/universe-explorer)
(ο πηγαίος κώδικας είναι στο `master`). Για ενημέρωση μετά από αλλαγή στο `src/` ή στο `tools/`:

```bash
python3 tools/build.py
rm -rf /tmp/ghpages && mkdir -p /tmp/ghpages
cp -a dist/. /tmp/ghpages/ && cd /tmp/ghpages
printf '' > .nojekyll && git init -q && git add -A
git commit -m "Build: Universe Explorer"
git push -f https://github.com/nterkosbill-wq/universe-explorer.git HEAD:gh-pages
```

Σε αυτόν τον σύνδεσμο το Chatling chatbot φορτώνει και απαντά κανονικά.

## Τοπική προβολή

Η ιστοσελίδα είναι πλήρως στατική — αρκεί ένας απλός server (τα σχετικά links δεν
δουλεύουν σωστά με `file://`):

```bash
cd dist
python3 -m http.server 8000
# http://localhost:8000
```

## Ανέβασμα

Ανέβασε **ολόκληρο τον φάκελο `dist/`** σε Netlify, Vercel, GitHub Pages ή οποιονδήποτε
static host. Δεν χρειάζεται βάση δεδομένων, build step ή server-side κώδικας.

## Επεξεργασία περιεχομένου

Το HTML παράγεται από τα Python modules στο `tools/` (μία πηγή αλήθειας για κείμενα,
πίνακες πλανητών και το ορέρι):

```bash
python3 tools/build.py     # ξαναχτίζει όλο το dist/
```

- `tools/content_planets.py`, `content_planets_extra.py` — πλανήτες
- `tools/content_topics.py` — άστρα, γαλαξίες, μαύρες τρύπες
- `tools/content_space.py` — εξερεύνηση, ζωή, μυστήρια
- `tools/content_quiz.py` — ερωτήσεις κουίζ
- `tools/site.py` — header/footer/πλοήγηση, `tools/build.py` — σελίδες και renderer

Μπορείς επίσης να επεξεργαστείς απευθείας τα HTML στο `dist/`, αν δεν θέλεις rebuild.

## Chatbot (Chatling)

Το πραγματικό embed είναι μία φορά, στο `<head>` κάθε σελίδας μέσω του `tools/site.py`
(συνάρτηση `document`), ώστε να μην διπλασιάζεται το κουμπί:

```html
<script>window.chtlConfig = { chatbotId: "3978654878" }</script>
<script async data-id="3978654878" id="chtl-script"
        src="https://chatling.ai/js/embed.js"></script>
```

Αλλαγή chatbot: τροποποίησε το `chatbotId` στο `tools/site.py` και τρέξε
`python3 tools/build.py` — ή απευθείας στα HTML του `dist/` (αναζήτηση `chtlConfig`).
Το floating κουμπί κάτω δεξιά και το παράθυρο συνομιλίας τα δημιουργεί η Chatling.

Στη Chatling (Settings → Appearance / Greeting) βάλε αυτό το μήνυμα υποδοχής ώστε ο
επισκέπτης να ξέρει ότι μιλάει σε AI:

> Γεια σου! Είμαι ψηφιακός βοηθός AI — όχι άνθρωπος. Ρώτησέ με ό,τι θέλεις για το
> σύμπαν: πλανήτες, άστρα, γαλαξίες, μαύρες τρύπες, αποστολές.

## Χαρακτηριστικά

- Σκούρο διαστημικό design, ζωντανό αστρικό πεδίο, νεφελώματα, reveal-on-scroll.
- Διαδραστικό ηλιακό σύστημα: επιλογή πλανήτη, ταχύτητα, παύση.
- Αναζήτηση (48 καταχωρήσεις) με ομαδοποίηση και άλματα σε ενότητες.
- Κουίζ 10 τυχαίων ερωτήσεων από σύνολο 18, βαθμολογία και επανάληψη.
- «Ήξερες ότι;» με τυχαία γεγονότα, timelines, ανοιγόμενες κάρτες, υπολογιστές.
- Ambient μουσική Web Audio (χωρίς αρχεία ήχου), play/pause και ένταση, ποτέ αυτόματη.
- Πλήρως responsive (κινητό/tablet/desktop), skip link, aria attributes, reduced-motion.

## Εικόνες & πνευματικά δικαιώματα

Οι εικόνες προέρχονται από το δημόσιο αρχείο της NASA (NASA Image and Video Library)
και είναι ως επί το πλείστον public domain. Οι πηγές και τα credits κάθε αρχείου
βρίσκονται στο `src/assets/img/manifest.json` και εμφανίζονται στο footer κάθε σελίδας.

## Γραμματοσειρές

Inter και Literata, αυτο-φιλοξενούμενες (`src/assets/fonts`) με ελληνικό subset —
η σελίδα δεν εξαρτάται από Google Fonts.
