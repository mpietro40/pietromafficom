#!/usr/bin/env bash
# Scarica una copia statica (html+css+js) della sezione Galdus e la mette in Galdus/.
# Va lanciato dal tuo computer: richiede wget (macOS: brew install wget).
set -u
cd "$(dirname "$0")/.."
rm -rf .copia
wget --mirror --no-parent --page-requisites --adjust-extension --convert-links \
     --restrict-file-names=nocontrol -e robots=off -P .copia \
     https://www.pietromaffi.com/Galdus/ || echo "(alcune pagine non sono state scaricate: controlla l'elenco sopra)"
rm -rf Galdus && mkdir Galdus
cp -R .copia/www.pietromaffi.com/Galdus/. Galdus/
rm -rf .copia
echo "Fatto. Le pagine .php sono ora file .php.html (HTML già generato)."
echo "Controlla Galdus/ aprendo Galdus/index.html, poi lancia: python build.py"
