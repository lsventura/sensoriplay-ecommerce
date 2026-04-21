# Debate SensoriPlay — Lente Arquitetura Técnica
**Auditor:** Arquiteto Sênior  
**Data:** 2026-04-19  
**Metodologia:** Código lido linha a linha, banco inspecionado, endpoints testados via curl, carga simulada com 10 requisições concorrentes.

---

## Veredicto executivo

O sistema tem uma base técnica sólida para MVP — melhor do que a maioria dos projetos nesta fase. Mas há **cinco riscos reais** que precisam ser resolvidos antes do primeiro pedido real, e uma decisão arquitetural crítica que está sendo adiada (SQLite vs PostgreSQL). O resto é dívida técnica gerenciável.

---

## 1. Stack escolhida está certa?

### Diagnóstico honesto

FastAPI + HTML vanilla + SQLite é uma escolha **defensável para MVP**, mas com ressalvas sérias.

**O que está certo:**
- FastAPI é genuinamente bom: validação de entrada via Pydantic, tipos, async, documentação automática. Não é over-engineering para este caso.
- HTML vanilla sem bundler elimina toda uma categoria de complexidade de build. Para um time sem frontend dedicado, a escolha é pragmática.
- Design system com CSS tokens (`design-tokens.css`) é o padrão correto — evita o caos de "style soup" que todo e-commerce vanilla sofre.

**O que está errado:**
- O site está **rodando na porta 8090 direto do servidor dos bots de cripto**. Um único servidor, sem separação de ambientes, sem proxy reverso (Nginx/Caddy), sem SSL. Se o crypto-bot tiver pico de CPU, o e-commerce fica lento. Se o e-commerce cair, arrasta o processo junto.
- SQLite em produção para e-commerce é um erro categórico. Mais sobre isso abaixo.

**Quando a stack quebra:**
- Estoque: 2 usuários adicionam o último item ao carrinho simultaneamente. SQLite não tem `SELECT FOR UPDATE`. Verificado no código: não existe nenhuma linha com `with_for_update()` ou `SERIALIZABLE`. O primeiro `db.commit()` ganha, o segundo comete oversell silencioso.
- Leitura: SQLite permite N leitores concorrentes mas **1 escritor exclusivo com lock de arquivo**. Em pico de Black Friday com pedidos sendo criados, o webhook do Mercado Pago batendo e admin atualizando status ao mesmo tempo: timeout ou `database is locked` garantido.
- Escala: FastAPI com Uvicorn em single process aguenta ~200-500 req/s em leitura pura. Para o volume real de um e-commerce de nicho no primeiro ano (estimativa: 1.000-5.000 pedidos/mês, picos de 50 req/s), **a stack aguenta**. O SQLite é o gargalo, não o Python.

**Comparação com alternativas (números reais):**

| Opção | Custo mensal | Tempo pra vender | Integração logística | Customização |
|---|---|---|---|---|
| Stack atual (self-hosted) | ~R$100 VPS | 4-8 semanas | Manual | Total |
| Nuvemshop | R$60 + 0,99% | 1-2 dias | Correios/Jadlog nativos | Limitada |
| Loja Integrada | R$0 até R$50k/mês | 1-2 dias | Nativos | Limitada |
| Shopify | USD 29/mês (~R$165) | 2-3 dias | Apps de terceiros | Moderada |

**Quando o custom faz sentido:**
1. Você tem lógica de negócio que plataformas SaaS não suportam (ex: recomendação baseada em perfil sensorial, assinatura recorrente de kits terapêuticos).
2. Você quer integração com sistemas proprietários (prontuário terapêutico, ERP clínica).
3. Você projeta crescimento para >R$1M/ano onde 0,99% de transação = R$10k/mês de custo.
4. Você tem time técnico para manter.

Para **validar o mercado** com os primeiros 100-500 pedidos, Nuvemshop ou Loja Integrada ganham em velocidade. Para construir o produto diferenciado de longo prazo (recomendação inteligente por perfil sensorial, área do terapeuta), o custom faz sentido — mas a fundação técnica precisa ser mais sólida.

