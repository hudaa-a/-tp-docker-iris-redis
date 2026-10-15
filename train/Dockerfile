# Version optimisee.
# - image slim : python:3.11-slim, sans les outils de compilation de l'image complete
# - multi-etapes : l'etape builder installe les dependances, l'image finale ne garde que le resultat
# - reordonnancement : requirements.txt est copie et installe avant train.py,
#   donc un changement de code ne relance pas pip
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

# scikit-learn a besoin de libgomp au demarrage (OpenMP).
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /install /usr/local
# Corrige deux vulnerabilites HIGH signalees par Trivy :
# wheel CVE-2026-24049 et jaraco.context CVE-2026-23949.
RUN pip install --no-cache-dir --upgrade "wheel>=0.46.2" "jaraco.context==6.1.0" "setuptools==84.0.0"
COPY train.py .

# Au demarrage du conteneur, on entraine et on ecrit le modele dans /model.
CMD ["python", "train.py"]
