# SensoriPlay — Proposta Consolidada Pós-Debate

**Data:** 20/04/2026
**Participantes do debate:** Viabilidade/GTM, Posicionamento/Funil, Arquitetura, Compliance BR, UX/Produto
**Arquivos-fonte:** `/home/claude/sensoriplay/debate/01..05`

---

## 1. Veredito Executivo

**O site NÃO está pronto para receber dinheiro.** Não por um motivo, mas por cinco motivos **acumulados** — qualquer um deles já seria razão para não lançar:

1. **Regulatório** — revender brinquedo sem INMETRO é multa de R$ 100 a R$ 1,5M + apreensão. Responsabilidade solidária.
2. **Técnico** — checkout termina em 404, webhook aceita fraude, oversell garantido em concorrência, HTTP puro.
3. **Comercial** — unit economics fecham por pouco (27% margem), mas só se canal for B2B/TOs — Meta Ads queima capital.
4. **Produto** — fotos de produtos são emojis, CSS tokens quebrados nas páginas internas, filtros não cruzam (quebra o diferencial prometido).
5. **Credibilidade** — social proof fabricado ("Dra. Fernanda M. CREFITO-SP" é risco de fraude), claims terapêuticos são publicidade enganosa.

**Não é para morrer.** É para consertar fundação antes de gastar R$ 1,00 em tráfego.

---

## 2. Consensos Fortes (todos os 5 concordaram)

### 2.1. Checkout está quebrado end-to-end
- Arquiteto: `back_urls` apontam para `checkout-success.html` / `checkout-failed.html` / `checkout-pending.html` — **nenhum existe no projeto**
- Marketeiro: "funil quebrado no ponto mais crítico"
- UX: listou na auditoria heurística

**Ação**: criar as 3 páginas de retorno + testar o fluxo completo com token MP sandbox antes de qualquer anúncio.

### 2.2. Zero social proof real / risco de fraude
- Marketeiro: "Dra. Fernanda M. CREFITO-SP: se é placeholder, é risco real de credibilidade"
- Compliance: claims terapêuticos são Art. 37 CDC + CONAR
- UX: depoimentos editoriais sem plataforma de verificação

**Ação**: remover social proof fabricado AGORA. Substituir por "Cadastre-se para receber nossos primeiros reviews verificados" ou similar, até ter reviews reais.

### 2.3. Gastar em ads agora é queima de capital
- Hunter: CAC Meta Ads R$ 80-160 vs CAC B2B/TO R$ 30-50. LTV/CAC 2,5x vs 20x.
- Marketeiro: "não gastar R$ 1.000 ainda. Pré-requisitos: checkout funcional + pixel + hero reescrito"
- Arquiteto: "aceitar dinheiro antes dos 5 P0s é amadorismo"

**Ação**: **zero tráfego pago** até checklist do próximo item estar 100%.

### 2.4. Fotos reais são não-negociáveis
- UX: "CRITICO-01: emojis no lugar de fotos"
- Hunter: gate obrigatório antes de marketing
- Marketeiro: sem fotos, conversão vai pra zero

**Ação**: fotografar ou obter 5 produtos-âncora reais (cada um com 4-6 ângulos + detalhe + em uso).

---

## 3. Onde os Agentes Divergem

### 3.1. Build vs. Buy (custom vs Nuvemshop)
| Lente | Posição |
|-------|---------|
| Arquiteto | Custom só ganha acima de **R$ 14k GMV/mês**. Abaixo disso SaaS é mais barato. MAS o diferencial "recomendação por perfil sensorial" não existe em SaaS — se implementarmos, custom se justifica. |
| Hunter | Não opinou explicitamente, foca em unit economics que independem |
| UX | Implícito: o custom atual tem 3 críticos — Shopify com tema premium seria superior hoje |
| Compliance | Neutro — impõe requisitos que funcionam nas duas stacks |

**Resolução minha (líder):** manter custom **condicional**. Se em 60 dias não implementarmos o diferencial de recomendação por perfil sensorial, migrar para Nuvemshop. O custo de esperar é menor que o custo de migrar no mês 9 com dívida técnica acumulada.

### 3.2. Quando abrir CNPJ
| Lente | Posição |
|-------|---------|
| Compliance | ME desde o dia 1 (MEI não serve para o ticket/volume projetado) |
| Hunter | CNPJ pode esperar 60-90 dias enquanto valida produto com 1 TO piloto |

**Resolução:** Compliance vence. Abrir ME nas primeiras 2 semanas. Risco de operar informalmente > custo de abrir ME (R$ 200 + contador R$ 150/mês).

