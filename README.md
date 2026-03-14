# SensoriPlay E-commerce

E-commerce de brinquedos sensoriais e educativos impressos em 3D.

## Estrutura do Projeto

- `index.html` — Frontend estático com HTML/CSS/JS
- `backend/main.py` — API em FastAPI para produtos, pedidos e cupons
- `db/schema.sql` — Estrutura do banco de dados PostgreSQL
- `security_checklist.md` — Checklist de segurança para backend, banco e infra

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

### Variáveis de ambiente principais

- `DATABASE_URL` — conexão com PostgreSQL (produção)
- `FRONTEND_ORIGINS` — lista de origens permitidas no CORS, separadas por vírgula (ex.: `https://sensoriplay.com.br,https://www.sensoriplay.com.br`)
- `MERCADOPAGO_ACCESS_TOKEN` — token de acesso da API do Mercado Pago (usado no backend, nunca no frontend)
- `MERCADOPAGO_WEBHOOK_TOKEN` — token secreto para proteger o endpoint `/webhook/mercadopago`

## Infraestrutura sugerida

- **Backend**: FastAPI em um droplet da DigitalOcean, Railway, Render ou Oracle Cloud Free Tier
- **Banco de dados**: PostgreSQL (Supabase, Neon ou RDS)
- **Frontend**: GitHub Pages, Vercel ou deploy estático no mesmo servidor do backend

Consulte `security_checklist.md` antes de colocar o projeto em produção para garantir as configurações mínimas de segurança.
