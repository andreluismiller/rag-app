# rag-app

Aplicacao RAG (Retrieval-Augmented Generation) sobre FAQs de programas do MEC.

## Estado atual: Fase 1 -- apenas ingestao no Qdrant

Por ora, o `docker-compose.yml` sobe **somente**:
- **Qdrant** — banco de dados vetorial
- **app** — container de desenvolvimento (Python + `uv`), onde o VS Code / Codespaces se conecta

**Postgres** e **Streamlit** (chat + dashboard) estao com os servicos comentados no
`docker-compose.yml`, prontos para religar quando essa fase comecar (ver
instrucoes dentro do proprio arquivo).

## Estrutura

```
.
├── app/                  # UI Streamlit (fase futura, codigo ja pronto)
├── src/
│   ├── config.py          # Settings via .env (OPENAI_API_KEY agora opcional)
│   ├── ingestion/         # extract -> chunk -> ingest (Qdrant)
│   ├── embeddings/        # embedder.py atual usa OpenAI (fase futura);
│   │                      # sera substituido por FastEmbed (denso+esparso, ONNX)
│   ├── rag/               # retriever, generator (fase futura), pipeline
│   └── evaluation/        # ground truth e metricas
├── data/
│   ├── raw/                # coloque aqui o mec_faq.json
│   ├── processed/
│   └── ground_truth/
├── docker/postgres/init.sql   # fase futura
├── docker-compose.yml     # so qdrant + app ativos
├── Dockerfile
├── pyproject.toml
└── .env.example
```

## Configuracao inicial

1. Copie `.env.example` para `.env`. Para esta fase, os valores padrao de
   `QDRANT_*` ja funcionam — nao e necessario preencher `OPENAI_API_KEY` nem
   os `POSTGRES_*` (ficam comentados).
2. (Recomendado) Gere o lockfile localmente antes do primeiro push:
   ```bash
   uv sync
   ```
3. Suba os servicos:
   ```bash
   docker compose up -d --build
   ```
4. Confira: `docker compose ps` (qdrant deve estar `healthy`, app `running`).
5. Acesse o painel do Qdrant em `http://localhost:6333/dashboard`.

## Reativando Postgres/Streamlit (fase futura)

Edite `docker-compose.yml`: descomente os servicos `postgres` e `streamlit` e
a linha `postgres_data` em `volumes`; descomente as variaveis `POSTGRES_*`
no `.env`. Depois `docker compose up -d --build`.

## Comandos uteis

| Comando         | Descricao                                        |
|-----------------|---------------------------------------------------|
| `make up`       | Sobe os servicos ativos em background              |
| `make down`     | Derruba os servicos                                |
| `make build`    | Rebuild da imagem do container `app`               |
| `make logs`     | Segue os logs de todos os servicos                 |
| `make shell`    | Abre um shell dentro do container `app`            |
| `make ingest`   | Roda a ingestao (`src/ingestion/ingest.py`)        |
| `uv add <pkg>`  | Adiciona uma dependencia ao projeto                |
| `make fmt`      | Formata o codigo com ruff                          |
| `make lint`     | Roda o linter (ruff)                               |
