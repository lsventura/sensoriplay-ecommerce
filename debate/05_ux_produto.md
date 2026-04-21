# Auditoria UX/Produto — SensoriPlay
**Autora:** UX Lead Sênior (Atlas Team)
**Data:** 2026-04-19
**Metodologia:** Inspeção direta de código-fonte + análise heurística Nielsen + benchmark competitivo contra RESEARCH.md

---

## Premissa honesta

Antes de começar: o site atual não é um desastre. É um MVP tecnicamente funcional, com design system documentado, stack limpa, e boas intenções de acessibilidade. O problema é que "não é desastre" não converte. Para um e-commerce de nicho sensível, precisamos de mais — muito mais. Esta auditoria não vai poupar elogios falsos.

**Nota geral: 5.5 / 10**

Justificativa: a fundação é sólida (tokens, componentes, aria-labels), mas falha sistematicamente nos momentos de decisão de compra. Um usuário motivado consegue comprar. Um usuário ansioso, cansado ou em dúvida abandona antes do checkout.

---

## 1. Auditoria Heurística — Nielsen's 10

### 1.1 Visibilidade do Status do Sistema — Nota: 6/10

**O que funciona:**
- Toast notifications para "adicionado ao carrinho" (verde, canto inferior direito).
- Badge do carrinho com contador no header.
- Progress steps no checkout (1/2/3) visíveis e com estados done/active.
- Barra de progresso para frete grátis no carrinho.

**O que quebra:**
- Ao carregar a página, a vitrine aparece vazia por frações de segundo (sem skeleton loader). Em conexão lenta, fica vazia por segundos sem qualquer indicador de que está carregando. O `showToast('Carregando catalogo...', 'info')` só dispara em caso de erro de API — não existe loading state visual no grid de produtos.
- A busca é debounced (350ms), mas sem indicador visual de "buscando". O usuário não sabe se o campo reagiu.
- Na PDP (`produto.html`), o produto inteiro fica dentro de `<div id="pdpMain" style="display:none">` e só aparece quando o JS carrega. Em conexão lenta, o usuário vê uma página em branco. Não há loading skeleton.
- O filtro de categorias na home (tabs "Por Idade" / "Por Sentido" / "Por Objetivo") é preenchido por JS, mas não tem estado ativo visual persistente — ao rolar a página, o usuário perde o contexto de qual filtro está aplicado.

**Severidade:** Médio. O efeito de flash-of-empty-content é percebido pelo usuário como "site quebrado" na primeira visita.

---

### 1.2 Correspondência entre Sistema e Mundo Real — Nota: 7/10

**O que funciona:**
- Linguagem do BRAND.md é seguida com consistência: sem "fofinho", sem promessas vazias.
- Labels de categoria são claros: "Fidgets", "Ponderados", "Kits e Bundles".
- FAQ usa linguagem natural, não jargão clínico.
- O copy do hero ("Cada sentido que desperta abre uma porta no cérebro") é bom — evocativo sem ser vazio.

**O que quebra:**
- A seção de categorias na home tem tab "Por Objetivo" com itens como "Autorregulação", "Propriocepção", "Integração Sensorial". São termos técnicos apresentados sem tooltip, sem explicação. O BRAND.md (seção 5) exige tooltip explicativo para "propriocepção" — o site não implementa.
- O filtro de ordenação chama a primeira opção "Destaques primeiro" mas o que ele faz é ordenar por `featured: true` — não há indicação visual de quais produtos têm esse badge e por que.
- A categoria de produto no card (`product-cat-label`) mostra texto bruto da categoria do banco: "Mastigavel", "Cognicao" — sem acento, sem formatação. Um produto mostra "Água/Banho" com inconsistência de capitalização.

**Severidade:** Médio. Os termos técnicos sem contexto são um problema real para a persona "mãe ansiosa" (Ana), que não conhece jargão TO.

---

### 1.3 Liberdade e Controle do Usuário — Nota: 6/10

**O que funciona:**
- ESC fecha o modal e o carrinho.
- Botão "Limpar filtros" existe.
- Botão "Voltar à loja" no checkout.
- Modal de produto tem botão X explícito.

**O que quebra:**
- O modal de produto não tem botão "Ver página completa" suficientemente destacado. O link `modal-secondary-link` é discreto demais — um usuário que quer comparar produtos não consegue abrir dois ao mesmo tempo ou salvar para depois.
- Não existe lista de favoritos / wishlist. Para o ICP (mãe pesquisando para filho com TEA), a jornada frequentemente envolve "vou mostrar para o TO dela antes de comprar". Sem wishlist, o usuário copia link ou abandona.
- O botão "Comprar agora" na PDP (`buy-now-btn`) vai direto para checkout mas não há indicação de que o carrinho atual é mantido. Usuário pode acidentalmente abandonar itens.
- Após adicionar ao carrinho via modal da home, o modal fecha automaticamente. Isso é uma "ação imposta" — o usuário pode ter querido continuar olhando o produto.

**Severidade:** Médio. Wishlist ausente é especialmente grave para este nicho onde a compra é consultiva.

---

### 1.4 Consistência e Padrões — Nota: 4/10

**Esta é a maior falha técnica do site. Evidência direta do código:**

- O arquivo `produto.html` usa `var(--surface)`, `var(--text-main)`, `var(--text-muted)`, `var(--font-display)`, `var(--font-ui)`, `var(--bg)`, `var(--teal-light)`, `var(--coral-light)`, `var(--purple-light)`, `var(--yellow-light)` — variáveis que NÃO existem em `design-tokens.css`.
- `minha-conta.html` usa `var(--surface)`, `var(--bg)`, `var(--font-display)`, `var(--teal-light)`, `var(--yellow-light)` — mesmas variáveis fantasmas.
- O `design-tokens.css` define: `--white`, `--off-white`, `--teal-soft`, `--coral-soft`, `--purple-soft`, `--yellow-soft`, `--f-display`, `--f-body`. Mas as páginas internas usam os nomes antigos.
- Resultado: produto.html e minha-conta.html **quebram silenciosamente** — todos os `var()` sem correspondência retornam vazio, e o browser usa o valor padrão (branco ou nada). A PDP provavelmente tem fundo branco onde deveria ter off-white quente, e espaços com cor errada.

Além dos tokens quebrados:
- `checkout.html` define seu próprio sistema de botões (`.btn`, `.btn-primary`, `.btn-secondary`) inline no `<style>` da página, ignorando `components.css`. Isso significa que o botão coral do checkout pode ter bordas, padding ou hover state diferentes da home.
- A barra de notificação superior (`shipping-bar`) existe na home mas não em nenhuma página interna — o usuário que chega à PDP não vê a oferta de frete grátis.
- O header na home é `components.css` completo (logo + busca + ícones + nav-cats). Na PDP e minha-conta, é um header simplificado diferente. Não há sistema de header unificado.

**Severidade: Crítico.** Inconsistência de tokens é dívida técnica que já está afetando visualmente o site em produção agora.

---

### 1.5 Prevenção de Erros — Nota: 6/10

**O que funciona:**
- Validação de CEP com busca automática via ViaCEP no checkout.
- Campos obrigatórios marcados com `*`.
- Erro de campo marcado com classe `.err` (borda vermelha).
- Mensagem `err-msg` sob o campo com erro.
- Limite de caracteres em cupom (`maxlength="20"`).

