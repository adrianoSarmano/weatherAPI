# Weather API
Uma API simples para consultar e registrar dados climáticos usando a API OpenWeather.

## Descrição
Este projeto consiste em uma API RESTful desenvolvida em Flask que:
- Consulta dados climáticos atuais de uma cidade na API OpenWeather
- Armazena os dados em um banco de dados PostgreSQL
- Fornece endpoints para consultar os dados atuais e históricos

## Estrutura do Projeto
```
  weather-api/
  ├── app.py             # Aplicação principal Flask
  ├── Dockerfile         # Configuração para build da imagem Docker
  ├── docker-compose.yml # Configuração dos serviços Docker
  ├── .env               # Variáveis de ambiente (chave da API, etc.)
  └── README.md          # Documentação do projeto
```

## Requisitos
- Docker e Docker Compose
- Chave de API do OpenWeather

## Configuração e Execução
1. Clone o repositório
2. Configure a chave da API OpenWeather no arquivo .env
3. Execute os containers usando Docker Compose:

```bash
docker-compose up
```
A API estará disponível em http://localhost:5000

## Endpoints Disponíveis

### GET /api/now
Retorna dados climáticos atuais para uma cidade.

**Parâmetros de consulta:**
- 'city' (opcional): Nome da cidade (padrão: Florianópolis)

**Exemplo de resposta:**
```json
{
  "city": "Florianopolis",
  "temperature": 25.3,
  "humidity": 70,
  "pressure": 1012,
  "wind_speed": 3.5,
  "description": "céu limpo",
  "timestamp": "2025-04-01T14:30:45.123456"
}
```

### GET /api/history
Retorna o histórico de dados climáticos para uma cidade.

**Parâmetros de consulta:**
- 'city' (opcional): Nome da cidade (padrão: Florianópolis)
- 'limit' (opcional): Número máximo de registros (padrão: 10)

**Exemplo de resposta:**
```json
[
  {
    "city": "Florianopolis",
    "temperature": 25.3,
    "humidity": 70,
    "pressure": 1012,
    "wind_speed": 3.5,
    "description": "céu limpo",
    "timestamp": "2025-04-01T14:30:45.123456"
  },
  {
    "city": "Florianopolis",
    "temperature": 24.8,
    "humidity": 72,
    "pressure": 1011,
    "wind_speed": 3.2,
    "description": "nuvens dispersas",
    "timestamp": "2025-04-01T13:15:30.654321"
  }
]
```

## Arquitetura
O projeto utiliza uma arquitetura baseada em containers Docker:

- **Container API**: Uma aplicação Flask que serve os endpoints da API
- **Container PostgreSQL**: Banco de dados para armazenamento dos dados climáticos

A comunicação entre os containers é gerenciada pelo Docker Compose, que também configura healthchecks para garantir que a API só inicie após o banco de dados estar pronto.

## Variáveis de Ambiente para o arquivo .env
- OPENWEATHER_API_KEY: Chave de API para o OpenWeather
- DB_NAME: Nome do banco de dados PostgreSQL
- DB_USER: Usuário do banco de dados
- DB_PASSWORD: Senha do banco de dados

## Informações Técnicas
- **Linguagem**: Python 3.9
- **Framework Web**: Flask
- **Banco de Dados**: PostgreSQL 13
- **Containerização**: Docker & Docker Compose