# Version optimisee, meme principe que l'entrainement.
# L'image finale charge le modele deja present dans /model, elle ne l'entraine pas.
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
# pip 24.0 de l'image de base refuse parfois un telechargement
# en le signalant comme un hash incorrect. On le met a jour d'abord.
RUN pip install --no-cache-dir --upgrade "pip==26.2.1" \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /install /usr/local
# Corrige deux vulnerabilites HIGH signalees par Trivy :
# wheel CVE-2026-24049 et jaraco.context CVE-2026-23949.
RUN pip install --no-cache-dir --upgrade "wheel>=0.46.2" "jaraco.context==6.1.0" "setuptools==84.0.0"
COPY predict.py .
COPY api.py .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