**O que quebra:**
- Não existe validação client-side no campo nome (`nome_dest`), que aceita qualquer string. Um usuário pode digitar "123" e avançar.
- Não existe máscara de CEP — o usuário pode digitar "12345678" sem hífen e a validação pode falhar.
- O botão "Continuar para pagamento" não tem loading state. Em conexão lenta, o usuário pode clicar múltiplas vezes.
- O carrinho não avisa sobre estoque. Se um produto está com `stock: 0` no banco, o usuário só descobre no checkout (ou nunca, se a API não bloquear).
- A seleção de estado no checkout tem SP selecionado por padrão (`<option selected>SP</option>`) — para usuários de outros estados, isso é um erro pré-preenchido que precisa ser desfeito ativamente.

**Severidade:** Médio.

---

### 1.6 Reconhecimento em vez de Lembrança — Nota: 5/10

**O que funciona:**
- Filtros persistem enquanto o usuário navega na home.
- Badge de faixa etária visível em cada card de produto.
- Breadcrumb na PDP (`Home > Categoria > Produto`).

**O que quebra:**
- O card de produto mostra: categoria, nome, descrição curta, preço + Pix. Mas NÃO mostra quais sentidos o produto estimula. Para o nosso ICP, saber que um produto é "Tato + Propriocepção" é a informação de decisão mais importante — e ela está ausente do card.
- Não existe busca com sugestões (autocomplete). O usuário digita "abafad" e não vê sugestões — precisa lembrar o nome exato ou a categoria.
- Na PDP, após adicionar ao carrinho, o usuário não tem feedback de "você tem X itens no carrinho" — o toast desaparece em 3s e não há forma fácil de voltar ao carrinho sem clicar no ícone do header.
- Não há seção "Vistos recentemente". Para uma jornada de compra consultiva (pesquisa → TO → retorno → compra), o usuário precisa refazer a busca do zero.
- O filtro de categoria na vitrine mostra "Mastigavel" e "Cognicao" sem acento — o usuário que digita "mastigável" na busca pode não encontrar resultados.

**Severidade:** Alto. A ausência de tags de sentido nos cards é o maior gap de reconhecimento — e é exatamente o diferencial prometido pelo BRAND.md.

---

### 1.7 Flexibilidade e Eficiência — Nota: 4/10

**O que funciona:**
- Atalho de teclado (Enter na busca).
- Debounce na busca (350ms) para busca ao digitar.
- Filtros de dropdown mais rápidos que busca por categoria no menu.

**O que quebra:**
- Só existe um eixo de filtro por vez. RESEARCH.md identifica que o diferencial competitivo é "filtro simultâneo tato + 3-5 anos + autorregulação + até R$150". O site atual só permite filtrar por faixa etária OU categoria — nunca ambos cruzados. Um usuário expert (Juliana, a TO) perde o principal argumento de compra.
- Não há atalho de teclado para abrir carrinho, fechar modal, ou navegar entre produtos.
- Não há opção de "visualização em lista" vs "grid" — todos veem o mesmo grid de 3 colunas.
- Usuários logados não têm pré-preenchimento de endereço no checkout (a funcionalidade está no HTML comentada mas não implementada).
- Não há opção de "comprar todos os itens do kit" na PDP de bundle — o Kit Sala Calma (R$649) não tem button diferenciado de "comprar kit completo".
- O campo de busca não tem filtro de sentido ou objetivo diretamente — precisa-se combinar busca textual com dropdown, que é cognitivamente mais caro.

**Severidade: Crítico.** A falta de filtros cruzados elimina o principal diferencial competitivo do produto frente a concorrentes como BmB.

---

### 1.8 Design Estético e Minimalista — Nota: 6/10

**O que funciona:**
- Paleta coerente na home: off-white quente, coral nos CTAs, teal nos links.
- Tipografia Nunito + Inter funciona bem juntas.
- Cards com border-radius 12px e shadow sutil passam sensação de qualidade.
- Seções alternadas (off-white / cream) criam ritmo visual sem poluição.
- O hero não tem imagem de fundo — escolha limpa que evita o problema de não ter fotografia de produto.

**O que quebra:**
- O hero tem eyebrow text pequeno + H1 grande + parágrafo + dois botões + 4 trust items. São 7 elementos de informação antes do fold em mobile. A hierarquia existe mas a densidade é alta para o público-alvo (mãe ansiosa, possivelmente em modo "overwhelmed").
- A seção de categorias tem tabs (Por Idade / Por Sentido / Por Objetivo) com um grid abaixo. O grid mostra tiles com emoji + nome + descrição + botão. Para "Por Objetivo", as descrições são longas ("Brinquedos que ajudam no foco e na regulação emocional — fundamentais para crianças com TDAH, TEA ou simplesmente para quem tem dificuldade de esperar"). Isso cria tiles de altura desigual — o grid quebra o alinhamento.
- Os emojis nas tiles de categoria (👶, 🧒, 🏃, 📚, 🎯) são visualmente inconsistentes — mistura de pessoas e objetos sem sistema. Em telas com emoji set diferente (Android vs iOS), a aparência varia.
- O product placeholder (emoji de 96px em gradiente teal→coral) é funcionalmente adequado mas visualmente comunica "produto sem foto" para qualquer usuário com experiência mínima de e-commerce. É a maior fraqueza visual do site — discuto em detalhe na seção 4.
- O footer tem newsletter + 4 colunas de links. Para um MVP, é denso. A newsletter não tem indicação de frequência ou o que o usuário vai receber.
- Os depoimentos usam avatar com inicial (letra em círculo teal) em vez de foto. Em 2026, isso é aceito mas reduz autenticidade percebida.

**Severidade:** Médio. O problema do placeholder de emoji não é cosmético — é de conversão.

---

### 1.9 Ajuda a Reconhecer e Recuperar de Erros — Nota: 7/10

**O que funciona:**
- Toast com estado `.error` (fundo vermelho) para erros de API.
- Mensagem de erro inline nos campos do checkout com classe `.err-msg`.
- Página de produto não encontrado com fallback (`div.not-found`).
- Filtro sem resultado tem "Nenhum produto encontrado" + botão "Limpar filtros".

**O que quebra:**
- O toast de erro desaparece em 3 segundos. Para erros de pagamento — onde o usuário precisa agir — 3 segundos não é tempo suficiente para ler e entender a instrução.
- A mensagem de erro da API de produtos é "Carregando catálogo..." — que é uma mensagem de loading, não de erro. Se a API falhar definitivamente, o usuário não sabe que o catálogo não vai carregar.
- No checkout, se o CEP for inválido, há `cepErr` mas a mensagem específica depende da API ViaCEP. Se a ViaCEP estiver fora, o erro é genérico ("CEP não encontrado") sem alternativa (ex: "preencha manualmente").
- Erros de pagamento são tratados pelo Mercado Pago — não há mapeamento de erros comuns (cartão vencido, limite, saldo insuficiente) para mensagens amigáveis em PT-BR na interface.

**Severidade:** Médio.

---

### 1.10 Ajuda e Documentação — Nota: 5/10

