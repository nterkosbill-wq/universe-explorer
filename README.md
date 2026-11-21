# Universe Explorer — «Εξερεύνησε το Άπειρο»

Διαδραστική, στατική ιστοσελίδα εξερεύνησης του σύμπαντος στα ελληνικά: 18 σελίδες,
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
  assets/{css,js,img,fonts}
src/                      # Πηγαία assets (CSS/JS/εικόνες/γραμματοσειρές)
tools/                    # Γεννήτρια σελίδων (Python 3, μόνο stdlib + Pillow για τις εικόνες)
```

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
