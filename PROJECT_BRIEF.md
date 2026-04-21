# SensoriPlay — Project Brief

**Este documento é a fonte única de verdade para todos os agentes trabalhando no projeto.**
**Consulte SEMPRE antes de fazer qualquer alteração para garantir consistência.**

## Visão do produto
E-commerce de **produtos sensoriais para crianças** — brinquedos que estimulam desenvolvimento sensorial (tato, visão, propriocepção, equilíbrio), voltado a:
- Pais e mães de crianças 0-10 anos
- Famílias com crianças neurodivergentes (autismo, TDAH, TPAC)
- Terapeutas ocupacionais, pediatras, escolas

## Stack (não mudar sem justificar)
- **Frontend:** HTML + CSS + JS vanilla (sem React/Vue)
- **Backend:** FastAPI (Python 3.11+)
- **DB:** SQLite em dev/MVP, PostgreSQL em produção
- **Auth:** JWT (email/senha) + Google OAuth
- **Pagamento:** Mercado Pago
- **Deploy:** systemd user service, porta 8090

## Estado atual
- Local: `/home/claude/sensoriplay/`
- Vitrine + filtros + busca + carrinho: ✅ implementados
- Admin CRUD de produtos: ✅ implementado
- Auth (email/senha + Google): ✅ backend pronto, frontend tem stub
- Cupons: ✅ implementados
- Schema DB: ✅ completo (users, products, coupons, orders, order_items)
- **PENDENTE:**
  - Endpoints de orders (create, list, detail, update status)
  - Integração Mercado Pago (preference + webhook completo)
  - Página de checkout (endereço + frete + confirmação)
  - Melhorias visuais/UX a partir de benchmark
  - Catálogo real de produtos sensoriais

## Identidade visual (PRELIMINAR — pode ser atualizada pelo marketeiro)
- Cores: tons pastéis, acolhedor, seguro
- Logo: `/assets/sensori-play-logo.png`
- Tom: amigável, informativo, cientifico quando necessário (citar estudos em produtos específicos), nunca infantilizar o comprador

## ICP (comprador-alvo)
- **Primary:** mãe ou terapeuta, 25-45 anos, busca presente significativo ou ferramenta terapêutica
- **Secondary:** pai tech-literate comprando brinquedo intencional para filho

## Porta e URL
- Desenvolvimento: `http://142.93.235.6:8090`
- Systemd: `sensoriplay.service`

## Regras de consistência entre agentes
1. **Todas as cores, fontes, copy, e mensagens devem seguir o que estiver documentado aqui** ou em `/home/claude/sensoriplay/BRAND.md` (será criado)
2. **Antes de criar nova página ou componente, verifique se já existe algo similar**
3. **Nomes de produto, categorias e taxonomia** seguem o que o pesquisador definir em `/home/claude/sensoriplay/RESEARCH.md`
4. **Endpoints backend** seguem padrão REST já estabelecido em `backend/main.py`
5. **Nunca alterar schema do DB sem justificativa forte** — usar migrations

## Prioridade atual
1. **P0** — Site no ar e navegável
2. **P1** — Checkout funcional com Mercado Pago
3. **P2** — Pesquisa de mercado + melhorias UX
4. **P3** — Catálogo real de produtos
5. **P4** — SEO, analytics, emails