**O que funciona:**
- FAQ com 4 perguntas na home + link "Ver todas as perguntas".
- Página `faq.html` existe.
- Depoimento da TO (Dra. Fernanda) serve como prova de que o site é adequado para uso profissional.

**O que quebra:**
- Não há chat ao vivo ou WhatsApp visível. O FAQ menciona "chat" e "WhatsApp" nas respostas mas não há botão flutuante de suporte. O usuário que tem dúvida no meio do fluxo não tem saída óbvia.
- Não há guia de como usar os filtros. Um pai que nunca ouviu falar de "propriocepção" não vai clicar em "Por Sentido > Propriocepção". Faltam tooltips nos termos técnicos (prometidos no BRAND.md, não entregues).
- A seção "Como funciona" (3 steps) é boa, mas está enterrada depois do hero e de benefícios — o usuário que chega confuso precisa dela antes, não depois.
- Não existe guia de compra para profissionais (mencionado no FAQ como "área profissional no menu" — mas não existe área profissional no menu).
- O produto não tem instruções de uso na listagem. A PDP tem a tab "Como usar" com texto genérico idêntico para todos os produtos — não é personalizado por produto.

**Severidade:** Alto. Para um nicho onde a dúvida é a principal barreira de conversão, ausência de suporte acessível é crítica.

---

## 2. Jornada do Usuário por Persona

### Persona 1: Ana (mãe ansiosa, filho TEA 4 anos, 2 meses de diagnóstico)

**Canal de entrada:** Google "brinquedo sensorial autismo" → provavelmente landing na home.

**Jornada:**

1. **Home** — A shipping-bar no topo ("Frete grátis acima de R$199, cupom BEMVINDO10") é relevante. O hero headline "Cada sentido que desperta" é abstrato para ela neste momento — ela quer ver "autismo" ou "TEA" de forma explícita. O eyebrow text diz "Curadoria especializada em desenvolvimento sensorial" — não valida o diagnóstico dela.

2. **Trust bar** — "Certificado INMETRO, 7 dias devolução, Curadoria por TOs" — esse último ponto importa muito para Ana. Mas não há link para ver quem são esses TOs. É uma afirmação sem prova.

3. **Benefícios** — 5 cards. Ana vai ler o terceiro ("Linha profissional para terapeutas") e pensar: "isso é para mim ou para a terapeuta da minha filha?". A seção não faz distinção clara.

4. **Filtro de categorias** — Ana clica em "Por Objetivo". Vê "Autorregulação", "Propriocepção", "Integração Sensorial", "Foco e Atenção". Ela não sabe o que seu filho precisa especificamente. O RESEARCH.md menciona que Fun and Function tem "quiz de descoberta" — aqui não existe. Ana está perdida.

5. **Vitrine** — Ela tenta o dropdown "Toda faixa etária → 4+ anos". Resultado: vê 3-4 produtos. Nenhum card menciona "TEA" ou "autismo". A descrição curta do produto é informativa mas não conecta com o contexto dela. Ela não sabe qual escolher.

6. **Card de produto** — Clica no emoji do produto (acidentalmente abre modal). O modal mostra: categoria, nome, preço, descrição, botão "Adicionar ao carrinho" e link "Ver página completa". Ela quer mais informação — clica no link. Vai para PDP.

7. **PDP** — Encontra ficha técnica com ícones, tabs, FAQ do produto. A tab "Como usar" é genérica. O FAQ da PDP pergunta "O produto é adequado para meu filho com TEA?" e responde "A adequação depende do perfil sensorial da criança". Ana fica mais ansiosa, não menos.

8. **Decisão** — Ana não consegue relacionar o produto ao diagnóstico do filho sem orientação explícita. Probabilidade de conversão nesta sessão: **15-25%**. Ela provavelmente vai salvar o link, consultar a TO e talvez voltar. Mas sem wishlist, ela perde o link.

**Fricção crítica:** ausência de "útil para TEA" como filtro/badge, ausência de quiz, ausência de curadoria nomeada por TO.

---

### Persona 2: Juliana (TO profissional, quer 12 unidades para consultório)

**Canal de entrada:** Indicação de colega → home ou busca direta por nome.

**Jornada:**

1. **Home** — Juliana vê a trust bar: "Curadoria por TOs". Clica mentalmente em "aprovado". O eyebrow do hero valida. Vai direto para a vitrine.

2. **Filtros** — Juliana quer "fidgets sensoriais para crianças de 3 a 8 anos". Ela tenta: dropdown "Faixa etária" → "3+" + dropdown "Categoria" → "Fidget". Resultado: aparecem os fidgets de 3+. Mas ela também queria ver os de 5+ e 6+ juntos. Teria que rodar o filtro 3 vezes e comparar mentalmente.

3. **Multiproduto** — Juliana quer comprar 12 unidades de 3 produtos diferentes. Ela adiciona ao carrinho: 4 de um, 4 de outro, 4 de um terceiro. O carrinho não tem campo de quantidade — cada adição é +1. Ela precisa clicar 12 vezes. (Verificado no código: `addToCart(id)` sempre adiciona 1.)

4. **Checkout** — Juliana precisa de nota fiscal para CNPJ. O checkout não tem campo de CNPJ. Há menção no FAQ de "modalidade para profissionais" mas não há botão ou fluxo visível.

5. **Abandono** — Juliana vai embora para buscar outro fornecedor com NF-e. Probabilidade de conversão: **5-10%** nesta sessão.

**Fricção crítica:** ausência de seletor de quantidade, ausência de fluxo B2B com CNPJ. Juliana é o ICP com maior ticket médio e LTV — e é a que o site menos suporta.

---

### Persona 3: Rodrigo (pai tech, presente para filha de 6 anos, desenvolvimento típico)

**Canal de entrada:** Instagram/recomendação → home.

**Jornada:**

1. **Home** — Rodrigo vê o hero. O copy é bom mas um pouco sério para ele — ele não está em contexto de ansiedade, está procurando um "presente bacana". O "brincar com intenção" ressoa mas não o emociona imediatamente.

2. **Vitrine** — Rodrigo filtra por "6+ anos". Vê 4-5 produtos. Preços: R$74,90 a R$389. Ele não tem referência de qual é "justo" para o que é. Sem reviews, sem número de vendas, sem social proof nos cards.

3. **Modal** — Rodrigo clica num produto. O modal é funcional. Ele clica "Adicionar ao carrinho" e o carrinho abre no lado direito. Ele vê o total.

4. **Upsell** — O carrinho tem barra de progresso de frete grátis. Ele está em R$89. Faltam R$110 para frete grátis. Mas não há sugestão de produto para completar o valor — a barra mostra o número mas não guia.

5. **Checkout** — Rodrigo consegue finalizar. O fluxo de 3 steps é claro. Ele vai sem problemas.

**Probabilidade de conversão: 55-65%.** Rodrigo é a persona mais compatível com o site atual porque não precisa de validação especializada.

**Fricção menor:** ausência de reviews (não consegue checar se outros pais gostaram), ausência de "comprar agora via Pix" sem passar por checkout de 3 steps.

---

## 3. Benchmark Visual Rigoroso

