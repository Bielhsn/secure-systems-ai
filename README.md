Aqui está um README completo, consolidando IADT + SOAT, alinhado com tudo que você implementou.

# Secure Systems AI

## Hackathon Integrado - IA para Devs (IADT) + Software Architecture (SOAT)

---

# Descrição do Problema

Empresas que operam sistemas distribuídos utilizam diversos diagramas arquiteturais para:

* revisões técnicas;
* auditorias de segurança;
* avaliações de escalabilidade;
* discussões arquiteturais entre times.

Esses diagramas normalmente são analisados manualmente, exigindo:

* alto tempo operacional;
* especialistas técnicos;
* processos pouco escaláveis;
* validações repetitivas.

A proposta do projeto é automatizar a análise técnica desses diagramas utilizando Inteligência Artificial multimodal.

---

# Objetivo da Solução

Desenvolver um sistema capaz de:

* receber diagramas arquiteturais;
* processar arquivos de imagem e PDF;
* aplicar IA para análise automática;
* identificar componentes arquiteturais;
* identificar riscos técnicos;
* gerar recomendações;
* produzir relatório técnico em PDF.

---

# Arquitetura da Solução

A solução foi desenvolvida utilizando uma arquitetura desacoplada baseada em serviços.

## Componentes principais

### API Gateway (FastAPI)

Responsável por:

* receber uploads;
* validar arquivos;
* criar jobs;
* consultar status;
* disponibilizar relatórios.

---

### RabbitMQ

Responsável por:

* mensageria assíncrona;
* desacoplamento do processamento;
* distribuição de jobs.

---

### Worker de Processamento

Responsável por:

* consumir jobs da fila;
* acionar a IA;
* processar diagramas;
* gerar relatórios;
* atualizar status.

---

### PostgreSQL

Responsável por:

* persistência dos jobs;
* persistência de status;
* persistência dos resultados;
* persistência dos relatórios.

---

### Gemini Multimodal AI

Responsável por:

* interpretação visual dos diagramas;
* identificação de componentes;
* classificação de riscos;
* recomendações arquiteturais;
* geração estruturada de saída.

---

# Fluxo da Aplicação

```text id="5v4z8j"
Upload do Diagrama
        ↓
API Gateway (FastAPI)
        ↓
Persistência PostgreSQL
        ↓
Publicação no RabbitMQ
        ↓
Worker Assíncrono
        ↓
Gemini Multimodal
        ↓
Análise Arquitetural
        ↓
Geração de PDF
        ↓
Persistência do Relatório
        ↓
Download do PDF
```

---

# Diagrama de Arquitetura

```mermaid
flowchart TD

    User[Usuário] -->|Upload de diagrama| API[API Gateway - FastAPI]

    API -->|Valida arquivo| Upload[Upload Service]
    Upload -->|Salva arquivo| Storage[(Storage Local)]
    Upload -->|Cria job| DB[(PostgreSQL)]
    Upload -->|Publica job_id| Queue[(RabbitMQ)]

    Queue -->|Consome mensagem| Worker[Processing Worker]

    Worker -->|Busca job| DB
    Worker -->|Envia imagem| Gemini[Gemini Multimodal AI]
    Gemini -->|Retorna JSON estruturado| Worker

    Worker -->|Gera PDF| Report[Report Service]
    Report -->|Salva relatório| Reports[(Reports Storage)]

    Worker -->|Atualiza status e resultado| DB

    API -->|Consulta status| DB
    API -->|Download relatório| Reports

    User -->|Consulta status| API
    User -->|Download PDF| API
```

---

# Tecnologias Utilizadas

## Backend

* Python 3.11
* FastAPI
* Uvicorn

---

## Banco de Dados

* PostgreSQL
* SQLAlchemy

---

## Mensageria

* RabbitMQ
* Pika

---

## Inteligência Artificial

* Google Gemini 2.5 Flash
* Gemini Multimodal API

---

## Relatórios

* ReportLab

---

## Infraestrutura

* Docker
* Docker Compose

---

## Testes

* Pytest

---

# Endpoints

## Health Check

```http id="q37h6n"
GET /
```

---

## Upload de Diagrama

```http id="s9t1o6"
POST /upload
```

Tipos aceitos:

* PNG
* JPG
* JPEG
* PDF

---

## Consulta de Status

```http id="r6q6ht"
GET /status/{job_id}
```

Status possíveis:

