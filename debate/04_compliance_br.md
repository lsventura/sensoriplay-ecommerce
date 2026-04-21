# SensoriPlay — Debate 04: Compliance legal, operacional e fiscal BR

> **Autor**: agente Compliance BR (Atlas Team)
> **Data**: 2026-04-19
> **Escopo**: análise rigorosa e prática do que é exigido para abrir, operar e vender produtos sensoriais infantis no Brasil em 2026, com foco em brinquedos certificados, ecommerce próprio e produtos com apelo terapêutico.
> **Premissa crítica**: o site em produção (http://142.93.235.6:8090) hoje NÃO está apto a vender legalmente. Este documento é o mapa para regularização.

---

## Sumário executivo — o veredito duro

O SensoriPlay, do jeito que está hoje, acumula pelo menos **7 riscos legais simultâneos** que podem inviabilizar o negócio na primeira notificação de IPEM, Procon, ANPD ou Ministério Público. Os dois maiores, em ordem de gravidade:

1. **Revenda de brinquedos sem certificação INMETRO** (Portaria 563/2016 + Portaria 302/2021): multa de **R$ 100 a R$ 1,5 milhão**, apreensão de mercadoria, responsabilidade solidária do varejista mesmo comprando de distribuidor nacional. Isso é o **kill switch regulatório** do nicho.
2. **Claims terapêuticos** ("ajuda no autismo/TDAH") sem respaldo como dispositivo médico ANVISA: sujeito a publicidade enganosa/abusiva (Art. 37 CDC + Art. 39 CDC + Seção 11 Código CONAR), ação do MP e Procon.

A boa notícia: nada disso é caro ou demorado de resolver — é questão de **sequência correta**. O roteiro priorizado está na Parte 4.

---

## Parte 1 — Checklist do MÍNIMO LEGAL para ir ao ar

### 🔴 IMPEDITIVO — não pode vender sem (bloqueio total)

| # | Item | Base legal | Motivo |
|---|------|-----------|--------|
| 1 | **CNPJ ativo com CNAE de comércio varejista** | Código Comercial + LC 123/2006 | Venda recorrente com ânimo de lucro = atividade empresarial; sem CNPJ, MP + Receita podem autuar |
| 2 | **Certificado INMETRO válido em TODOS os brinquedos** destinados a menores de 14 anos | Port. 563/2016 + Port. 302/2021 INMETRO | Sem cert → apreensão + multa R$100 a R$1,5M pelo IPEM estadual |
| 3 | **Nota fiscal eletrônica (NF-e) em cada venda** | RICMS estadual + LC 87/96 | Venda sem NF = sonegação; em SP, NFC-e obrigatória desde jan/2026 |
| 4 | **Dados da empresa visíveis no site**: razão social, CNPJ, endereço físico, email e telefone | Art. 33 Decreto 7.962/2013 (marco ecommerce) | Decreto específico de comércio eletrônico — fiscalização Procon |
| 5 | **Política de trocas e devoluções + direito de arrependimento 7 dias explícito** | Art. 49 CDC (Lei 8.078/90) + Dec. 7.962/2013 | Direito de arrependimento NÃO é opcional; tem que estar comunicado antes da compra |
| 6 | **Política de Privacidade + base legal de tratamento de dados** | Arts. 6º, 9º e 18 LGPD (Lei 13.709/18) | Site sem política = violação clara; ANPD já aplica multa (Art. 52) |
| 7 | **Termos de Uso** | Código Civil Art. 421 + CDC | Contrato entre lojista e consumidor; sem termo explícito = tudo sob CDC na interpretação mais pró-consumidor |
| 8 | **Preço total antes de finalizar + discriminação de frete/juros** | Art. 6º V CDC + Art. 2º Dec. 5.903/2006 | "Preço visível" é infração Procon — multa diária em caso extremo |
| 9 | **Canal de atendimento acessível e funcional** (email + 1 outro: WhatsApp/formulário) | Dec. 11.034/2022 (novo SAC) + Art. 4º CDC | Resposta obrigatória em até 7 dias corridos |
| 10 | **Rotulagem e marcação INMETRO nas embalagens** | Port. 563/2016 Anexo II | Deve constar: selo conformidade, faixa etária, advertências, fabricante, CNPJ importador |

### 🟡 DESEJÁVEL — melhora credibilidade, reduz risco, evita problema futuro

- **Cookie banner** (analytics/Google = tratamento de dados → consentimento LGPD Art. 7º IX, ainda que a interpretação varie)
- **Canal de comunicação LGPD** (email dpo@ ou privacidade@) mesmo sem DPO formal — agentes de pequeno porte dispensados de nomear DPO, mas **devem manter canal** (ANPD Res. 2/2022)
- **Registro de marca SensoriPlay no INPI** (classe 28 — brinquedos + classe 35 — comércio) antes de investir em branding
- **Certificado digital e-CNPJ A1** para emissão de NF-e automática (R$ 149–199/ano)
- **Cadastro no Reclame Aqui** (reativo; aderir é opcional, mas monitorar é praticamente obrigatório pelo impacto reputacional)
- **Contrato com contador** (MEI pode fazer sozinho; ME/EPP precisa — contabilidade online R$ 59–199/mês)
- **Certificado SSL válido** (já tem se o checkout funciona, mas confirmar HTTPS-only + headers de segurança)
- **Reescrever copy de produtos** substituindo "ajuda no autismo/TDAH" por formulações que não configuram claim médico (detalhe na seção 3 deste doc)

### 🟢 OPCIONAL — fase 2, depois do go-live

- Registro de marca internacional (Madrid Protocol) — só se exportar
- Selo Ebit/Reclame Aqui RA1000 (reputacional, custa)
- Adesão a associações (ABComm, ABRAE) — networking, não compliance
- Certificação ISO ou similar
- DPO externo contratado (útil acima de R$ 3,6M receita/ano)

---

## Parte 2 — Custos iniciais reais (tabela de bolso)

### 2.1. CUSTO DE ABERTURA (one-time)

| Item | Faixa de custo | Obrigatório? | Observação |
|------|---------------|--------------|------------|
| Abertura de MEI | **R$ 0** | Se faturar ≤ R$ 81.000/ano | Portal do Empreendedor — online, imediato |
| Abertura de ME (LTDA unipessoal / SLU) | **R$ 600–1.500** (Junta + taxas + contador assessoria) | Se faturar > R$ 81k | Varia por estado (em SP, Junta SP + INSS + alvarás) |
| Alvará de funcionamento municipal | **R$ 0–500** | Depende do município | Em SP capital, isento p/ virtual se não houver atendimento público |
| Inscrição estadual (SP, via Sintegra) | **R$ 0** | Sim (comércio) | Grátis, obrigatório para emitir NF-e com ICMS |
| **Certificação INMETRO por brinquedo** | **R$ 5.000–12.000 por modelo** (Modelo 5) | **SIM** | R$ 5–8k simples (Modelo 1b), R$ 7–12k Modelo 5, R$ 12–16k com ANATEL. 10–15% desconto a partir do 2º produto do mesmo fabricante |
| **Registro no INMETRO** (após certificação) | **~R$ 500** (taxa) | Sim | Taxa por produto registrado |
| Certificado digital e-CNPJ A1 | **R$ 149–199/ano** | Sim (para NF-e) | Bling/Certisign/Serasa |
| Registro de marca INPI (classe 28) | **R$ 440** (MEI/ME/EPP) ou R$ 880 (demais) | Desejável | Taxa unificada desde set/2025; cobre 10 anos |
| Registro de marca INPI (classe 35 — comércio varejista) | **R$ 475 adicional** | Desejável | 2ª classe no mesmo pedido |
| Domínio .com.br + hospedagem 1 ano | **R$ 50–300** | Sim | Registro.br + DigitalOcean |
| Assessoria jurídica inicial (Política Privacidade + Termos + Política Trocas) | **R$ 500–2.500** | Altamente recomendado | Modelos prontos R$0–200, redação sob medida R$ 1.500+ |

**Subtotal realístico (2 brinquedos certificados + CNPJ ME + marca + advogado):**
- **Cenário barato (MEI, 1 produto certificado, modelos prontos):** ~R$ 6.000
- **Cenário razoável (ME, 3 produtos certificados, marca, advogado):** ~R$ 25.000
- **Cenário profissional (ME, 10 produtos, marca 2 classes, jurídico completo):** ~R$ 70.000

### 2.2. CUSTO RECORRENTE MENSAL

| Item | Valor | Observação |
|------|-------|------------|
| DAS do MEI (se MEI) | **~R$ 75–80/mês** | Comércio 2026; reajusta conforme salário-mínimo |
| Contador online (se ME/EPP, Simples Nacional) | **R$ 59–199/mês** | Contabilizei, Agilize, Wise |
| Tributos Simples Nacional (comércio anexo I) | **4% a 19%** progressivo | ~4% até 180k/ano, sobe conforme faturamento |
| Emissor de NF-e (Bling, Tiny, Omie, NFe.io, Plugnotas) | **R$ 0–60/mês** (até X notas) → **R$ 100–300/mês** (plano médio) | Bling Básico R$35/mês (100 notas); Plugnotas pay-per-use ~R$0,12–0,30/NFe |
| Hospedagem + domínio + SSL | **R$ 20–100/mês** | Depende do tráfego |
| Gateway Mercado Pago (taxa) | **~4,99% PIX/crédito** + R$ 0,39 fixo | Progressivo para conta negócio (cai para ~3,99% com volume) |
| Frete (absorvido em "grátis acima R$149") | **R$ 15–45 por pedido** via Melhor Envio | Depende peso + destino |
| LGPD — ferramenta canal titular (opcional) | **R$ 0–200/mês** | Google Forms serve; plataformas dedicadas R$ 100–500 |
| Reclame Aqui (monitoramento) | **R$ 0** para reagir, **~R$ 500–1.500/mês** para plano premium | Opcional |

**Overhead mensal realístico para MVP funcionando:**
- **MEI minimalista:** R$ 150–250/mês (DAS + hospedagem + NF-e pay-per-use)
- **ME com volume baixo:** R$ 400–700/mês (contador + Bling + certificado + hospedagem)
- **ME com volume médio (500 pedidos/mês):** R$ 1.500–3.000/mês (+ tributos sobre faturamento)

---

## Parte 3 — Top 10 riscos jurídicos por ordem de gravidade

Classificação: probabilidade (P) × impacto (I). Impacto em R$ e em continuidade do negócio.

| # | Risco | Base legal | Gravidade | Probabilidade | Consequência |
|---|-------|-----------|-----------|---------------|--------------|
| **1** | **Revender brinquedo sem certificação INMETRO** | Port. 563/2016 + Lei 9.933/99 Art. 8º | 🔴 CRÍTICO | ALTA — IPEMs fiscalizam mkt places e físicos | Multa R$100–R$1,5M + apreensão + interdição de atividade. Responsabilidade SOLIDÁRIA na cadeia — não adianta culpar fornecedor |
| **2** | **Claim terapêutico sem registro ANVISA** (promessa de "curar/tratar" TEA/TDAH) | Art. 37 CDC (publicidade enganosa) + Art. 39 IV CDC (aproveitar fraqueza) + Código CONAR Seção 11 | 🔴 CRÍTICO | MÉDIA — aumenta com visibilidade | Ação MP + Procon, retirada forçada de anúncios, multa Procon R$ milhares a milhões. Dano reputacional enorme no nicho (mães neurodivergentes comunicam muito) |
| **3** | **Vender sem emitir nota fiscal** | Art. 1º Lei 8.137/90 (crime contra ordem tributária) + CTN | 🔴 CRÍTICO | ALTA (se descoberto) | Crime tributário (reclusão 2–5 anos) + multa 75–150% do imposto devido. Cruzamento via Mercado Pago → Receita detecta |
| **4** | **Publicidade dirigida a criança com estímulo à compra** | Seção 11 CONAR + Art. 37 §2º CDC | 🟠 ALTO | BAIXA-MÉDIA (improvável pelo nicho, mas possível se usar "peça pro papai comprar") | Processo CONAR + MP Infância; retirada de campanha. CONAR não multa mas a sanção moral afeta mídia paga |
| **5** | **LGPD — vazamento ou ausência de base legal** | Arts. 18, 46, 48, 52 LGPD | 🟠 ALTO | BAIXA para empresa pequena; MÉDIA com volume | Multa até 2% do faturamento (teto R$ 50M) + obrigação de notificar titulares em 48h |
| **6** | **Não cumprir direito de arrependimento 7 dias** | Art. 49 CDC + Dec. 7.962/2013 | 🟠 ALTO | ALTA (cliente reclama) | Ação no JEC individual (~R$ 3–15k cada), dano moral; reincidência = Procon multa |
| **7** | **Enquadramento MEI inadequado para o faturamento real** | LC 123/2006 Art. 18-A | 🟡 MÉDIO | MÉDIA (se vendas subirem rápido) | Desenquadramento retroativo + cobrança de tributos como ME/EPP desde o estouro do teto (R$ 81k/ano em 2026) |
| **8** | **Não ter dados de CNPJ e contato visíveis no site** | Art. 2º Dec. 7.962/2013 | 🟡 MÉDIO | MÉDIA | Notificação Procon → obrigação de correção + multa diária se reincidente |
| **9** | **Violação de marca registrada por terceiros** | Lei 9.279/96 (LPI) | 🟡 MÉDIO | BAIXA-MÉDIA — o nome "SensoriPlay" é bastante único mas há colisão potencial com "Sensory Play" genérico e marcas derivadas | Obrigação de mudar marca + dano se houver; investimento em branding perdido. **Priorizar consulta INPI ANTES de escalar marketing** |
| **10** | **SAC fora das regras (Dec. 11.034/2022)** — sem canal humano acessível | Dec. 11.034/2022 Arts. 5º, 6º, 10 | 🟢 BAIXO-MÉDIO | BAIXA inicial (decreto foca setores regulados como telecom/banco, mas varejo ecommerce é alcançado) | Notificação Procon; obrigação de adequação |

**Risco oculto não tabelado:** como *marketplace* das próprias produtos importados (se comprar de China via Shopee e revender), você assume papel de **importador** perante o fisco — tem que pagar Imposto de Importação + IPI + PIS/COFINS/Cofins-Importação + ICMS-ST. Só compensa acima de ~R$ 10k/mês de volume. Para começo: **comprar de distribuidor nacional com NF + certificado INMETRO do fornecedor**.

---

## Parte 4 — Roteiro priorizado (ordem exata)

### FASE 0 — Preparação (semana -1, antes de gastar R$1)

1. **Consulta INPI** — buscar "SENSORIPLAY", "SENSORI PLAY", "SENSORY PLAY" na base do INPI (gov.br/inpi) nas classes 28 e 35. Se colidir com marca já registrada, renomear ANTES. Custo: R$ 0, 30 min de trabalho.
2. **Escolha de fornecedores com certificado INMETRO NA MÃO** — exigir cópia do Certificado de Conformidade + nº de registro INMETRO. Sem isso, não comprar. Anotar em planilha: fornecedor → produto → nº cert → validade → CNPJ do detentor do certificado.
3. **Decidir MEI vs ME** — projetar faturamento ano 1. Se < R$ 81k: MEI. Se expectativa de estourar nos primeiros 6 meses: já abrir ME (Simples Nacional Anexo I). Como o produto de entrada é R$ 39 e ticket médio R$ 150, 540 pedidos/ano já estoura MEI — **SensoriPlay provavelmente nasce ME**.

### FASE 1 — Abertura legal (semana 1–2)

4. **Abrir CNPJ** como ME (LTDA unipessoal ou SLU) via Junta Comercial + Redesim.
   - **CNAE principal**: `4763-6/01` — Comércio varejista de brinquedos e artigos recreativos ✅
   - **CNAE secundário**: `4789-0/99` — Comércio varejista de outros produtos não especificados (para fidgets/acessórios que não se encaixem)
   - **CNAE secundário** (fase 2): `8220-2/00` — Atividades de teleatendimento / `7490-1/99` consultoria (se abrir consultoria B2B para terapeutas)
   - Regime: Simples Nacional Anexo I (comércio) — 4% inicial
5. **Obter inscrição estadual** (para emitir NF-e com ICMS).
6. **Comprar certificado digital A1 e-CNPJ** (R$ 149–199/ano, Certisign/Serasa via Bling).
7. **Contratar contador online** (Contabilizei/Agilize R$ 99–199/mês).

### FASE 2 — Compliance de produto e loja (semana 2–4)

8. **Exigir certificados INMETRO dos fornecedores** + validar cada número de registro em http://registro.inmetro.gov.br. **Bloquear cadastro de qualquer produto sem cert válido no admin do SensoriPlay.**
9. **Redigir (ou comprar pronto) os 3 documentos legais**:
   - Política de Privacidade (LGPD)
   - Termos de Uso
   - Política de Trocas, Devoluções e Reembolsos (com direito de arrependimento 7 dias explícito)
   - Adicionar links no rodapé + checkbox obrigatório no checkout
10. **Publicar no rodapé do site**: Razão Social, CNPJ, endereço completo, email, telefone/WhatsApp, horário de atendimento. Isso não é cosmético — é exigência do Dec. 7.962/2013.
11. **Cookie banner** com opt-in granular (necessários vs analytics vs marketing). Ferramentas grátis: Cookiebot (free tier), cookie-consent simples.
12. **Canal LGPD**: criar `privacidade@sensoriplay.com.br` + formulário na página de Privacidade. Obrigatório mesmo para MEI/pequeno porte (sem DPO nomeado, precisa do canal — ANPD Resolução CD/ANPD 2/2022).

### FASE 3 — Fiscal e pagamento (semana 3–4)

13. **Migrar Mercado Pago para Conta Negócio (PJ)** usando o CNPJ. Taxas progressivas melhores + permite emissão de NF automática integrada.
14. **Configurar integração com emissor de NF-e**:
   - **Opção barata**: NFe.io (pay-per-use ~R$0,15/NFe) via API → integra ao FastAPI backend
   - **Opção completa**: Bling (R$ 35–115/mês) — ERP + NF + estoque + integrações Mercado Pago/Melhor Envio nativas
   - Para MVP, **recomendo Bling ou Plugnotas** — NFe.io exige dev; tempo > dinheiro
15. **Fluxo de emissão**: a cada pedido pago → gerar NF-e automática → enviar PDF+XML por email ao cliente → arquivar XML por 5 anos (obrigação fiscal).
16. **Se SP**: NFC-e obrigatória desde jan/2026 — verificar se o emissor cobre. Para venda online (à distância), NF-e modelo 55 é o padrão; NFC-e é para venda presencial.

### FASE 4 — Copy compliance (semana 3)

17. **Revisar TODO o copy de produto** e remover:
    - ❌ "ajuda no autismo" → ✅ "útil em contextos de hipersensibilidade sensorial"
    - ❌ "trata TDAH" → ✅ "apoia momentos que exigem foco"
    - ❌ "acalma crises" → ✅ "pode contribuir para o conforto em ambientes ruidosos"
    - ❌ "recomendado por médicos" (sem nome e CRM) → ✅ "recomendado por terapeutas ocupacionais" (com nome e CREFITO)
    - ❌ emojis/infantilização → manter tom adulto e informativo (já é diretriz do RESEARCH.md §6)
    - Adicionar em cada PDP com alegação terapêutica um disclaimer: *"Este produto é um brinquedo/acessório sensorial e não substitui acompanhamento profissional. Não é dispositivo médico registrado na ANVISA."*

### FASE 5 — Logística e frete (semana 4)

18. **Cadastro no Melhor Envio** (pode ser com CPF inicialmente, mas após CNPJ ativar PJ para notas e contratos melhores).
19. **Definir política de frete** alinhada com RESEARCH §7: grátis acima de R$149 (absorvendo R$15–45 por pedido — incorporar ao custo dos produtos; benchmark mostra essa é a margem que o nicho aceita).
20. **Política de frete reverso** em devoluções: por CDC (Art. 18) defeito/não-conformidade = **lojista paga**. Arrependimento (Art. 49, compra online) = divergência legal; interpretação majoritária TJDFT e STJ é **lojista paga** porque o consumidor "está exercendo direito legal". Orçar isso no preço.

### FASE 6 — Propriedade intelectual (semana 4–6, paralelo)

21. **Depositar marca SENSORIPLAY no INPI** — classe 28 (+ classe 35 se couber orçamento). R$ 440 × 1 ou 2 classes. Recomendo **fazer com agente de PI** (~R$ 500 honorários) na primeira vez — taxa de aprovação sobe de ~65% para 90%+.

### FASE 7 — Go-live defensável (semana 6+)

22. **Checklist de go-live** antes de abrir divulgação:
    - [ ] CNPJ emitindo NF-e real
    - [ ] Todos produtos no admin com nº certificado INMETRO preenchido
    - [ ] Rodapé com CNPJ + endereço + contato
    - [ ] Política Privacidade + Termos + Trocas publicadas e linkadas no checkout
    - [ ] Cookie banner ativo
    - [ ] Canal LGPD funcional (email + formulário)
    - [ ] Mercado Pago Conta Negócio configurada
    - [ ] Copy revisado sem claims médicos
    - [ ] Política de frete + prazo publicada na página do produto
    - [ ] Email de SAC com resposta automática confirmando recebimento + prazo de 7 dias úteis

---

## Anexos — respostas pontuais às perguntas específicas do briefing

### A. Estrutura jurídica — respostas diretas

- **CNPJ obrigatório?** SIM, para venda recorrente com ânimo de lucro. Operar sem = crime tributário + informalidade agravante.
- **MEI serve?** Sim, no início. Teto 2026: **R$ 81.000/ano** (R$ 6.750/mês de referência). Há projeto no Congresso pra elevar mas **não foi sancionado**. Assuma R$ 81k.
- **Tipo ideal**: MEI → migrar para **ME (Simples Nacional Anexo I)** no estouro do teto. LTDA-LTDA (com sócio) só faz sentido depois. SLU/LTDA-unipessoal é o formato recomendado p/ Leo sozinho no controle.
- **CNAE brinquedos online**: **4763-6/01** ✅ permite MEI e é o correto (cobre venda online e física).
- **CNAE consultoria terapêutica**: se fizer curadoria paga B2B (clínicas/escolas), adicionar **8599-6/99** (outras ativ. de ensino) ou **7020-4/00** (consultoria empresarial) — ATENÇÃO: **consultoria em saúde mental requer registro em conselho profissional** (CRP/CREFITO). Sem profissional habilitado contratado, não oferecer "consulta", só "curadoria de produtos".
- **ISS municipal**: só incide se prestar serviço. Venda de produto = ICMS, não ISS. Se cobrar consultoria separadamente, aí cai no ISS do município.
- **ICMS interestadual + DIFAL**: **Simples Nacional NÃO paga DIFAL em venda para consumidor final não contribuinte** (ADI 5469 STF). Isso é bom — simplifica ecommerce para todo o Brasil. Empresa que sai do Simples passa a pagar DIFAL; planejar quando isso acontecer.

### B. Regulatório INMETRO — respostas diretas

- **Certificação compulsória para brinquedos?** SIM, Port. 563/2016 + atualizações via Port. 302/2021. Abrange **todo produto recreativo para menores de 14 anos**.
- **Custo**: R$ 5.000–12.000 por modelo (R$ 7–12k Modelo 5, o mais comum para importados). Desconto 10–15% a partir do 2º produto.
- **Processo**: escolher OCP acreditado (Yes, Saron, BRICS, Intertek) → enviar amostras → ensaio em laboratório → auditoria de fábrica (Modelo 5) → emissão do certificado (2–4 semanas se tudo em ordem, realisticamente 6–10 semanas).
- **Embalagem exige**: nome comercial, fabricante/importador+CNPJ, país de origem, faixa etária recomendada, advertências de segurança (partes pequenas, idade mínima), selo de identificação do OCP, marcação em português.
- **Revenda de importado sem cert**: apreensão + multa. Responsabilidade SOLIDÁRIA — o IPEM autua quem está com o produto irregular. **Sempre exigir certificado do distribuidor antes de comprar.**

### C. Alegação terapêutica — respostas diretas

- **Abafador de ruído, colar mordedor, fidget "terapêutico"** — são classificados como **brinquedos** pela Port. 302/2021 se a função primária for lúdica/sensorial. Viram **produto para saúde (ANVISA Classe I)** se comercializados como EPI/dispositivo médico. **Para SensoriPlay, manter como brinquedo é mais simples** — mas a rotulagem e copy devem respeitar isso (não prometer ação terapêutica).
- **ANVISA registra?** Só se vendido como dispositivo médico. Se for brinquedo/acessório sensorial, **fica no INMETRO**. Não tente "dupla pegada" — escolha um caminho.
- **Claim "ajuda no autismo/TDAH"**: zona cinzenta. **Como brinquedo, não pode prometer efeito terapêutico** (CONAR + Art. 37 CDC). **Solução do RESEARCH.md §6 já é correta**: usar "útil para", "apoia", "contexto de hipersensibilidade", com disclaimer de que não substitui tratamento. Manter.
- **Procon/MP**: o nicho é vigiado. MP Infância tem agido contra marcas que capitalizam em vulnerabilidade familiar (ver casos de "suplementos para autismo"). Evitar 100% qualquer promessa de cura/tratamento.

### D. LGPD — respostas diretas

- **Site captura dados de auth + checkout** — SIM, é tratamento de dado pessoal (Art. 5º I LGPD). Base legal: execução de contrato (Art. 7º V) para dados de pedido; consentimento (Art. 7º I) para marketing/newsletter.
- **Política de Privacidade obrigatória?** SIM, Art. 9º LGPD — titular tem direito de acesso fácil a informação clara sobre tratamento.
- **Termos de Uso**: não é obrigatório por lei específica, mas na prática **indispensável** para definir contrato, limitar responsabilidade, estabelecer jurisdição.
- **Cookie banner**: interpretação predominante é **obrigatório** quando há analytics/marketing (tratamento além do necessário). ANPD publicou orientação em 2022 recomendando opt-in granular.
- **DPO obrigatório?** Para agentes de pequeno porte (receita ≤ R$ 4,8M como ME) a ANPD (Resolução CD/ANPD 2/2022) **dispensa nomeação formal**, MAS **obriga manter canal de comunicação com titulares** — email dedicado ou formulário. Acima de R$ 3,6M recomenda-se DPO (interpretação da ANPD recente).
- **Direitos do titular**: todos os 9 direitos do Art. 18 devem ser atendíveis em até 15 dias. Criar processo interno — planilha simples já serve em volume baixo.

### E. Nota fiscal e pagamento — respostas diretas

- **NF obrigatória em toda venda?** SIM, nenhuma exceção para ecommerce. MEI também emite (obrigação vem aumentando com Reforma Tributária).
- **NFC-e vs NF-e**: NFC-e (modelo 65) é para venda presencial ao consumidor. **Ecommerce usa NF-e modelo 55** (venda à distância). Em SP, NFC-e obrigatória para varejo físico desde jan/2026 — não afeta ecommerce puro.
- **Emissores recomendados** (fase 1):
  - **Bling** (R$ 35–115/mês): mais completo, integra tudo, NF + estoque + Mercado Pago + Melhor Envio
  - **Plugnotas**: API pay-per-use (~R$0,12–0,30/NFe), barato se dev integrar ao FastAPI
  - **NFe.io**: similar a Plugnotas, foco API
  - **Tiny ERP**: concorrente do Bling, preços parecidos
- **Certificado digital A1**: SIM obrigatório para emitir NF-e. Validade 12 meses, R$ 149–199/ano.
- **Mercado Pago PF vs PJ**: PF tem limite prático ~R$ 10k/mês por 3 meses → obriga CNPJ. PJ (Conta Negócio) tem taxas melhores progressivas. **Migrar assim que CNPJ estiver ativo.**

### F. Logística — respostas diretas

- **Correios contrato PJ**: só compensa acima de ~100 envios/mês (desconto 15–40% sobre balcão). Até lá, **Melhor Envio/Frenet/Kangu** já dão 22–80% de desconto sem contrato.
- **Melhor Envio**: permite cadastro com CPF (começar) ou CNPJ (migrar depois). Frete reverso integrado — facilita devoluções.
- **Jadlog**: bom no Sul/Sudeste, 1–10kg, áreas urbanas. Correios ganham em cobertura nacional e envios leves.
- **Embalagem**: brinquedos frágeis (luminárias, ponderados) exigem plástico bolha + caixa. Custo ~R$ 3–8 por pacote. Embalagem presente **SIM é diferenciador** (Lovevery faz) — ~R$ 2–5 a mais, paga-se via ticket médio maior.
- **"Frete grátis acima de R$ 149"**: absorção média R$ 15–35 por pedido para SE/Sul. Nordeste/Norte custa R$ 40–80 (avaliar se aumenta o mínimo para NE/N ou se incorpora no preço).
- **Devolução**: por CDC e majoritária jurisprudência, **custo do frete reverso é do lojista** (tanto por defeito quanto por arrependimento). Prever no P&L.

### G. SAC — respostas diretas

- **Decreto 11.034/2022 (SAC 2.0)**: aplicável a serviços **regulados** (telecom, banco, saúde, energia) com rigor; setor varejo ecommerce é alcançado em princípio geral mas a fiscalização foca em telecom/bancos. Boa prática seguir mesmo assim.
- **Obrigações mínimas para ecommerce**:
  - Canal telefônico + 1 outro (WhatsApp, email, formulário)
  - Opção de falar com humano em canais automatizados
  - Resposta em até 7 dias corridos
  - Não transferir mais de 1 vez no mesmo atendimento
  - Horário telefônico mínimo 8h/dia em dias úteis (para empresas de porte; para MEI/ME pequeno, email + WhatsApp funcionam)
  - Gravar chamadas 90 dias / manter registros 2 anos
- **Para SensoriPlay fase 1**: email `contato@` + WhatsApp Business com resposta automática + formulário no site = cobre o mínimo razoável.

### H. Importados — respostas diretas

- **Revender chinês importado direto**: vira **importador**. Precisa DI (Declaração de Importação) + II + IPI + PIS/COFINS-Importação + ICMS-ST. Inviável sem volume alto.
- **Comprar de distribuidor nacional**: muito melhor para começar. Ele importa, paga impostos, emite NF de venda, **fornece cópia do Certificado INMETRO**. Você revende com NF de saída sua.
- **Regra crítica**: nunca aceitar produto "sem nota". Sem NF de entrada, você não pode emitir NF de saída e cria cadeia de sonegação.

### I. Propriedade intelectual — respostas diretas

- **Consulta "SENSORIPLAY" no INPI**: pendente (fazer na Fase 0). Nome é razoavelmente único em PT-BR mas pode colidir com "Sensory Play" (inglês/americano). Há registros internacionais em classe 28 nos EUA com variantes — **fazer a consulta antes de escalar branding**.
- **Registrar como**: classe 28 (brinquedos) prioritária; classe 35 (comércio/ecommerce) recomendada se orçamento permitir.
- **Custo 2026**: R$ 440 (MEI/ME/EPP, especificação pré-aprovada) por classe, **10 anos de proteção inclusos** (reforma INPI de set/2025 unificou taxas).
- **Logo**: protegido por direito autoral automaticamente. Registrar como marca mista (nome+logo) custa o mesmo.
- **Conteúdo do blog/educativo**: direitos autorais automáticos. Produzir próprio, citar fontes quando usar pesquisa de terceiros (Lovevery, Ayres, etc.).

---

## Parte 5 — Fluxograma de decisão rápida para Leo

```
┌────────────────────────────────────────────┐
│  SITE ESTÁ NO AR HOJE (IP:8090) ?          │
│  → NÃO VENDE AINDA                         │
│  Risco atual: baixo (nenhum pedido real)   │
└──────────────┬─────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────┐
│  VAI VENDER DE VERDADE EM < 30 DIAS?       │
└───────┬──────────────────────┬─────────────┘
        │ SIM                  │ NÃO
        ▼                      ▼
┌─────────────────┐   ┌──────────────────────┐
│ FAZER FASES 1-3 │   │ Fase 0 (consulta     │
│ ANTES DE LIGAR  │   │ INPI + estudar       │
│ CHECKOUT REAL.  │   │ fornecedores com     │
│ CUSTO MÍNIMO    │   │ INMETRO pronto)      │
│ ~R$ 6–10k       │   │ enquanto bot de      │
│ PARA LEGALIDADE │   │ cripto gera caixa    │
│ MÍNIMA.         │   │                      │
└─────────────────┘   └──────────────────────┘
```

**Recomendação final do agente Compliance:**

Se a prioridade declarada no PROJECT_BRIEF é "P0 — Site no ar e navegável", ok, o site pode ficar no ar **em modo catálogo/lista de espera** (sem checkout funcional) sem violar nada. O momento em que o botão "Comprar" começa a processar pagamento real é o momento em que TODA a Parte 1 impeditiva precisa estar cumprida. Isso é inegociável — o nicho é fiscalizado, tem associações de pais vigilantes, e um caso de "loja vendendo brinquedo sem INMETRO pra mãe de autista" vai longe rápido em mídia e Procon.

**Orçamento mínimo realístico para ir ao ar vendendo legal**: R$ 8.000–15.000 (setup) + R$ 400–700/mês (recorrente), assumindo ME Simples + 2–3 produtos certificados + advogado básico + Bling + certificado digital. Dimensionamento faseado é possível: começar com 2 produtos certificados, expandir catálogo conforme caixa.

---

## Referências e fontes consultadas

### Legislação primária
- [Lei 8.078/1990 — Código de Defesa do Consumidor](http://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm) (Arts. 37, 39, 49)
- [Lei 13.709/2018 — LGPD](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [Lei 9.933/1999 — INMETRO](http://www.planalto.gov.br/ccivil_03/LEIS/L9933.htm) (Art. 8º — multas)
- [LC 123/2006 — Simples Nacional e MEI](http://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm)
- [Decreto 7.962/2013 — Marco do Comércio Eletrônico](http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/decreto/d7962.htm)
- [Decreto 11.034/2022 — Novo SAC](http://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/decreto/d11034.htm)
- [Portaria INMETRO 563/2016 + 302/2021 — Brinquedos](http://www.inmetro.gov.br/brinquedo/)
- [Lei 9.279/1996 — Propriedade Industrial (LPI)](http://www.planalto.gov.br/ccivil_03/leis/l9279.htm)

### Fontes consultadas 2026 (web)
- [Limite MEI 2026 R$81.000 — Contabilizei](https://www.contabilizei.com.br/contabilidade-online/faturamento-mei-2026/)
- [Regulamento Brinquedos INMETRO — Perguntas Frequentes](http://www.inmetro.gov.br/brinquedo/)
- [Custo Certificação Brinquedos INMETRO 2026 — Yes Certificações](https://yescert.com.br/blog/inmetro/quanto-custa-certificar-brinquedos-inmetro/)
- [Multas Produto Sem INMETRO](https://yescert.com.br/blog/guias-tutoriais/produto-sem-certificacao-inmetro-quais-sao-as-multas-e-penalidades/)
- [LGPD Dispensa DPO Pequeno Porte — ANPD Res 2/2022](https://www.privacytools.com.br/en/dpo-nas-pequenas-empresas/)
- [NFC-e SP Obrigatória 2026 — Certisign](https://certisign.com.br/blog/nfc-e-obrigatoria-sp)
- [Reforma Tributária MEI/Simples 2026–2027](https://tactus.com.br/reforma-tributaria-e-simples-nacional/)
- [CNAE 4763-6/01 — Comércio Varejista Brinquedos](https://concla.ibge.gov.br/busca-online-cnae.html?subclasse=4763601&view=subclasse)
- [Decreto 11.034 Novo SAC — Projuris](https://www.projuris.com.br/blog/lei-do-sac/)
- [Direito de Arrependimento 7 dias — Serasa](https://www.serasaexperian.com.br/conteudos/direito-de-arrependimento-do-cdc/)
- [DIFAL Simples Nacional dispensa consumidor final — MRS Advogados](https://mrsadvogados.com/empresas-optantes-pelo-simples-nacional-e-o-difal-nas-vendas-para-consumidor-final/)
- [INPI Taxas Registro Marca 2026](https://contaja.com.br/blog/quanto-custa-registrar-uma-marca/)
- [CONAR Criança e Consumo](http://www.conar.org.br/pdf/conar-criancas.pdf)
- [Mercado Pago Conta Negócio PJ](https://conteudo.mercadopago.com.br/conta-pj-mercado-pago)
- [Melhor Envio — Plataforma de Fretes](https://melhorenvio.com.br/)

---

**Fim do debate 04 — Compliance BR.**
*Próxima recomendação: alinhar com o Tech-lead Atlas a implementação de campos "INMETRO_cert_number" e "INMETRO_validity_date" obrigatórios no schema de products do SensoriPlay, bloqueando publicação de produto sem esses campos preenchidos. Isso transforma compliance em controle técnico — que é o jeito certo de não esquecer.*
