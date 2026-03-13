# SensoriPlay E-commerce

E-commerce de brinquedos sensoriais e educativos impressos em 3D.

## Estrutura do Projeto

- `index.html` — Frontend estático com HTML/CSS/JS
- `backend/main.py` — API em FastAPI para produtos, pedidos e cupons
- `db/schema.sql` — Estrutura do banco de dados PostgreSQL

## Banco de Dados

Banco recomendado: **PostgreSQL**.

Criação do banco:

```sql
CREATE DATABASE sensoriplay;
```

Depois execute o conteúdo de `db/schema.sql`.

## Backend (FastAPI)

Requisitos:

```bash
pip install -r backend/requirements.txt
```

Rodar servidor:

```bash
uvicorn backend.main:app --reload
```

## Infraestrutura sugerida

- **Backend**: FastAPI em um droplet da DigitalOcean ou Oracle Cloud Free Tier
- **Banco de dados**: PostgreSQL (Supabase, Neon ou RDS)
- **Frontend**: GitHub Pages, Vercel ou deploy estático no mesmo servidor do backend