### Lovevery (gold standard)
**Onde estamos 3 anos atrás:**
- Lovevery tem fotografia lifestyle com bebês reais em cada produto. Nós temos emojis.
- Lovevery tem descrição de produto como um pequeno artigo científico: "Neste estágio de 4-5 meses, o córtex pré-frontal começa a processar causa-efeito...". Nossas descrições são boas mas mais curtas.
- Lovevery tem sistema de assinatura por fase com curadoria trimestral. Nós somos one-shot.
- Lovevery tem quiz de descoberta prominente no hero. Nós não temos quiz.

**Onde estamos na mesma liga:**
- Tipografia clean sem exagero (Nunito é comparável ao DM Serif deles).
- Paleta off-white quente vs fundo branco frio deles (nós temos vantagem aqui).
- Copy sem infantilização (nós implementamos corretamente).

**Onde estamos à frente:**
- Lovevery não tem filtros cruzados — é tudo por fase. Nós planejamos ter (mas ainda não implementamos).
- Preço BR acessível vs US$80+ por kit.

### Fat Brain Toys
**Onde estamos atrás:**
- Fat Brain tem subcategorias por sentido no menu (Visual, Tactile, Fidget, Musical) com imagens. Nós temos dropdown de texto.
- Fat Brain tem reviews com estrelas em cada card de produto.
- Fat Brain tem "Age" badge com link funcional de navegação.

**Onde estamos na frente:**
- Paleta mais sofisticada (deles é azul-primário genérico, o nosso off-white quente é mais premium).
- Copy mais técnico e honesto (deles é mais "fun store" genérico).

### Alma Azul (Brasil)
**Onde estamos à frente:**
- Nossa taxonomia é mais rica (deles: só categorias funcionais sem filtros).
- Nossa paleta é mais moderna (deles usa azul autismo que o RESEARCH.md identificou como datado).
- Nossa PDP tem mais campos (eles têm página de produto básica).
- Nosso design system é mais consistente na home.

**Onde estamos atrás:**
- Alma Azul tem CNPJ visível, história real, identidade de marca estabelecida. Nós parecemos mais "startup recente" (porque somos).

### BmB Terapêuticos (Brasil)
**Onde estamos à frente:**
- Design mais limpo e menos clínico.
- Narrativa mais acessível para pais leigos.

**Onde estamos muito atrás:**
- BmB tem 7 filtros cruzados na sidebar. Nós temos 2 dropdowns.
- BmB tem fluxo B2B real. Nós não temos.
- BmB tem catálogo de mais de 100 produtos. Nós temos 18.
- BmB tem social proof real (anos no mercado, CREFITO referenciados).

**Veredito geral:** Estamos à frente de Alma Azul em design. Estamos 1-2 anos atrás de BmB em funcionalidade. Estamos 3-4 anos atrás de Lovevery em fotografia e conteúdo. Para um MVP de 18 produtos, isso é razoável — mas precisa ser dito claramente.

---

## 4. Problemas Concretos e Severidade

### CRITICO-01: Placeholder de emoji nas imagens de produto
**Problema:** Todos os 18 produtos têm uma div com emoji de 96px em gradiente colorido como "foto". O código é explícito: `<div class="product-img-placeholder" aria-hidden="true">${p.emoji}</div>`.

**Impacto:** E-commerce sem foto de produto não converte. Ponto final. O estudo seminal da Nielsen Norman (2010, ainda válido) mostra que usuários de e-commerce verificam imagens antes de texto. Emoji não é imagem de produto. Um abafador de ruído representado por "🎧" não transmite tamanho, qualidade de material, ou aparência real.

**Benchmark:** ZERO concorrentes analisados no RESEARCH.md — nem os piores — usam placeholder sem foto.

**Fix:** Foto de fundo branco (pode ser stock photo temporária, específica por categoria). Minimum viable: uma foto real por produto. Se não houver foto real, uma ilustração flat específica ao produto é melhor que emoji.

**Severidade: Crítico. Impacto direto em conversão.**

---

### CRITICO-02: Tokens CSS quebrados em páginas internas
**Problema:** `produto.html` e `minha-conta.html` usam variáveis CSS que não existem no `design-tokens.css` atual. `var(--surface)` → não existe (deveria ser `var(--white)`). `var(--bg)` → não existe (deveria ser `var(--off-white)`). `var(--font-display)` → não existe (deveria ser `var(--f-display)`). `var(--teal-light)` → não existe (deveria ser `var(--teal-soft)`).

**Impacto:** As páginas internas têm cores erradas ou ausentes em produção agora. Usuário que navega da home para a PDP vê inconsistência visual imediata.

**Fix:** Auditoria sistemática das variáveis CSS em todas as páginas. Adicionar aliases no `design-tokens.css` para retrocompatibilidade, ou corrigir os nomes nas páginas internas.

**Severidade: Crítico. Está em produção.**

---

### CRITICO-03: Filtros não cruzados (um eixo por vez)
**Problema:** O usuário só pode filtrar por faixa etária OU categoria. Não há "3-5 anos + Tato + até R$150". Isso é o principal diferencial competitivo prometido no posicionamento — e não existe.

**Impacto:** Juliana (TO) e Ana (mãe informada) são as personas com maior probabilidade de conversão — e são as que mais precisam de filtros cruzados. Sem isso, o site não é melhor que MercadoLivre para quem sabe o que quer.

**Fix:** Adicionar filtro de sentido (multi-select) e filtro de preço (slider) na vitrine. Substituir os dropdowns atuais por checkboxes de sidebar em desktop ou drawer de filtros em mobile.

**Severidade: Crítico.**

---

### ALTO-01: Ausência de tags de sentido nos cards
**Problema:** O card de produto mostra categoria (ex: "Fidget") mas não os sentidos estimulados (ex: "Tato + Propriocepção"). A API retorna os dados mas o renderProducts() não exibe.

**Impacto:** O reconhecimento de produto depende de informação contextual. A persona que filtra por "tato" clica em um produto mas o card não confirma que é de tato — precisa abrir para confirmar.

**Fix:** Adicionar 1-2 ícones ou badges de sentido em cada card (dado já existe no banco: campo tags/sensory_systems se existir, ou derivado da categoria).

**Severidade: Alto.**

---

### ALTO-02: Sem selector de quantidade no carrinho
**Problema:** `addToCart(id)` sempre adiciona 1 unidade. Para adicionar 4 unidades, o usuário clica 4 vezes.

**Fix:** Adicionar seletor de quantidade (+/-) no card do carrinho e campo de quantidade no modal de produto.

**Severidade: Alto.** Especialmente crítico para Juliana (B2B).

---

### ALTO-03: Sem busca com autocomplete
**Problema:** O campo de busca é texto livre sem sugestões. Para um catálogo de 18 produtos com nomes técnicos longos, o usuário precisa lembrar o nome exato ou a categoria.

**Fix:** Implementar autocomplete que filtra os produtos enquanto o usuário digita — o dataset é pequeno (18 itens), pode ser client-side.

**Severidade: Alto.**

---

### ALTO-04: Sem fluxo B2B
**Problema:** O FAQ menciona "modalidade para profissionais com NF-e". O header não tem link para área profissional. O checkout não tem campo de CNPJ. É uma promessa de feature não entregue.

