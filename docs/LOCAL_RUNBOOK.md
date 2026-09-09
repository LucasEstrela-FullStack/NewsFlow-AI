# Guia de validação local

Este guia é a referência operacional do NewFlow AI para desenvolvimento e
revisão de pull requests.

## Antes de executar

- Crie `.env` a partir de `.env.example`; o arquivo é ignorado pelo Git.
- Escolha uma senha local para `POSTGRES_PASSWORD`.
- Atualize `DATABASE_URL` para usar essa mesma senha.
- Para o digest real, configure valores válidos de SMTP e um destinatário.
- Não inclua senhas, tokens ou URLs com credenciais em commits, issues ou logs.

## Verificação rápida da aplicação web

```bash
python run.py
curl http://127.0.0.1:5000/health
```

O endpoint deve responder com HTTP 200 e o corpo:

```json
{"service":"newflow","status":"ok"}
```

## Verificação do banco local

```bash
docker compose up -d database
docker compose ps
```

O serviço `database` deve ficar saudável. Quando o job diário for executado,
ele cria as tabelas `articles`, `digest_deliveries` e
`digest_delivery_articles` se necessário.

## Execução do digest

```bash
python -m app.jobs.daily_digest
```

O comando acessa feeds e SMTP reais. Execute-o somente com variáveis de ambiente
preenchidas e credenciais autorizadas. A repetição para o mesmo destinatário e
dia não deve enviar outro e-mail.

## Checklist de pull request

- [ ] `python -m pytest` conclui sem falhas.
- [ ] `python -m compileall -q app config.py` conclui sem erros.
- [ ] `git diff --check` não encontra espaços ou quebras inválidas.
- [ ] O README continua compatível com o comportamento implementado.
- [ ] `.env` e dados sensíveis não estão no diff.
- [ ] A alteração usa uma branch dedicada e um commit convencional.
- [ ] O workflow de CI passa no pull request.

## Quando algo falhar

1. Confirme que o ambiente virtual está ativo e as dependências foram instaladas.
2. Confirme que o PostgreSQL está saudável e que `DATABASE_URL` aponta para ele.
3. Verifique os nomes das variáveis em `.env`, sem compartilhar valores secretos.
4. Para o job, diferencie falhas externas de feed ou SMTP das falhas da aplicação.
5. Consulte os testes que cobrem o componente antes de alterar a regra de negócio.
