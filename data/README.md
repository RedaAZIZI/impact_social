# Données

Aucune donnée n'est commitée dans ce dépôt. Les scripts de ce dossier téléchargent les jeux de données UCI utilisés en phase 2 :

```bash
python data/download_uci.py            # German Credit + Heart Disease
```

Ces jeux servent le test go/no-go du projet : sur données réelles, le vocabulaire expert (concepts dérivés : ratio dette/revenu, IMC, pression pulsée…) domine-t-il les features brutes sur la courbe d'explicabilité ?