### 3.3. Canal primário nos primeiros 90 dias
| Lente | Posição |
|-------|---------|
| Hunter | **B2B/TOs primeiro**. 5 TOs = 60 pedidos/mês sem ads |
| Marketeiro | Funil orgânico + tráfego pago secundário |

**Resolução:** híbrido com prioridade B2B. Mês 1: fechar 2 TOs piloto. Mês 2: conteúdo + SEO. Mês 3: tráfego pago controlado.

---

## 4. Os 5 P0 (impeditivos para lançar)

| # | Bloqueador | Dono | Prazo | Custo |
|---|-----------|------|-------|-------|
| **P0-1** | INMETRO: certificar 5 produtos-âncora OU trocar por linha já certificada | Leo + Compliance | 30-60 dias | R$ 5-12k por modelo — OU trocar por produtos revendidos com INMETRO pronto |
| **P0-2** | Abrir ME + contador + certificado digital A1 | Leo | 15 dias | R$ 500 setup + R$ 150/mês |
| **P0-3** | Consertar checkout: criar 3 back_urls + validar webhook HMAC + implementar lock pessimista no estoque | Dev | 3-5 dias | zero |
| **P0-4** | Remover claims terapêuticos do copy, remover social proof fabricado | Marketing | 1-2 dias | zero |
| **P0-5** | SSL + domínio próprio + nginx reverse proxy | Dev/Infra | 1 dia | R$ 50/ano domínio |

**Estes 5 são sequenciais em termos de risco, não de tempo.** P0-3 e P0-4 dão pra fazer enquanto P0-1 e P0-2 tramitam.

---

## 5. Os 5 P1 (precisam antes de gastar R$ 500 em ads)

| # | Item | Prazo |
|---|------|-------|
| **P1-1** | Fotos reais dos 5 produtos-âncora (4-6 ângulos cada) | 7 dias |
| **P1-2** | Reescrever hero + copy principal — remover metáforas, focar em dor do comprador | 3 dias |
| **P1-3** | Implementar pixel Meta + GA4 + hotjar | 1 dia |
| **P1-4** | Filtros cruzados funcionais (idade + sentido + objetivo simultâneos) — o diferencial prometido | 3-4 dias |
| **P1-5** | Consertar CSS tokens quebrados em `produto.html` e `minha-conta.html` | 2 horas |

---

## 6. Nova Proposta Estratégica

### 6.1 Posicionamento revisado
Adotar proposta do marketeiro:
> **"O brinquedo certo para a fase certa do seu filho. Sem achismo. Sem garimpar. Sem errar."**

Tom: **pragmático, não inspiracional**. Resolve dor, não inspira sentimento.

### 6.2 Diferencial defensável
"Recomendação por perfil sensorial" — sistema de 8 perguntas que recomenda 3-5 produtos específicos para a criança do visitante. **É isso que justifica o custom.** Se não implementarmos, migramos pra Nuvemshop.

### 6.3 Canal primário: B2B/TOs
- Mês 1: fechar 2 TOs parceiros com desconto 15% + comissão R$ 20/indicação + catálogo PDF profissional
- Meta: 30-40 pedidos B2B/mês por TO parceiro
- Custo: contato frio + visita + presente simbólico

### 6.4 Canal secundário: conteúdo + SEO
- 4 artigos/mês respondendo dúvidas reais de mães:
  - "Meu filho acabou de ser diagnosticado com TEA, por onde começar"
  - "Diferença entre brinquedo sensorial e fidget"
  - "Guia: brinquedo por faixa etária 0-10"
  - "INMETRO explicado: como saber se o brinquedo é seguro"
- Target: 6-12 meses para orgânico relevante

### 6.5 Canal terciário (só depois dos P1): Meta Ads controlado
- Budget inicial R$ 500/mês
- Audiência: interesse "autismo", "desenvolvimento infantil", "Maria Montessori"
- Creative: vídeo curto de produto real em uso
- KPI: CAC < R$ 120, pause se passar

---

## 7. Stack técnica: decisão

**Manter custom FastAPI + HTML vanilla**, **com 2 condições**:

1. Implementar o "Recomendador por perfil sensorial" em 60 dias (é o motivo do custom existir)
2. Consertar os 5 P0s técnicos do arquiteto antes de aceitar 1 pagamento real

**Se em 60 dias o Recomendador não estiver ao vivo**, migrar pra **Nuvemshop**:
- Custo: R$ 60/mês + 0,99% das vendas
- Ganha: SSL, CDN, app mobile, integrações logísticas prontas, emissão NF-e integrada
- Perde: liberdade de UX, diferencial técnico