**Minha recomendação:** Manter o custom, mas resolver os cinco riscos abaixo antes de aceitar dinheiro real. A stack não é o problema; a infraestrutura ao redor é.

---

## 2. Banco de dados

### SQLite em produção: Não

Verificado empiricamente:

```
journal_mode: delete  # NÃO é WAL — modo mais lento e menos concorrente
```

SQLite no modo `delete` (padrão) usa lock exclusivo por transação de escrita. Qualquer `INSERT` de pedido bloqueia toda leitura simultânea. Para `create_order` (que faz `db.flush()` + múltiplos `db.add()` + `db.commit()`), a janela de lock é de 50-200ms. Com 5 pedidos simultâneos: fila de espera visível.

**O problema maior é o oversell.** O fluxo atual de criação de pedido:
1. `SELECT stock FROM products WHERE id = X` — lê estoque
2. Valida se `stock >= qty` 
3. `UPDATE products SET stock = stock - qty` — decrementa

Entre o passo 1 e o passo 3, outro request pode ler o mesmo estoque e passar na validação. Sem `SELECT FOR UPDATE` (indisponível em SQLite), isso é uma condição de corrida garantida para qualquer produto com estoque baixo.

**Schema: bem feito, com ressalvas**

Positivo:
- `product_name_snapshot` em `order_items` — correto, preserva histórico de preço do produto no momento da compra.
- Foreign keys com `ON DELETE CASCADE` em `order_items`.
- Índices criados em `schema.sql` para category, featured, user_id, status.

Problemas reais:
- `shipping_address` armazenado como `TEXT` com JSON serializado. Não há validação de schema no banco. Uma corrupção silenciosa (ex: JSON malformado salvo por bug) produz `None` no `_order_to_out()` sem erro — pedido existe mas endereço some.
- `status` em `orders` é `VARCHAR(30)` sem `CHECK constraint`. Nada impede inserir `status='banana'` diretamente no banco. O enum está apenas no Python.
- Sem `updated_at` automático via trigger/DEFAULT: depende do código Python sempre setar `updated_at=datetime.utcnow()`. Um bug no código produz timestamps incorretos silenciosamente.
- Sem índice em `order_items.product_id` — para relatórios de "produtos mais vendidos" isso vira full scan.
- Sem índice em `products.stock` — para alertas de "estoque crítico" no admin, full scan.

**Migração para PostgreSQL: esforço real**

O código já usa SQLAlchemy ORM com tipos portáveis. A migração é:
1. Provisionar PostgreSQL (Railway/Render: R$25-50/mês, ou DO Managed: USD 15/mês).
2. Trocar `DATABASE_URL` de `sqlite:///...` para `postgresql://...`.
3. Rodar `CREATE TABLE` do `schema.sql` no PostgreSQL — já existe e está correto.
4. Migrar dados: `INSERT INTO ... SELECT ...` ou pg_dump. Com 18 produtos e 0 pedidos reais, isso é 10 minutos de trabalho.
5. Ativar `SELECT FOR UPDATE` no fluxo de `create_order` — 3 linhas de código.

Downtime esperado: 15-30 minutos. Risco baixo.

**Backup:** Não existe nenhum script de backup do `sensoriplay.db`. O arquivo tem 76KB agora. Se o disco falhar ou o servidor for reiniciado com erro, dados de usuários e produtos somem.

---

## 3. Auth e segurança

### Problemas encontrados, do mais grave ao menos grave

**P0 — CORS + credentials em modo dev aberto**

No `.env` atual, `FRONTEND_ORIGINS` está configurado (correto: `http://142.93.235.6:8090`). Mas o código tem fallback perigoso: se `FRONTEND_ORIGINS` não for definida em produção, o valor vira `["*"]` com `allow_credentials=True`. Segundo a especificação CORS (RFC 6454), browsers **bloqueiam** requisições com credenciais quando `allow_origins=["*"]` — mas isso não é o problema. O problema é que sem `FRONTEND_ORIGINS`, qualquer origem pode consumir a API sem restrição de origem (a menos que o browser bloqueie, o que ele bloqueia para cookies, mas não para Bearer tokens no header Authorization). Se o deploy em Railway/Render esquecer de setar a variável, a API fica aberta.