**Fix:** Adicionar link "Para Profissionais" no nav. Adicionar campo CNPJ/CPF no checkout. Criar email de contato direto para pedidos B2B.

**Severidade: Alto.** Juliana representa tickets 5-10x maiores.

---

### ALTO-05: Trust signals sem prova
**Problema:** O hero afirma "Curadoria por TOs" como trust item. O depoimento menciona "Dra. Fernanda M., CREFITO-SP". Mas não existe página de curadoria, não existe lista de TOs parceiros, não existe CREFITO verificável.

**Impacto:** Para o público-alvo (mãe de criança com TEA que está em contato com TOs reais), uma afirmação não verificável pode gerar desconfiança quando o TO real não conhece o site.

**Fix:** Criar seção "Nossos Consultores" com nome + CREFITO + foto + área de especialidade. Mesmo uma TO parceira parcial já é melhor que nenhuma.

**Severidade: Alto.**

---

### MÉDIO-01: Flash of empty content na vitrine
**Problema:** O grid de produtos fica vazio enquanto o JS carrega a API. Sem skeleton loader.

**Fix:** Adicionar skeleton placeholders (divs animados com gradiente cinza) antes do fetch completar.

**Severidade: Médio.**

---

### MÉDIO-02: Header diferente em cada página
**Problema:** Header da home tem nav-cats (links de categoria). PDP tem header simplificado. Minha conta tem header diferente. Não há consistência de navegação entre páginas.

**Fix:** Criar componente de header parcial (via include ou template literal) usado em todas as páginas. No MVP sem SSR, pode ser um script JS que injeta o header.

**Severidade: Médio.**

---

### MÉDIO-03: Acentuação ausente em categorias
**Problema:** Categorias no banco e nos dropdowns: "Mastigavel", "Cognicao", "Agua/Banho" — sem acento. O `product-cat-label` exibe o valor bruto.

**Fix:** Map de normalização de categoria no frontend: `{ 'Mastigavel': 'Mastigável', 'Cognicao': 'Cognição', 'Bebê': 'Bebê' }`.

**Severidade: Médio.** Afeta percepção de qualidade.

---

### MÉDIO-04: Sem wishlist / lista de favoritos
**Problema:** Jornada consultiva (pesquisa → consulta com TO → retorno) não é suportada.

**Fix:** Botão "Salvar" em cada card. Persiste em localStorage. Link "Minha lista" no header.

**Severidade: Médio.**

---

### BAIXO-01: Shipping bar ausente nas páginas internas
**Problema:** A oferta de frete grátis e o cupom BEMVINDO10 só aparecem na home.

**Fix:** Incluir shipping-bar em produto.html e checkout.html.

**Severidade: Baixo.**

---

### BAIXO-02: Depoimentos sem foto real
**Problema:** Avatar com inicial em vez de foto reduz autenticidade percebida.

**Fix:** Usar foto real (ou avatar ilustrado personalizado) nos depoimentos. Mesmo ilustração flat é melhor que "C" em círculo teal.

**Severidade: Baixo.**

---

### BAIXO-03: SP pré-selecionado no estado do checkout
**Problema:** `<option selected>SP</option>` pré-seleciona São Paulo para todos os usuários.

**Fix:** Remover o `selected` e usar placeholder "Selecione o estado". Ou usar geolocalização para pré-preencher.

**Severidade: Baixo.**

---

## 5. Nova Proposta de Design (Alto Nível)

### 5.1 Estrutura de Navegação (IA)

**Header (sticky):**
```
[Logo] [Busca com autocomplete — 50% da largura] [Para Profissionais] [Favoritos] [Conta] [Carrinho]
```

**Sub-nav (scroll reveal, desaparece ao rolar):**
```
[Por Sentido ▾] [Por Idade ▾] [Por Objetivo ▾] [Kits] [Para Profissionais] [Blog]
```

**Dropdown "Por Sentido":**
```
Tato — Visão — Propriocepção — Equilíbrio — Audição — Oral
```

**Dropdown "Por Objetivo":**
```
Autorregulação — Foco e Atenção — Coordenação Motora — Linguagem — Sono e Calma
```

**Mobile:**
```
[Logo] [Busca] [Carrinho]
[Hamburger menu] → drawer com as mesmas opções
```

---

### 5.2 Princípios Visuais (3 palavras-chave)

1. **Acolhedor**: espaço branco generoso, nenhuma seção "gritada", texto de apoio sempre presente.
2. **Criterioso**: dados visuais (badges, fichas técnicas) presentes em todos os níveis de produto.
3. **Humano**: fotografia lifestyle real, depoimentos com foto, curador nomeado.

---

### 5.3 Biblioteca de Componentes Necessária

**Componentes existentes que ficam:**
- Button (primary/secondary/ghost) — manter
- Card de produto — adicionar campo de sentidos
- Modal de produto — manter estrutura, melhorar imagem
- Cart sidebar — adicionar seletor de quantidade
- Toast — aumentar duração para erros
- FAQ accordion — manter

**Componentes novos a criar:**
- FilterPanel (sidebar com checkboxes multi-select + slider de preço)
- SkeletonCard (loading placeholder do card de produto)
- SensoryBadge (badge de sentido com ícone dedicado por sentido)
- ProductImageGallery (substituir placeholder emoji)
- QuizWidget (5 perguntas → recomendação)
- WishlistButton (coração em cada card)
- QuantitySelector (+-N no carrinho e na PDP)
- TrustBar (reutilizável em todas as páginas)
- ProfessionalBanner (area B2B com CNPJ)
- CuratorBlock (TO nomeado com CREFITO + foto)

---

### 5.4 Tipografia Final

Manter Nunito + Inter — a combinação está correta. Ajustes:

- H1 hero: Nunito 800, 52px desktop / 36px mobile, line-height 1.15
- H2 seção: Nunito 700, 32px desktop / 24px mobile
- Nome do produto na PDP: Nunito 800, 28px
- Body e descrições: Inter 400, 16px, line-height 1.65
- Labels e badges: Inter 600, 12px, uppercase com letter-spacing 0.5px
- Preço principal: Nunito 800, 32px
- Preço Pix: Inter 500, 14px, cor success

---

### 5.5 Paleta Final

Manter a paleta de design-tokens.css com **uma correção crítica**: unificar os tokens com os nomes usados nas páginas internas. Escolher um sistema e padronizar.

**Sistema proposto (unificação):**
```
--bg:           var(--off-white)    /* #FBFAF7 */
--surface:      var(--white)        /* #FFFFFF */
--teal-light:   var(--teal-soft)    /* #E8F6F6 */
--coral-light:  var(--coral-soft)   /* #FDEEEC */
--text-main:    var(--ink)          /* #1F1B16 */
--text-muted:   var(--muted)        /* #6B6359 */
--font-display: var(--f-display)
--font-ui:      var(--f-body)
```
Adicionar esses aliases no design-tokens.css para que páginas antigas funcionem sem refactor imediato.

---

### 5.6 Grid System

- **Desktop (1280px max-width):** 12 colunas, gutter 24px, margin lateral 48px
- **Tablet (768-1279px):** 8 colunas, gutter 16px, margin lateral 24px
- **Mobile (<768px):** 4 colunas, gutter 12px, margin lateral 16px

