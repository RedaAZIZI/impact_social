"""Téléchargement des jeux de données UCI de la phase 2 (rien n'est commité).

- German Credit (Statlog) : https://archive.ics.uci.edu/dataset/144
- Heart Disease (Cleveland) : https://archive.ics.uci.edu/dataset/45

Usage : python data/download_uci.py
"""

import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

DATASETS = {
    "german_credit.data": "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data",
    "german_credit.doc": "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.doc",
    "heart_cleveland.data": "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data",
    "heart_disease.names": "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/heart-disease.names",
}


def main():
    for name, url in DATASETS.items():
        dest = os.path.join(HERE, name)
        if os.path.exists(dest):
            print(f"déjà présent : {name}")
            continue
        print(f"téléchargement : {url}")
        urllib.request.urlretrieve(url, dest)
        print(f"  -> {dest}")


if __name__ == "__main__":
    main()