**P0 — Webhook do Mercado Pago sem validação de assinatura real**

O webhook valida apenas um `?token=` como query parameter. O Mercado Pago (documentação v2) envia um header `x-signature` com HMAC-SHA256 do corpo. O código atual **não valida esse header**. Qualquer pessoa que descubra a URL do webhook (ou que faça brute-force do token) pode fabricar notificações de "pagamento aprovado" e liberar pedidos sem pagar.

O código faz a chamada de volta à API do MP para confirmar o status — isso mitiga parcialmente. Mas o fluxo ainda aceita o `resource_id` da notificação forjada e faz uma consulta ao MP com ele. Se o atacante tiver um `resource_id` de um pagamento real (qualquer transação MP), pode redirecionar a aprovação para um pedido arbitrário.

**P1 — JWT com `is_admin` no payload, não verificado no banco**

```python
access_token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
```

O claim `is_admin` está no JWT. Quando o token chega no `get_current_admin`, o código faz:

```python
async def get_current_admin(current_user: database.User = Depends(get_current_user)):
    if not current_user.is_admin:
```

Aqui `current_user` foi recarregado do banco via `get_current_user` — isso está correto, valida contra o DB. Mas se o admin for revogado (`is_admin = False` no banco), o token existente ainda funciona até expirar (padrão: 1440 minutos = 24 horas). Sem blacklist de tokens, não há como revogar um admin imediatamente.

**P1 — JWT expira em 24 horas (1440 minutos)**

Configurado no `.env`. Para token de admin, 24 horas é excessivo. Se o token vazar, o atacante tem janela de até 24 horas. Recomendado: 15-60 minutos para usuário comum, com refresh token; ou 4 horas máximo.

**P1 — Sem política de força de senha**

```python
class UserCreate(BaseModel):
    password: str  # sem validação, sem comprimento mínimo
```

Aceita `password="1"`. Nenhuma verificação de comprimento mínimo, complexidade ou lista de senhas comuns.

**P2 — Sem 2FA, sem reset de senha**

Reset de senha por email: não implementado. Usuário esqueceu a senha do Google OAuth? Sem saída. Usuário cadastrado por email/senha: sem recuperação.

**P2 — Sem CSRF protection**

A aplicação usa Bearer token em `Authorization` header (não cookies), então CSRF clássico não se aplica. Mas o admin panel usa `localStorage` para o token — XSS em qualquer página lê o token diretamente. Sem Content Security Policy (CSP) header configurado no Uvicorn.

**P2 — Sem audit log para ações admin**

Admin pode deletar produto, cancelar pedido, mudar status. Nenhuma dessas ações é logada com "quem fez, quando, de qual IP". Para um e-commerce com questões de contestação de chargeback, isso é necessário.

---

## 4. Pagamento

### Mercado Pago: arquitetura correta, implementação com gaps

A escolha de MP via Preference (Checkout Pro) é a forma padrão e correta para BR. PIX nativo exigiria integração mais complexa (QR code, webhook diferente). Pagar.me é alternativa válida mas tem curva de integração maior. Stripe não é recomendado para BR (sem PIX nativo, taxas maiores).

**O que está certo:**
- O código consulta a API do MP para confirmar o status antes de marcar pedido como pago — correto, não confia cegamente na notificação.
- Estorno de estoque em cancelamento/falha está implementado.
- `external_reference` corretamente mapeado para `order.id`.
- Desconto do cupom repassado ao MP via ajuste proporcional de preços (workaround funcional para o MP não aceitar item com valor negativo).

**O que está errado:**