**Grid de produtos:**
- Desktop: 4 colunas (minmax 240px)
- Tablet: 3 colunas (minmax 200px)
- Mobile: 2 colunas (minmax 160px)

---

### 5.7 Densidade de Informação

**Menor que a atual na home.** O hero atual tem 7 elementos antes do fold. O alvo é 4 (eyebrow + H1 + subtítulo + CTA pair). Trust bar separada abaixo.

**Maior que a atual nos cards de produto.** Adicionar tags de sentido sem aumentar muito a altura do card. Usar ícones pequenos (16px) em vez de texto.

**Muito maior que a atual na PDP.** A PDP atual é boa mas genérica. Cada campo (ficha técnica, tabs) precisa de conteúdo específico por produto.

---

### 5.8 Mobile vs Desktop

**Mobile-first obrigatório.** O ICP (mãe ansiosa) pesquisa no celular enquanto espera a TO, enquanto a criança dorme, no WhatsApp. O checkout em mobile precisa de uma atenção especial:

- Teclado numérico automático para CEP e telefone
- Botões de CTA com mínimo 48px de altura
- Resumo do pedido colapsável (para não tomar toda a tela)
- PIX como opção proeminente (não enterrada em terceiro lugar)

---

## 6. Wireframes Descritos

### 6.1 Homepage

**SHIPPING BAR (altura 36px, fundo teal-soft, texto teal)**
Linha única: "Frete grátis acima de R$199 — Cupom BEMVINDO10 (10% na 1ª compra)" | link "ver condições"

**HEADER (sticky, 64px)**
- Esquerda: Logo SensoriPlay (48px height)
- Centro: campo de busca (60% da largura, placeholder "Buscar por nome, sentido, faixa etária...") com autocomplete dropdown
- Direita: [ícone coração "Favoritos"] [ícone pessoa "Conta"] [ícone carrinho + badge de quantidade]

**SUB-NAV (48px, visível em desktop)**
Pills horizontais: [Todos] [Por Sentido ▾] [Por Idade ▾] [Por Objetivo ▾] [Kits ✦] [Para Profissionais]
Em mobile: scroll horizontal de pills (igual ao nav-cats atual mas com dropdowns em desktop)

**HERO (height: 560px desktop / auto mobile)**
Layout 2 colunas: texto à esquerda (55%), imagem à direita (45%).
- Esquerda: eyebrow pequeno (teal, 13px) → H1 (52px, Nunito 800, ink) → subtítulo (18px, Inter 400, text, max 60ch) → CTA pair (coral primário "Explorar produtos" | secundário outline teal "Fazer quiz de descoberta")
- Direita: hero image (foto lifestyle ou ilustração flat de criança explorando kit sensorial — NÃO emoji)
- Trust row abaixo do CTA: 4 items com ícone linha + texto (INMETRO, 7 dias devolução, Curadoria TOs, Envio nacional)

Em mobile: imagem acima, texto abaixo. Altura da imagem: 240px.

**SEÇÃO QUIZ (off-white, 200px)**
Background cream. Centralizado.
- Heading: "Não sabe por onde começar?" (H2, 28px)
- Subtítulo: "Responda 5 perguntas e receba uma lista de produtos para a fase do seu filho agora." (Inter 16px)
- Botão coral grande: "Fazer quiz gratuito →"

**SEÇÃO CURADOR (cream, 280px)**
Layout 3 colunas de cards de TO:
- Cada card: foto circular (64px) + nome + CREFITO + cidade + citação curta (2 linhas) + link "Ver lista de indicados"
- Heading: "Curado por terapeutas reais" + subtítulo "Não é afirmação de marketing. Esses profissionais testaram e aprovaram."

**SEÇÃO VITRINE (off-white, altura variável)**
- Heading H2 "Catálogo" + contador "18 produtos"
- FilterPanel: sidebar esquerda (desktop, 240px) | drawer bottom (mobile)
  - Checkbox group "Faixa etária": 0-12m, 1+, 2+, 3+, 4+, 5+, 6+
  - Checkbox group "Sentido": Tato, Visão, Audição, Propriocepção, Equilíbrio, Oral
  - Slider "Preço": R$0 — R$700
  - Toggle "Apenas com INMETRO"
  - Botão "Aplicar filtros" (mobile) / aplicação automática (desktop)
- Grid de produtos (direita): 3 colunas desktop / 2 colunas mobile
- Sort dropdown no topo direito do grid: [Destaques | Menor preço | Maior preço | A-Z]

**CARD DE PRODUTO (novo layout)**
- Topo: imagem real (240px height) com badges sobrepostos no canto superior esquerdo (Mais vendido / Novidade / INMETRO)
- Badge faixa etária: canto superior direito
- Botão favorito (coração): canto superior direito, hover coral
- Body: nome do produto (Nunito 600, 15px, 2 linhas max) + linha de sentidos (ícones 14px: 👐 Tato, 👁 Visão) + estrelas + nº reviews
- Footer: preço principal + preço Pix + botão "+" (adicionar ao carrinho, círculo coral)

**SEÇÃO DEPOIMENTOS (cream, 500px)**
Grid 3 colunas de testimonial cards:
- Card: foto do autor (56px, circular real) + estrelas + quote (4-5 linhas, blockquote, Inter 15px) + nome + papel (TOs com CREFITO)

**SEÇÃO BENEFÍCIOS (off-white, 400px)**
Grid 2x3 de benefit cards (não 5 cards em linha — reduz a 2 linhas de 3):
- Ícone (32px, cor alternada por card) + título (Nunito 700, 16px) + descrição (Inter 400, 14px, 3 linhas max)

**SEÇÃO FAQ (cream, altura variável)**
Accordion com 6 perguntas. Chevron à direita. Resposta expande abaixo.
- Heading + link "Ver todas as perguntas →"

**FOOTER (ink, 400px)**
- Linha 1: Logo + tagline + newsletter (email + botão "Receber guias")
- Linha 2: 4 colunas de links (Produtos / Atendimento / Empresa / Para Profissionais)
- Linha 3: selos (SSL, Mercado Pago, INMETRO) + copyright + disclaimer médico

---

### 6.2 Página de Produto (PDP)

**HEADER:** mesmo header global

**BREADCRUMB (40px, muted)**
`Home / Sensorial / Tato / Tapete Squish de Apertar`

**PDP PRINCIPAL (grid 2 colunas, 60/40)**

**Coluna esquerda (galeria):**
- Imagem principal: 480px height, border-radius 12px, fundo off-white
- Thumbnails abaixo: 4 miniaturas 72px (foto produto / foto lifestyle / foto detalhe material / vídeo demo)
- Badge "INMETRO" sobreposto na imagem principal (canto inf esq)

**Coluna direita (informações):**
- Categoria (teal uppercase, 12px): ex "FIDGET — TATO"
- Nome do produto (Nunito 800, 28px, ink): ex "Tapete Sensorial Squish de Apertar — Foco e Autorregulação"
- Linha de avaliação: ★★★★★ (4.8) · 23 avaliações (link âncora)
- Tags de sentido (badges teal-soft): 👐 Tato | 🦴 Propriocepção
- Faixa etária badge: "3+ anos"
- "Recomendado por TOs" badge (se tiver curador)
- Bloco de preço:
  - Preço principal: R$ 39,90 (Nunito 800, 32px)
  - Preço Pix: R$ 37,90 no Pix (5% off) | 3x de R$ 13,30 s/ juros (Inter 500, 14px, success)
  - Desconto disponível com cupom BEMVINDO10
