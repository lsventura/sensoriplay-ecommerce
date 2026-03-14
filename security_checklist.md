# Checklist de Segurança - SensoriPlay

Este checklist resume os pontos mínimos de segurança para o e-commerce SensoriPlay (frontend HTML/JS, backend FastAPI em Python e banco PostgreSQL).

## 1. Credenciais e Segredos

- [ ] NUNCA commitar senhas, tokens ou chaves de API no repositório.
- [ ] Usar variáveis de ambiente para:
  - `DATABASE_URL`
  - `SECRET_KEY`
  - Tokens do Mercado Pago (ACCESS_TOKEN, PUBLIC_KEY, etc.)
- [ ] Garantir que `.env` está no `.gitignore`.
- [ ] No servidor, configurar as variáveis via painel do provedor (Railway, Render, Fly.io, etc.).

## 2. Senhas e Autenticação

- [ ] Armazenar senhas somente com **hash forte** (ex.: `bcrypt`).
- [ ] Nunca salvar senha em texto puro no banco ou logs.
- [ ] Implementar limite de tentativas de login (rate limiting) para evitar brute-force.
- [ ] Usar tokens de sessão/JWT com:
  - `SECRET_KEY` forte e aleatória.
  - Expiração curta para tokens sensíveis.

## 3. Banco de Dados (PostgreSQL)

- [ ] Usar usuário de banco com **permissões mínimas** (sem ser `postgres` superuser em produção).
- [ ] Usar **prepared statements** / ORM (SQLAlchemy) para evitar SQL Injection.
- [ ] Nunca concatenar strings de usuário diretamente em queries SQL.
- [ ] Habilitar SSL na conexão com o banco (quando disponível no provedor).
- [ ] Fazer backup periódico do banco (automático pelo provedor ou via script).

## 4. FastAPI / Backend

- [ ] Validar todos os inputs com **Pydantic** (modelos para request body, query params e path params).
- [ ] Retornar erros genéricos (não vazar stack trace ou detalhes internos em produção).
- [ ] Tratar exceções globais com handler customizado.
- [ ] Sanitizar/validar dados de CEP, e-mails, nomes, etc.
- [ ] Não expor endpoints administrativos sem autenticação/autorização.
- [ ] Manter dependências atualizadas (rodar `pip list --outdated` periodicamente).

## 5. CORS e Frontend

- [ ] Configurar CORS no FastAPI permitindo SOMENTE domínios de produção, por exemplo:
  - `https://sensoriplay.com.br`
  - `https://www.sensoriplay.com.br`
- [ ] Evitar `allow_origins=['*']` em produção.
- [ ] Garantir que o frontend sempre consome a API via **HTTPS**.

## 6. Mercado Pago (Pagamentos)

- [ ] Usar credenciais de **produção** separadas das de **sandbox**.
- [ ] Nunca expor o **Access Token** no frontend (somente no backend).
- [ ] Validar notificações de **webhook** do Mercado Pago:
  - Verificar assinatura/cabecalhos de segurança.
  - Confirmar status do pagamento chamando a API do Mercado Pago antes de marcar pedido como "pago".
- [ ] Tratar somente estados esperados (`approved`, `pending`, `rejected`).
- [ ] Logar ID da transação, status e horário (sem dados sensíveis de cartão).

## 7. Rate Limiting e Proteção contra Abuso

- [ ] Aplicar **rate limiting** em rotas sensíveis:
  - `/login`
  - `/checkout`
  - endpoints de criação/alteração de dados.
- [ ] Bloquear/limitar IPs com comportamento suspeito (muitas requisições em pouco tempo).

## 8. Logs e Monitoramento

- [ ] Nunca logar senhas, tokens, dados de cartão ou dados pessoais sensíveis.
- [ ] Centralizar logs do backend (stdout + ferramenta do provedor ou stack própria).
- [ ] Monitorar erros HTTP 4xx/5xx e tempo de resposta.
- [ ] Configurar alertas para falhas críticas (ex.: pagamento não conseguindo criar preferência, erro de conexão com banco).

## 9. Admin e Painel Interno

- [ ] Criar usuários **admin** apenas via banco/script seguro (nunca via formulário público).
- [ ] Proteger rotas administrativas com autenticação forte.
- [ ] Registrar auditoria básica (quem alterou status de pedido, quando, e de quê para quê).

## 10. Deploy e Infraestrutura

- [ ] Forçar HTTPS (provedor normalmente já cuida disso, mas conferir redirecionamento HTTP→HTTPS).
- [ ] Não expor porta do banco de dados publicamente (usar rede interna do provedor quando possível).
- [ ] Separar ambientes `dev` e `prod` (bancos e credenciais diferentes).
- [ ] Revisar permissões de acesso ao painel do provedor (apenas contas necessárias).

## 11. Checklist Antes de Ir pra Produção

- [ ] `.env` criado localmente e **NÃO** commitado.
- [ ] Variáveis de ambiente configuradas no provedor.
- [ ] Senhas com hash `bcrypt` funcionando.
- [ ] CORS restrito aos domínios oficiais.
- [ ] Integração Mercado Pago testada em sandbox.
- [ ] Webhook do Mercado Pago testado e validado.
- [ ] Usuário admin criado manualmente e login testado.
- [ ] Backup do banco configurado.
- [ ] Logs básicos funcionando em produção.

> Use este arquivo como referência sempre que for ajustar o backend, criar novas rotas ou configurar um novo ambiente (dev/homolog/prod).