1. **Idempotência parcial:** O webhook processa a notificação somente se `new_status != old_status`. Isso evita processamento duplo para o mesmo status, mas não para múltiplas notificações do mesmo evento com status diferente chegando fora de ordem (MP pode reenviar). Não há log de quais `resource_id`s já foram processados.

2. **Sem validação de assinatura HMAC** (já citado em segurança — P0).

3. **Sem cron de reconciliação:** Se o webhook falhar (servidor fora do ar, timeout), o pedido fica preso em `pending` para sempre. Não há job que varra pedidos com mais de X horas em `pending` e consulte o MP para atualizar o status.

4. **`back_urls` apontam para páginas que não existem:** O código referencia `checkout-success.html`, `checkout-failed.html`, `checkout-pending.html` em `/pages/`. Nenhum desses arquivos existe no projeto. O usuário depois do pagamento seria redirecionado para 404.

5. **Frete hardcoded via variável de ambiente:** R$19,90 fixo para todo o Brasil, frete grátis acima de R$199. Sem integração com Correios/Jadlog para calcular frete real por CEP e peso. Para produtos físicos, isso é inadequado — um produto de R$45 enviado de SP para AM pode custar R$40 de frete, mas o sistema cobra R$19,90.

---

## 5. Frontend

### Hybrid MPA/SPA não declarado

O site não é claramente MPA (Multi-Page Application) nem SPA (Single Page Application). É um híbrido:
- Cada URL é uma página HTML separada (MPA)
- Mas o estado (carrinho, token de auth, cupom) vive em `localStorage` e é reconstituído em JS em cada página (comportamento SPA)
- A navegação é `<a href>` tradicional (MPA)

Isso é funcional, mas cria problemas:

**localStorage para carrinho:** Verificado no código — o carrinho é salvo como JSON em `localStorage.getItem('sensori_cart')`. Problemas conhecidos:
- Não sincroniza entre dispositivos (usuário adiciona no celular, não aparece no desktop)
- Não valida estoque ao carregar (produto pode ter ficado sem estoque enquanto o item estava no carrinho)
- Sem expiração — carrinho de 30 dias atrás ainda aparece
- Se dois abas do mesmo browser modificam o carrinho simultaneamente, a segunda sobrescreve a primeira

**JWT em localStorage:** O token de autenticação está em `localStorage` (confirmado: `localStorage.getItem('sensori_token')`). Isso é vulnerável a XSS. O padrão mais seguro é `httpOnly cookie`, que JavaScript não consegue ler. Com XSS em qualquer parte do site, o atacante lê o token e autentica como o usuário.

**SEO:** O site renderiza produtos via JavaScript (`fetch('/products').then(...)`). Googlebot indexa JavaScript, mas com delay de dias a semanas. Para um e-commerce de nicho onde SEO orgânico é crítico (pesquisa "brinquedo sensorial autismo"), ter os produtos no HTML estático seria muito melhor. Com a stack atual, o Google vê uma página em branco na primeira passagem.

**Tamanho dos assets sem compressão:**
- `index.html`: 66,5KB (sem gzip)
- `components.css`: 32,7KB  
- `base.css`: 13,9KB
- Total primeiro load: ~187KB de texto (sem imagens, sem fontes Google)
- **Sem GZipMiddleware no FastAPI** — confirmado no código. Com gzip, esse payload reduz para ~56KB.

A correção é uma linha: `from fastapi.middleware.gzip import GZipMiddleware; app.add_middleware(GZipMiddleware)`.

---

## 6. Performance

**Medições reais (servidor local, sem rede):**

```
GET /           → 200 OK, 3.3ms, 68.1KB (sem gzip)
GET /products   → 200 OK, 5.2ms, 9.9KB
10 req paralelas → 13ms-39ms, todos 200 OK
```

O servidor responde rápido localmente. Mas há dois problemas para usuário real:

1. **Sem CDN:** CSS, JS e logo passam pelo servidor Python em DigitalOcean Amsterdam. Para usuário em SP, latência de ida-e-volta de 200-250ms por recurso. Com 4-5 assets por página, o primeiro load leva 1-1,5s só de latência de rede antes de renderizar.

