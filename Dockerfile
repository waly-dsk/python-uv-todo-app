# ---- Étape 1 : Builder ----
# On installe les dépendances et on prépare l'application
FROM python:3.12-slim AS builder

# On récupère l'outil "uv" (gestionnaire de dépendances) depuis son image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# On copie d'abord les fichiers de dépendances seulement
# (permet à Docker de mettre en cache cette étape si le code change mais pas les dépendances)
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

# On copie maintenant le reste du code de l'application
COPY main.py db.py ./
COPY static/ ./static/


# ---- Étape 2 : Image finale ----
# Image plus légère, sans les outils de build
FROM python:3.12-slim AS final

WORKDIR /app

# On récupère uniquement ce qui a été préparé dans l'étape précédente
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/db.py /app/db.py
COPY --from=builder /app/static /app/static

# Le port sur lequel l'application écoute
EXPOSE 8000

# La commande qui démarre l'application
CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
