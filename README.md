# Sito di Pietro Maffi – guida rapida

Sito statico (html + css, nessun database). Le pagine sono file **Markdown** in `content/`.
La cartella `Galdus/` viene pubblicata identica, senza elaborazioni.

## 1. Aggiornare un testo

1. Su github.com apri il repository → `content/` → il file (es. `tips.md`).
2. Clicca la matita, scrivi, poi **Commit changes**. Dopo circa un minuto è online.

Markdown minimo:

    # Titolo      ## Sezione      **grassetto**   *corsivo*
    - elemento di elenco
    [testo del link](https://indirizzo.it)
    ![descrizione dell'immagine](https://indirizzo.it/img.png)

**Nuova pagina:** crea `content/nome.md` che inizia con

    ---
    title: Titolo della pagina
    menu: Voce nel menu        (scrivi  menu: -  per non metterla nel menu)
    order: 5                   (posizione nel menu)
    lang: it                   (facoltativo, es. en)
    ---

L'indirizzo sarà `/nome/`. La voce **Galdus** (ordine 3) è fissa e porta alla sezione intatta.

## 2. Copiare la sezione Galdus (una volta sola)

Dal tuo computer, nella cartella del progetto:

    ./scripts/scarica-galdus.sh

Scarica il sito attuale in `Galdus/`. Le pagine `.php` diventano `.php.html` (HTML già generato:
si vedono come oggi, ma database e moduli non funzionano). Poi: `python build.py` e controlla `dist/`.

## 3. Pagine da migrare dal vecchio sito

Sono create ma contengono solo un avviso: `less.md`, `unfix.md`, `okr.md`, `linux-unix.md`,
`windows10.md`. Copia il testo da pietromaffi.com/gs **prima** di spostare il dominio: dopo,
il vecchio sito non sarà più raggiungibile. Anche la pagina Galdus di GetSimple è sostituita
dalla vera sezione `Galdus/`.

## 4. Pubblicare gratis (GitHub Pages)

1. Crea un repository **pubblico** e carica tutti i file (anche la cartella nascosta `.github`).
2. Settings → Pages → Source: **GitHub Actions**.
3. Settings → Pages → Custom domain: `pietromaffi.com`, poi **Enforce HTTPS**.
4. Nel DNS: record `A` verso gli indirizzi indicati nella documentazione GitHub Pages e
   `CNAME` di `www` verso `<tuo-utente>.github.io`.

Alternativa: Cloudflare Pages, con build `pip install -r requirements.txt && python build.py`
e cartella di output `dist`.

## 5. Provare in locale

    pip install -r requirements.txt
    python build.py
    cd dist && python -m http.server 8000      # http://localhost:8000

