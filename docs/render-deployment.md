# Deploy no Render

O projeto é implantado como um Web Service Python usando o arquivo `render.yaml`.

## Criar o serviço

1. No painel do Render, selecione **New > Blueprint**.
2. Conecte o repositório `NewsFlow-AI`.
3. Selecione a branch `main` e confirme a criação do serviço `newflow-ai`.
4. Preencha as variáveis marcadas como secret no painel antes do primeiro deploy.

O Render instala as dependências com `pip install -r requirements.txt`, inicia a aplicação com Gunicorn e verifica `GET /health` antes de encaminhar tráfego.

## Variáveis de ambiente

| Variável | Uso |
| --- | --- |
| `SECRET_KEY` | Chave secreta da aplicação Flask. |
| `DATABASE_URL` | URL de conexão do PostgreSQL de produção. |
| `SMTP_HOST` | Servidor SMTP do provedor de e-mail. |
| `SMTP_PORT` | Porta SMTP com SSL, normalmente `465`. |
| `SMTP_USERNAME` | Usuário ou endereço de e-mail autenticado. |
| `SMTP_PASSWORD` | Senha de aplicativo ou credencial SMTP. |
| `SMTP_SENDER` | Remetente exibido nas mensagens. |

`NEWFLOW_ENV=production` e `NEWFLOW_DEBUG=false` já são definidos pelo Blueprint.

## Validação e rollback

Após o deploy, acesse `https://<seu-servico>.onrender.com/health`. A resposta esperada é `{"service":"newflow","status":"ok"}`.

Em caso de falha, consulte os logs do serviço e use **Manual Deploy > Deploy latest successful commit** no painel do Render para retornar à versão anterior.