---

## 8. Roadmap 90 dias consolidado

### Mês 1 — Fundação legal + técnica
- [ ] Abrir ME + CNAE 4763-6/01 + contador + certificado digital A1
- [ ] Negociar certificação INMETRO de 5 produtos âncora (ou substituir por linha já certificada)
- [ ] Consertar os 5 P0s técnicos (checkout, webhook HMAC, lock estoque, SSL, backup)
- [ ] Remover claims terapêuticos e social proof fabricado
- [ ] Criar Política de Privacidade + Termos de Uso + canal `privacidade@`
- [ ] Fotos reais dos 5 produtos-âncora

### Mês 2 — Fundação comercial
- [ ] Fechar 2 TOs parceiros (com desconto + comissão)
- [ ] Reescrever hero + PDP + FAQ com copy novo
- [ ] Instalar pixels (Meta + GA4)
- [ ] Implementar filtros cruzados (diferencial prometido)
- [ ] Lançar blog com 4 primeiros artigos
- [ ] 10 pedidos-teste B2B processados end-to-end

### Mês 3 — Tração controlada
- [ ] Implementar Recomendador por perfil sensorial (ou decidir migrar para Nuvemshop)
- [ ] Meta Ads R$ 500/mês — target CAC < R$ 120
- [ ] Expandir catálogo para 30 produtos reais (com INMETRO)
- [ ] Fluxo de review pós-compra com incentivo (cupom 10%)
- [ ] Meta de 50 pedidos/mês no mês 3

---

## 9. Custos iniciais consolidados

### Setup (único)
- Abertura ME + contador primeiro mês: R$ 500
- Certificado digital A1: R$ 200
- Certificação INMETRO (se não substituir produtos): R$ 25-60k para 5 modelos
- Domínio + SSL: R$ 50
- Fotos profissionais (5 produtos): R$ 1.500-3.000
- Plataforma NF-e setup: R$ 300
- **Total setup**: R$ 2.550-66.050 (depende da rota INMETRO)

### Recorrente mensal
- Contador: R$ 150
- Plataforma NF-e: R$ 50-150
- Servidor: R$ 40 (atual OVH) ou migrar pra VPS dedicado R$ 80
- Domínio: R$ 4
- Gateway MP: 4,99% + R$ 0,39 por transação (variável)
- **Total fixo mensal**: R$ 250-350

### Budget marketing (a partir do mês 3)
- Meta Ads: R$ 500-2.000/mês
- Conteúdo: R$ 500/mês se terceirizar
- Newsletter (Mailerlite free até 1k): R$ 0

---

## 10. Decisões que Leo precisa tomar esta semana

1. **INMETRO — certificar próprios ou revender já certificado?** Define se orçamento é R$ 3k ou R$ 40k
2. **Abrir ME agora ou aguardar PoC B2B?** Recomendação: abrir agora
3. **Implementar Recomendador ou migrar pra Nuvemshop em 60 dias?** Define se continua custom
4. **Fotografar produtos ou contratar fotos de banco?** Fotos próprias convertem 2-3x mais
5. **Quem cuida do B2B com TOs?** Esse é o canal #1 e precisa de humano

---

## 11. O que NÃO fazer (do debate)

- ❌ Gastar em Meta Ads antes de checkout funcional + fotos reais + pixels
- ❌ Manter copy com claims terapêuticos diretos (risco CONAR + CDC)
- ❌ Manter social proof fabricado (risco de dano à marca irreparável)
- ❌ Operar sem CNPJ (risco fiscal + Mercado Pago suspende)
- ❌ Manter SQLite em produção sem backup (já fraco em concorrência — catastrófico sem DR)
- ❌ Implementar features antes de conserter os P0s (dívida acumulada)

---

## 12. Saída honesta do debate

**Se as 5 lentes tivessem que votar "seguir o projeto": todas votariam "sim, com reservas".**

Ninguém disse para matar. Mas **ninguém também disse que está pronto**. O projeto tem mérito (nicho real, diferencial defensável possível, mercado em crescimento), mas a execução tem 3 semanas de trabalho duro antes do primeiro anúncio fazer sentido.

O risco não é o projeto falhar. É o projeto **fracassar por motivo evitável** (INMETRO, checkout, claim regulatório) enquanto tinha viabilidade real.

---

**Próximo passo recomendado:** Leo agenda 30 min para revisar este documento e responder as 5 decisões do item 10. Enquanto isso, time executa P0-3, P0-4 e P1-5 (que independem de decisão de negócio).