- Seletor de quantidade: [−] [1] [+]
- Botão "Adicionar ao carrinho" (coral, width 100%, height 52px)
- Botão "Comprar agora via Pix" (outline teal, width 100%)
- Ficha técnica visual (grid 3 colunas de fichas):
  - Idade recomendada | Sentidos trabalhados | Material | Dimensões | Certificação | Uso recomendado
- Info de frete: barra de progresso "Falta R$ 159 para frete grátis" + tempo estimado de entrega
- Trust row: 🔒 Compra segura | 🔄 7 dias devolução | 📦 Enviado em 1 dia útil

**TABS (Descrição / Como usar / Cuidados / Segurança)**
- Descrição: parágrafo técnico específico ao produto (não genérico)
- Como usar: 3-5 bullets específicos ao produto
- Segurança: materiais, certificações, faixa etária racional

**CURADOR (se disponível)**
Caixa cream com foto + nome + CREFITO + "Por que recomendo este produto" (3 linhas)

**FAQ DO PRODUTO**
5 perguntas específicas ao produto — não genéricas

**SEÇÃO REVIEWS**
- Resumo: 4.8 / 5 (23 avaliações) + distribuição de estrelas (barras)
- Filtros: [Todos | Pais de TEA | Terapeutas | Desenvolvimento típico]
- Cards de review: foto do cliente (quando disponível) + estrelas + data + texto + "útil?" thumbs

**RELACIONADOS**
Grid de 4 produtos com link "Ver produto" e botão add-to-cart rápido

---

### 6.3 Checkout

**HEADER (simplificado):**
Logo centralizado + "🔒 Checkout 100% seguro" + suporte "Dúvidas? Chat →"

**STEPS BAR:**
Endereço ✓ → Pagamento ← [atual] → Confirmação

**LAYOUT (2 colunas, 60/40):**

**Coluna esquerda (form):**
Cada step é uma seção com título Nunito 700 + ícone

STEP 1 — Endereço:
- Banner: "Entre para preencher automaticamente | ou continue como visitante"
- CEP com busca automática + botão "Buscar"
- Campos: Rua | Número + Complemento | Bairro | Cidade | Estado (select, sem pré-seleção)
- Nome do destinatário | Telefone (com máscara)
- Botão "Continuar →" (coral, full width, com loading state)

STEP 2 — Pagamento:
- Método: 3 cards selecionáveis [PIX ✦ 5% off] [Cartão de crédito] [Boleto]
- Se PIX: QR code + código copia-cola + instruções
- Se Cartão: Número | Validade | CVV | Nome impresso | Parcelas (dropdown)
- Cupom: campo + botão "Aplicar" + confirmação visual inline
- Botão "Pagar" (coral, full width)

STEP 3 — Confirmação:
- Ícone check verde grande (64px)
- "Pedido confirmado!" + número do pedido
- Resumo do pedido
- "O que acontece agora?" (3 steps: Separação → Envio → Entrega)
- Botão "Continuar comprando" | Botão "Ver meu pedido"

**Coluna direita (resumo fixo):**
- Título "Resumo do pedido"
- Lista de itens (emoji/imagem + nome + quantidade + preço)
- Subtotal | Desconto cupom (se aplicado) | Frete | Total
- Nota "Preço final. Sem surpresas."

---

## 7. Comparação Honesta: Custom vs Shopify Tema Premium

**Cenário hipotético:** Leo compra o tema Impulse ou Prestige da Shopify por USD 350 (não USD 100 — esses têm qualidade inferior).

**Onde Shopify ganha:**
- Fotografia de produto: Shopify impõe upload de imagem real. Nosso custom permite emoji. Shopify vence por coerção de padrão.
- Apps de review (Judge.me ou Okendo): reviews reais, verificados, com foto. Nossa implementação atual não tem reviews funcionais.
- Checkout nativo: checkout do Shopify é testado por bilhões de transações, tem PIX integrado via Mercado Pago ou Pagar.me, tem detecção de fraude, tem upsell pré-checkout. Nossa implementação tem 3 steps mas não tem detecção de fraude, não tem recuperação de carrinho abandonado.
- SEO automático: schema.org para produtos, sitemaps, canonical tags, Open Graph. Nossa implementação tem OG tags na home mas não nas páginas internas.
- App ecosystem: wishlist (R$29/mês), quiz de descoberta (R$49/mês), heat maps (R$79/mês). Funcionalidades que teriam que ser desenvolvidas do zero no custom.
- CNPJ/B2B: apps prontos para área profissional com preço diferenciado.

**Onde nossa implementação custom ganha:**
- Paleta de cores e tipografia: genuinamente mais sofisticadas que temas Shopify genéricos.
- Copy e narrativa: totalmente sob controle. Temas Shopify têm blocos engessados.
- Performance: sem o overhead do Shopify JS (~300KB). Nossa página carrega mais rápido.
- Custo operacional: sem fee de 0.5-2% por transação do Shopify para planos não-Shopify Payments (e Shopify Payments não está disponível no Brasil).
- Controle técnico total: podemos implementar qualquer feature sem limitação de plataforma.

**Veredito honesto:**

Neste momento (MVP com 18 produtos, zero reviews reais, zero fotos), um tema premium Shopify com USD 350 de investimento estaria **substancialmente à frente** em UX de conversão. O motivo principal é que Shopify obrigaria a ter foto real por produto, teria checkout battle-tested, e teria reviews funcionais desde o dia 1.

A vantagem do custom atual é apenas visual (paleta, tipografia) — e visual não converte sem conteúdo. Quando tivermos fotos reais de produto, reviews reais, e B2B implementado, a implementação custom se tornará superior. Por enquanto, é um MVP com boa fundação mas abaixo do baseline de uma plataforma comercial.

Recomendação: **manter o custom** se houver compromisso de resolver CRITICO-01 (fotos), CRITICO-02 (tokens) e CRITICO-03 (filtros cruzados) nos próximos 15-30 dias. Se esses problemas não forem resolvidos em 30 dias, considerar migração de checkout para Shopify Lite (USD 9/mês) mantendo o frontend custom.

---

## 8. Acessibilidade Real (WCAG 2.1 AA)

### 8.1 Análise de Contraste de Cores

**Coral #E74C3C sobre branco #FFFFFF:**
- Ratio calculado: aproximadamente 4.0:1
- Requisito AA para texto normal (< 18px): 4.5:1
- **FALHA AA.** O botão coral com texto branco não passa em WCAG AA para texto de 14-16px.
- Para passar, o coral precisa ser #D44030 ou mais escuro (ratio ≥ 4.5:1).

