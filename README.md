# Projeto de Gestão de Estoques - API

Esta é a API desenvolvida para a Atividade Prática II da disciplina de Desenvolvimento de Sistemas WEB I. O projeto implementa um sistema robusto para gestão de estoques utilizando FastAPI, com funcionalidades de movimentação, controle de saldo, alertas e relatórios.

## Tecnologias Utilizadas
* Python 3
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite

## Como Executar a Aplicação 

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento local.

1.  **Pré-requisitos**
    Certifique-se de ter o Python 3.10+ e o `pip` instalados em sua máquina.

2.  **Clonar o Repositório**
    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-da-pasta-do-projeto>
    ```

4.  **Instalar as Dependências**
    Com o ambiente ativado, instale todas as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Executar a Aplicação**
    Utilize o servidor Uvicorn para iniciar a API:
    ```bash
    uvicorn main:app --reload
    ```
    A API estará disponível em `http://127.0.0.1:8000`.

6.  **Acessar a Documentação Interativa**
    A documentação automática do Swagger UI pode ser acessada no navegador através da URL:
    `http://127.0.0.1:8000/docs`

## Decisão Sobre Saldo Negativo

O sistema foi configurado para **bloquear** qualquer tentativa de registrar uma saída de estoque que resulte em um saldo negativo. Caso uma operação de `SAIDA` (seja por venda, ajuste ou movimentação direta) seja maior que o saldo atual do produto, a API retornará um erro `HTTP 400 Bad Request` com uma mensagem indicando saldo insuficiente, e a operação não será concluída. 

## Exemplos de Chamadas da API

A seguir estão exemplos de como utilizar os principais endpoints de gestão de estoque.

*(**Nota:** Antes de testar, certifique-se de ter criado ao menos uma categoria e um produto).*

### 1. Registrar uma Venda

Registra uma saída de estoque com o motivo "venda".

* **Endpoint:** `POST /api/v1/estoque/venda`
* **Corpo da Requisição (Body):**
    ```json
    {
      "produto_id": 1,
      "quantidade": 2
    }
    ```
* **Resposta de Sucesso (201 Created):**
    ```json
    {
      "id": 1,
      "produto_id": 1,
      "tipo": "SAIDA",
      "quantidade": 2,
      "motivo": "venda",
      "criado_em": "2025-10-05T14:30:00.123456"
    }
    ```

### 2. Registrar uma Devolução

Registra uma entrada de estoque com o motivo "devolucao".

* **Endpoint:** `POST /api/v1/estoque/devolucao`
* **Corpo da Requisição (Body):**
    ```json
    {
      "produto_id": 1,
      "quantidade": 1
    }
    ```
* **Resposta de Sucesso (201 Created):**
    ```json
    {
      "id": 2,
      "produto_id": 1,
      "tipo": "ENTRADA",
      "quantidade": 1,
      "motivo": "devolucao",
      "criado_em": "2025-10-05T14:35:00.123456"
    }
    ```

### 3. Consultar o Extrato de um Produto

Retorna as últimas movimentações de um produto específico, com paginação.

* **Endpoint:** `GET /api/v1/estoque/extrato/1?limit=5`
* **Corpo da Requisição (Body):** Nenhum
* **Resposta de Sucesso (200 OK):**
    ```json
    [
      {
        "id": 2,
        "produto_id": 1,
        "tipo": "ENTRADA",
        "quantidade": 1,
        "motivo": "devolucao",
        "criado_em": "2025-10-05T14:35:00.123456"
      },
      {
        "id": 1,
        "produto_id": 1,
        "tipo": "SAIDA",
        "quantidade": 2,
        "motivo": "venda",
        "criado_em": "2025-10-05T14:30:00.123456"
      }
    ]
    ```

### 4. Obter o Resumo de Estoques

Retorna uma lista com o resumo de todos os produtos, incluindo saldo e status de estoque mínimo.

* **Endpoint:** `GET /api/v1/estoque/resumo`
* **Corpo da Requisição (Body):** Nenhum
* **Resposta de Sucesso (200 OK):**
    ```json
    [
      {
        "produto_id": 1,
        "nome": "Produto A",
        "saldo": 8,
        "estoque_minimo": 10,
        "abaixo_minimo": true
      },
      {
        "produto_id": 2,
        "nome": "Produto B",
        "saldo": 50,
        "estoque_minimo": 20,
        "abaixo_minimo": false
      }
    ]
    ```