2. **Google Fonts bloqueante:** `<link href="https://fonts.googleapis.com">` está no `<head>` sem `font-display: swap`. Isso bloqueia renderização até as fontes carregarem. Em conexão lenta (3G), pode adicionar 1-3s ao First Contentful Paint.

3. **Imagens como emojis:** Tecnicamente zero-byte, mas quando produtos reais forem cadastrados sem campo de imagem, a loja vai parecer não-profissional. Não há campo `image_url` no schema atual.

---

## 7. DevOps e Infra

**Deploy atual: risco operacional alto**

O serviço roda como `systemd --user` no mesmo servidor do crypto-bot. Problemas:

- **Sem Nginx/Caddy na frente:** Uvicorn está exposto diretamente na porta 8090. Sem proxy reverso, não há: SSL/HTTPS, compressão, rate limiting por IP na camada HTTP, buffer de requests, cache de assets estáticos. FastAPI servindo arquivos estáticos via `StaticFiles` é funcional mas ~10x mais lento que Nginx para assets.
- **Sem SSL:** Todo tráfego em HTTP. Dados de cadastro (nome, email, senha), token JWT, endereço de entrega — trafegam em texto puro. Em 2026, browser vai marcar como "Not Secure" e usuários vão desconfiar.
- **Sem domínio:** `http://142.93.235.6:8090` não é endereço de loja. Google não indexa bem IPs. Usuário não vai comprar de IP nu.
- **Single point of failure:** 1 servidor = 1 ponto de falha. Se o servidor cair, loja e bots caem juntos.
- **Sem monitoramento de uptime:** O log existe (`logs/sensoriplay.log`) mas não há alerta. Se o processo morrer às 3h, Leo descobre pela manhã.
- **Dockerfile quebrado:** O Dockerfile copia apenas `backend/`, não copia `assets/`, `pages/`, `admin/`, `auth/` ou `index.html`. Se alguém tentar fazer build da imagem Docker, o servidor sobe sem frontend. A porta exposta é 8000, mas o systemd usa 8090. O `CMD` executa `main:app` mas o entrypoint real é `server:app`. Três inconsistências em 14 linhas.

**Custo atual:** Compartilhando VPS com crypto-bot — custo incremental perto de zero. Mas o risco de interferência entre serviços é real.

---

## 8. Dívida técnica — inventário completo