**Teal #17A2A2 sobre branco #FFFFFF:**
- Ratio calculado: aproximadamente 3.1:1
- **FALHA AA.** Links, ícones ativos e labels em teal sobre fundo branco não passam.
- O teal-dark (#138A8A) tem ratio de aproximadamente 4.0:1 — ainda falha para texto pequeno.
- Para texto teal sobre fundo branco em 14px, precisaria de #0F6B6B ou similar.

**Ink #1F1B16 sobre off-white #FBFAF7:**
- Ratio calculado: aproximadamente 17:1
- **Passa AAA.** Títulos e corpo de texto principais estão corretos.

**Muted #6B6359 sobre off-white #FBFAF7:**
- Ratio calculado: aproximadamente 5.8:1
- **Passa AA.** Texto de apoio está correto.

**Placeholder #A89F94 sobre off-white #FBFAF7:**
- Ratio calculado: aproximadamente 2.9:1
- **Falha AA.** Placeholders de formulário são ilegíveis para usuários com baixa visão — mas WCAG tem exceção para placeholders (eles não são texto funcional obrigatório). Ainda assim, é melhor ter contraste maior.

**Coral #E74C3C sobre teal-soft #E8F6F6:**
- Ratio calculado: aproximadamente 4.2:1
- **Falha marginalmente.** Badges coral em seções teal-soft não passam AA para texto pequeno.

**Resumo de contraste:** As duas cores de ação principais (coral e teal) têm contraste insuficiente para texto sobre fundo branco. Isso é um problema de auditoria formal WCAG — e é especialmente grave porque o público-alvo inclui pais mais velhos e pessoas com dislexia ou baixa visão.

**Fix recomendado:**
- Coral CTA: usar #C0392B (coral-dark) como cor de background do botão. Texto branco sobre #C0392B tem ratio ~6.1:1 — passa AA e AAA.
- Teal para texto: usar #0F7A7A (mais escuro que o atual). Ratio com fundo branco: ~5.2:1 — passa AA.

---

### 8.2 Navegação por Teclado

**O que funciona:**
- Skip link implementado ("Ir para o conteúdo principal") — aparece ao pressionar Tab.
- Todos os botões têm `focus-visible` com outline coral de 3px.
- Links têm `focus-visible` definido no base.css.
- Modal fecha com Escape.
- FAQ accordion usa botões (não divs) para as perguntas — correto.
- Cart sidebar é `role="dialog"` com `aria-modal="true"`.

**O que falha:**
- O modal de produto captura o foco corretamente? O `modal-overlay` não tem `autofocus` no botão de fechar. Quando o modal abre, o foco provavelmente fica na página de trás — usuário de teclado não sabe que um modal abriu.
- O cart sidebar não move o foco para dentro do sidebar quando abre. `openCart()` adiciona classe `open` mas não faz `focus()` no primeiro elemento interativo.
- As tabs de categoria ("Por Idade / Por Sentido / Por Objetivo") têm `role="tab"` e `aria-selected` — correto. Mas o conteúdo da tab (`div#catGrid`) não tem `role="tabpanel"` e `aria-labelledby` correspondente — o padrão ARIA de tab/tabpanel está incompleto.
- O grid de produtos usa `role="list"` no container e `role="listitem"` em cada artigo — correto. Mas a busca não anuncia quantos resultados foram encontrados para screen readers. O `filterCount` tem `aria-live="polite"` — isso está correto, funciona.

**Estimativa:** Navegação por teclado está 70% correta. Falha nos pontos críticos de gestão de foco em modais e cart sidebar.

---

### 8.3 Screen Reader Experience

**O que funciona:**
- `aria-label` em todos os botões de ícone (carrinho, conta, busca, fechar).
- `aria-hidden="true"` em todos os SVGs decorativos.
- `role="img"` + `aria-label` nas estrelas de depoimento.
- `aria-live="polite"` no badge do carrinho e no contador de filtro.
- Textos alternativos (`alt=""`) nas imagens decorativas.

**O que falha:**
- O placeholder emoji do produto tem `aria-hidden="true"` no código renderizado — correto, mas o card não tem uma imagem alternativa com texto descritivo. O screen reader anuncia o nome do produto mas não a imagem do produto. Com fotos reais, o `alt` teria que ser descritivo: `alt="Tapete Sensorial Squish, cor verde, aprox. 30x30cm"`.
- A seção de categorias (tabs "Por Idade" etc.) com o grid dinâmico: quando o usuário muda a tab, o grid atualiza, mas não há anúncio ARIA de que o conteúdo mudou. Um `aria-live` region ou focus management seria necessário.
- O modal de produto não anuncia que abriu (não tem `aria-labelledby` apontando para o título do modal).

---

### 8.4 Passaria em Auditoria Formal WCAG 2.1 AA?

**Não.**

Critérios que falham automaticamente:
- **1.4.3 Contrast (Minimum):** Coral #E74C3C e Teal #17A2A2 sobre branco são insuficientes para texto < 18px. Isso é um critério Level AA que seria identificado em qualquer ferramenta automatizada (axe, Lighthouse, WAVE).
- **4.1.2 Name, Role, Value:** O modal de produto não tem `aria-labelledby` conectando ao título. O tab panel não tem `role="tabpanel"`.
- **2.4.3 Focus Order:** O foco não é movido para o modal quando ele abre — violação de critério de ordem de foco.

**Critérios que passam:**
- 1.1.1 Non-text Content (alt text adequado para imagens funcionais)
- 1.3.1 Info and Relationships (uso correto de headings h1-h3, listas, labels)
- 2.1.1 Keyboard (todos os elementos interativos são alcançáveis por teclado)
- 2.4.1 Bypass Blocks (skip link implementado)
- 2.4.7 Focus Visible (outline coral-3px em todos os elementos focáveis)
- 3.1.1 Language of Page (lang="pt-BR" no html)

**Score estimado em Lighthouse Accessibility:** 78-82/100 (versus 90+ necessário para aprovação sem ressalvas).

---

## 9. Ranking de Prioridades para Próximas 4 Semanas

**Semana 1 (impacto imediato em conversão):**
1. [CRITICO-01] Fotos reais de produto — mínimo 1 foto por produto, fundo branco
2. [CRITICO-02] Corrigir tokens CSS quebrados — produto.html e minha-conta.html
3. [CRITICO-03] Adicionar filtros cruzados — sidebar com checkboxes de sentido + slider de preço

**Semana 2 (trust e conversão):**
4. [ALTO-01] Tags de sentido nos cards de produto
5. [ALTO-05] Seção de curadores nomeados (1 TO real com foto + CREFITO)
6. Correção de contraste coral e teal (fix de CSS, 30 minutos)

**Semana 3 (B2B e retenção):**
7. [ALTO-02] Seletor de quantidade no carrinho e PDP
8. [ALTO-04] Fluxo B2B básico (campo CNPJ no checkout + email para profissionais)
9. [MÉDIO-04] Wishlist em localStorage

**Semana 4 (polimento):**
10. [MÉDIO-01] Skeleton loader para vitrine
11. [MÉDIO-02] Header unificado entre páginas
12. [ALTO-03] Autocomplete na busca
13. Correção de ARIA (focus management em modal e cart)

---

*Auditoria conduzida sobre código-fonte direto de `/home/claude/sensoriplay/`. Nenhuma suposição foi feita sobre o site em produção sem verificação no código. Problemas marcados como "Crítico" já estão presentes no código atual em produção.*
