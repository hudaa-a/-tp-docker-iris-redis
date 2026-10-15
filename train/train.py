"""Entraîne un classifieur de fleurs iris et l'enregistre dans un volume."""

import os

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Le volume Docker sera monté ici. Le fichier survit à l'arrêt du conteneur.
MODEL_DIR = os.environ.get("MODEL_DIR", "/model")
MODEL_PATH = os.path.join(MODEL_DIR, "iris_model.joblib")


def main() -> None:
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Precision sur le jeu de test : {accuracy:.3f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "feature_names": list(iris.feature_names),
            "target_names": list(iris.target_names),
        },
        MODEL_PATH,
    )
    print(f"Modele enregistre dans {MODEL_PATH}")


if __name__ == "__main__":
    main()