| ID | Descrição | Severidade | Impacto se não resolvido |
|---|---|---|---|
| DT-01 | SQLite sem WAL mode, sem SELECT FOR UPDATE | P0 | Oversell garantido em pico |
| DT-02 | Webhook MP sem validação HMAC do header x-signature | P0 | Pedidos aprovados fraudulentamente |
| DT-03 | Páginas checkout-success/failed/pending inexistentes | P0 | Usuário em 404 após pagar |
| DT-04 | Sem SSL/HTTPS | P0 | Dados sensíveis em texto puro, browser marca "inseguro" |
| DT-05 | Sem backup do banco | P0 | Perda total de dados se servidor falhar |
| DT-06 | Frete fixo sem cálculo por CEP/peso | P1 | Margem negativa em envios para longe |
| DT-07 | JWT em localStorage (XSS leaks token) | P1 | Sequestro de sessão via XSS |
| DT-08 | Sem política de força de senha | P1 | Senhas triviais ("123456") aceitas |
| DT-09 | Sem reset de senha | P1 | Usuários bloqueados permanentemente |
| DT-10 | Sem cron de reconciliação de pagamentos | P1 | Pedidos presos em "pending" para sempre |
| DT-11 | GZipMiddleware ausente | P1 | 187KB de texto sem compressão por página |
| DT-12 | Dockerfile não copia frontend | P1 | Build Docker não funciona |
| DT-13 | Produtos sem campo image_url no schema | P1 | Loja de emojis em produção |
| DT-14 | CORS fallback para `["*"]` se ENV não configurada | P1 | API aberta sem origem em deploy descuidado |
| DT-15 | Sem domínio próprio | P1 | Não indexável, não profissional |
| DT-16 | Sem Nginx/proxy reverso | P1 | Uvicorn exposto, sem buffer, sem cache |
| DT-17 | Carrinho em localStorage sem expiração ou validação de estoque | P2 | Carrinho desatualizado, falha na compra |
| DT-18 | Sem audit log de ações admin | P2 | Sem rastreabilidade para disputas |
| DT-19 | Token admin expira em 24h sem revogação | P2 | Janela longa para token comprometido |
| DT-20 | Produtos renderizados via JS (SEO prejudicado) | P2 | Google indexa HTML vazio |
| DT-21 | Sem Google Fonts `font-display: swap` | P2 | Bloqueio de renderização em conexão lenta |
| DT-22 | Sem testes automatizados | P2 | Regressões silenciosas a cada mudança |
| DT-23 | CSS inline em cada página HTML além do design system | P2 | Tokens duplicados, divergências visuais |
| DT-24 | Sem 2FA para admin | P2 | Admin com senha fraca = comprometimento total |
| DT-25 | Status de pedido sem CHECK constraint no banco | P2 | Estados inválidos possíveis via SQL direto |
| DT-26 | Sem alerta de erro em tempo real | P2 | Falhas silenciosas descobertas tarde |
| DT-27 | Sem índice em order_items.product_id | P3 | Relatórios lentos com volume |
| DT-28 | Sem CI/CD pipeline | P3 | Deploy manual = risco de erro humano |
| DT-29 | Sem integração logística (Correios/Jadlog) | P3 | Tracking manual de envios |
| DT-30 | Cupons sem UI de admin | P3 | Criação de cupons só via SQL direto |

---

## 9. Comparação honesta: build vs. buy

**Quando usar Nuvemshop/Loja Integrada:**
- Objetivo é vender nos próximos 30 dias
- Produto ainda está sendo validado (menos de 200 pedidos/mês)
- Time não tem capacidade de manter infraestrutura
- Integração com Correios, Jadlog, emissão de nota fiscal são prioridade

**Quando manter o custom:**
- Produto tem diferencial que plataformas não suportam: recomendação por perfil sensorial, área do terapeuta, assinatura de kit mensal curado
- Previsão de crescimento que justifica evitar taxa de 0,99% (acima de ~R$300k/mês a taxa do MP via Nuvemshop supera o custo de manutenção de dev)
- Já existe investimento técnico e o time sabe manter

**Análise de custo para SensoriPlay especificamente:**

Se a loja fizer R$20k/mês (meta conservadora mês 6):
- Nuvemshop Turbo (R$139/mês): R$139 + 0,99% × R$20.000 = R$139 + R$198 = **R$337/mês**
- Stack custom (VPS dedicada R$200 + PostgreSQL R$75): **R$275/mês** + custo de manutenção de dev

Em R$20k/mês, os custos são equivalentes. O break-even está por volta de R$14k/mês. Abaixo disso, Nuvemshop é mais barata. Acima de R$100k/mês, o custom ganha claramente.

**Para a SensoriPlay hoje:** O diferencial de recomendação por perfil sensorial é real e não existe em plataforma SaaS. Manter o custom faz sentido — mas resolver os P0s antes de vender.

---

## 10. Checklist técnico para ir ao ar

Ordenado por criticidade. P0 = não lançar sem isso.

### P0 — Bloqueadores de lançamento