* RECEIVED
* PROCESSING
* DONE
* ERROR

---

## Download do Relatório

```http id="lb0vb7"
GET /report/{job_id}
```

---

# Pipeline de Inteligência Artificial

A solução utiliza um pipeline multimodal baseado em Large Language Models.

## Fluxo de IA

```text id="vb53v8"
Imagem/PDF
    ↓
Gemini Vision
    ↓
Análise Arquitetural
    ↓
Classificação de Riscos
    ↓
Recomendações Técnicas
    ↓
JSON Estruturado
    ↓
Geração de PDF
```

---

# Estratégia de IA

O projeto utiliza:

* prompt engineering;
* saída estruturada em JSON;
* guardrails básicos;
* validação de formato;
* tratamento de erros do modelo.

A IA foi configurada para:

* identificar componentes;
* identificar riscos;
* sugerir melhorias;
* calcular score arquitetural.

---

# Segurança

## Validação de Arquivos

O sistema permite apenas:

* `.png`
* `.jpg`
* `.jpeg`
* `.pdf`

Arquivos inválidos são rejeitados.

---

## Tratamento de Entradas Não Confiáveis

Foram implementadas:

* validação de extensão;
* isolamento de uploads;
* geração de nomes internos;
* tratamento de exceções.

---

## Uso Controlado da IA

A IA opera utilizando:

* restrição de saída JSON;
* controle de formato;
* prompt restritivo;
* limpeza de markdown;
* validação de JSON.

---

## Guardrails da IA

Foram implementados:

* tentativa de parsing JSON;
* tratamento de resposta inválida;
* persistência de erro;
* controle de status do job.

---

## Tratamento de Falhas

O sistema possui:

* logging estruturado;
* persistência de erros;
* controle de status;
* worker desacoplado.

---

## Limitações de Segurança

Por se tratar de um MVP:

* não possui autenticação;
* não possui rate limiting;
* não possui antivírus;
* depende de IA externa;
* não possui criptografia avançada.

---

# Como Executar

## Clonar o projeto

```bash id="o6gt71"
git clone <repo>
```

---

## Criar ambiente virtual

```bash id="zts00f"
python -m venv .venv
```

---

## Ativar ambiente virtual

### Windows

```bash id="q2xjlwm"
.venv\Scripts\activate
```

---

## Instalar dependências

```bash id="ckxhmr"
pip install -r requirements.txt
```

---

# Variáveis de Ambiente

Criar arquivo `.env`

```env id="0mgwgm"
GEMINI_API_KEY=SUA_CHAVE

DATABASE_URL=postgresql://fiap:fiap123@postgres:5432/secure_systems

RABBITMQ_URL=amqp://fiap:fiap123@rabbitmq:5672/
```

---

# Execução Local

## API

```bash id="ux0cl0"
python -m uvicorn app.main:app --reload
```

---

## Worker

```bash id="f4edoo"
python -m app.workers.ia_worker
```

---

# Execução com Docker

```bash id="n3qjwm"
docker compose up --build
```

---

# Swagger

```text id="86jvgg"
http://localhost:8000/docs
```

---

# RabbitMQ Management

```text id="2wnvwd"
http://localhost:15672
```

Usuário:

```text id="zq8ml0"
fiap
```

Senha:

```text id="p7qoky"
fiap123
```

---

# Estrutura do Projeto

```text id="zk78el"
secure_systems/
│
├── app/
│   ├── api/
│   ├── db/
│   ├── services/
│   └── workers/
│
├── tests/
├── reports/
├── storage/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env
```

---

# Testes

Executar:

```bash id="gqkwci"
pytest
```

---

# CI/CD

O projeto possui pipeline GitHub Actions para:

* instalação de dependências;
* execução de testes;
* validação do build.

---

# Limitações

A solução atual possui algumas limitações:

* ausência de autenticação;
* ausência de deploy cloud;
* ausência de OCR híbrido;
* dependência de IA externa;
* ausência de observabilidade avançada;
* ausência de Kubernetes.

---

# Melhorias Futuras

* Kubernetes;
* Prometheus/Grafana;
* autenticação JWT;
* OCR híbrido;
* classificação avançada de riscos;
* dashboard web;
* monitoramento distribuído;
* arquitetura baseada em microsserviços reais.

---

# Autores
Gabriel Henrique Souza do Nascimento

Projeto desenvolvido para o Hackathon Integrado FIAP - IADT + SOAT.
