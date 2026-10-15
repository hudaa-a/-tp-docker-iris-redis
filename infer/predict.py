"""Charge le modele iris enregistre dans le volume et predit une espece."""

import os
import sys

import joblib

MODEL_PATH = os.environ.get("MODEL_PATH", "/model/iris_model.joblib")

# Exemple classique : une iris setosa (longueurs et largeurs en cm).
DEFAULT_SAMPLE = [5.1, 3.5, 1.4, 0.2]


def read_sample() -> list[float]:
    if len(sys.argv) == 1:
        return DEFAULT_SAMPLE
    if len(sys.argv) != 5:
        print(
            "Usage : python predict.py "
            "[longueur_sepale largeur_sepale longueur_petale largeur_petale]"
        )
        sys.exit(1)
    return [float(value) for value in sys.argv[1:5]]


def main() -> None:
    if not os.path.isfile(MODEL_PATH):
        print(f"Modele introuvable : {MODEL_PATH}")
        print("Lance d'abord le conteneur d'entrainement avec le volume iris-models.")
        sys.exit(1)

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    feature_names = bundle["feature_names"]
    target_names = bundle["target_names"]

    sample = read_sample()
    prediction = int(model.predict([sample])[0])
    species = target_names[prediction]

    print(f"Modele charge depuis {MODEL_PATH}")
    for name, value in zip(feature_names, sample):
        print(f"  {name} : {value}")
    print(f"Espece predite : {species}")


if __name__ == "__main__":
    main()