- [ ] **SSL + domínio próprio** — Registrar domínio (R$40/ano Registro.br), configurar Caddy ou Certbot para HTTPS automático. Tempo: 2h.
- [ ] **Nginx ou Caddy como proxy reverso** — Terminar SSL, servir assets estáticos, compressão gzip. Tempo: 2h.
- [ ] **Criar páginas checkout-success, checkout-failed, checkout-pending** — O fluxo de pagamento redireciona para elas e elas não existem. Sem isso, usuário cai em 404 após pagar.
- [ ] **Migrar para PostgreSQL** — Provisionar banco gerenciado (Railway, Render ou DO), atualizar DATABASE_URL, rodar schema, migrar dados (18 produtos, 1 usuário). Tempo: 3h.
- [ ] **Implementar SELECT FOR UPDATE no create_order** — 3 linhas de código, resolve oversell.
- [ ] **Backup automático do banco** — Script cron que exporta dump diário para S3 ou Backblaze B2. Tempo: 1h.
- [ ] **Validar assinatura HMAC do webhook MP** — Ler header `x-signature`, validar contra `MERCADOPAGO_WEBHOOK_SECRET`. Tempo: 2h.
- [ ] **Configurar MERCADOPAGO_ACCESS_TOKEN real** — Hoje está vazio no .env. Sem isso, nenhum pagamento funciona.

### P1 — Necessário para operação confiável

- [ ] **GZipMiddleware** — Uma linha de código, reduz payload em 70%.
- [ ] **Frete por CEP** — Integrar API dos Correios ou Melhor Envio para cálculo real. Sem isso, frete fixo vai gerar reclamação ou prejuízo.
- [ ] **Reset de senha por email** — Envio de link com token temporário. Serviço: SendGrid (grátis até 100 emails/dia) ou Amazon SES (USD 0,10/mil emails).
- [ ] **Campo image_url no schema** — Migration simples: `ALTER TABLE products ADD COLUMN image_url TEXT`. Upload de imagem: Cloudflare R2 (grátis até 10GB) ou S3.
- [ ] **Política de força de senha mínima** — `len(password) >= 8` no Pydantic validator. Tempo: 10 minutos.
- [ ] **Cron de reconciliação de pagamentos** — Varrer pedidos em `pending` com mais de 2 horas e consultar API do MP. Tempo: 3h.
- [ ] **Monitoramento de uptime** — Healthcheck.io ou UptimeRobot (gratuito) pinga `/health` a cada 5 minutos e alerta no Telegram.

### P2 — Qualidade e crescimento

- [ ] **Google Fonts com font-display: swap** — CSS change, 10 minutos.
- [ ] **CSP header** — Configurar no Nginx/Caddy para mitigar XSS.
- [ ] **Audit log de ações admin** — Tabela `admin_actions` com user_id, action, entity_id, old_value, new_value, ip, timestamp.
- [ ] **Cupons com UI de admin** — Hoje só via SQL direto.
- [ ] **Pre-rendering ou SSR para SEO** — Alternativa mais simples: gerar HTML estático do catálogo via script e servir como fallback.
- [ ] **Testes de integração para o fluxo de checkout** — pytest + httpx, cobrir create_order → pay → webhook → status paid.

### Compliance

- [ ] **Política de Privacidade e LGPD** — Página obrigatória antes de coletar dados pessoais.
- [ ] **Termos de Uso** — Necessário para o Mercado Pago e para disputas de chargeback.
- [ ] **Nota fiscal eletrônica** — NFe para cada pedido. Integração com Enotas, NFe.io ou similar. Obrigatório por lei para pessoa jurídica vendendo produtos físicos.
- [ ] **Política de troca e devolução** — Página existe (`trocas.html`) mas precisa estar de acordo com o CDC (7 dias para desistência em compra online).

---

## Resumo de prioridades

**Hoje (antes de aceitar qualquer pagamento):**  
DT-01 (oversell), DT-02 (fraude webhook), DT-03 (404 pós-pagamento), DT-04 (sem SSL), DT-05 (sem backup) + configurar o token real do MP.

**Semana 1:**  
Domínio, Nginx, PostgreSQL, frete por CEP, páginas de retorno do MP.

**Mês 1:**  
Reset de senha, imagens de produtos, monitoramento, cron de reconciliação, nota fiscal.

**Mês 2+:**  
SEO, testes, audit log, 2FA para admin, pré-renderização de catálogo.
