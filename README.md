# API para Alocação de Desenvolvedores

Este projeto é uma API para gerenciar e realizar a alocação de desenvolvedores de software em projetos. A aplicação será utilizada por gerentes de projeto para garantir que desenvolvedores sejam alocados de forma eficiente e de acordo com suas especializações. Além disso, gerencia as informações relacionadas às tecnologias, programadores, projetos e suas respectivas alocações.

## Pré-requisitos

Antes de rodar o projeto, certifique-se de ter as seguintes ferramentas instaladas:

- **Python 3.10** ou superior
- **Docker** e **Docker Compose** instalados

## Como Clonar o Projeto

Clone o repositório para sua máquina local:

```bash
git clone https://github.com/JacksonCypriano/dev-alloc.git
```

Depois de clonar o repositório, entre na pasta do projeto:

```bash
cd dev-alloc
```

## Como Rodar o Projeto com Docker

1. **Construir os contêineres**:

   No diretório raiz do projeto, execute o comando abaixo para construir os contêineres Docker:

   ```bash
   docker-compose build
   ```

2. **Subir os contêineres**:

   Após a construção dos contêineres, execute o comando abaixo para subir os serviços (web, banco de dados, celery, etc.):

   ```bash
   docker-compose up
   ```

   Isso irá iniciar os serviços do projeto e você poderá acessar a API em `http://localhost:8000`.

3. **Variáveis de Ambiente**:

   Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente. Aqui está um exemplo de como preencher o arquivo `.env`:

   ```bash
   # Database Configuration
   POSTGRES_USER=devalloc_admin
   POSTGRES_PASSWORD=G3ehRpED#%9wbf
   POSTGRES_DB=devalloc
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   # Celery Configuration
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   CELERY_BEAT_SCHEDULE_FILENAME=/app/celerybeat-schedule
   ```

   Certifique-se de atualizar as variáveis de acordo com sua configuração desejada.

## Estrutura do Projeto

O projeto é dividido nos seguintes serviços principais:

- **web**: O serviço principal que executa o Django e serve a API.
- **db**: O banco de dados PostgreSQL onde as informações são armazenadas.
- **celery**: O serviço que gerencia as tarefas assíncronas.
- **celery_beat**: O serviço que executa tarefas periódicas agendadas no Celery.
- **redis**: O serviço que serve como broker para o Celery.

## Dockerfile

O arquivo `Dockerfile` é utilizado para construir a imagem do contêiner que irá rodar o Django e os serviços auxiliares, como o Celery. Ele realiza os seguintes passos:

1. Define a imagem base como `python:3.10-slim`.
2. Define o diretório de trabalho como `/app`.
3. Copia o arquivo `requirements.txt` para dentro do contêiner e instala as dependências.
4. Copia o código-fonte do projeto para dentro do contêiner.
5. Coleta os arquivos estáticos com o comando `python manage.py collectstatic`.
6. Expõe a porta 8000 para comunicação.
7. Configura o comando inicial para iniciar o servidor Django com `python manage.py runserver`.

## Comandos Principais

- **Subir o projeto**: `docker-compose up`
- **Construir os contêineres**: `docker-compose build`
- **Rodar os testes**: `docker-compose exec web python manage.py test`
- **Acessar o Django shell**: `docker-compose exec web python manage.py shell`

# Documentação - UserViewSet

Este documento descreve como utilizar o endpoint gerenciado pela classe `UserViewSet`, que fornece operações CRUD para o modelo de usuário no Django. Abaixo estão detalhadas as rotas disponíveis, parâmetros aceitos e comportamentos esperados.

## Endpoints Disponíveis

### 1. Listar Usuários
**Rota:** `GET /users/`

**Descrição:** Retorna a lista de usuários cadastrados, com paginação.

**Parâmetros de Query:**
- Qualquer campo do modelo `User` pode ser utilizado como filtro. Por exemplo:
  - `username=admin`
  - `email=exemplo@dominio.com`
  - `is_active=True`
- Campos com operadores podem ser utilizados:
  - `date_joined__gte=2023-01-01` (usuários cadastrados após uma data específica)

**Exemplo de Resposta:**
```json
{
  "count": 10,
  "next": "http://api.exemplo.com/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@dominio.com",
      "is_active": true
    }
  ]
}
```

---

### 2. Criar Usuário
**Rota:** `POST /users/`

**Descrição:** Cria um novo usuário. Este endpoint está aberto (não requer autenticação).

**Corpo da Requisição:**
```json
{
  "username": "novo_usuario",
  "email": "usuario@dominio.com",
  "password": "senha123"
}
```

**Exemplo de Resposta (sucesso):**
```json
{
  "message": "User created successfully.",
  "data": {
    "id": 2,
    "username": "novo_usuario",
    "email": "usuario@dominio.com",
    "is_active": true
  }
}
```

**Exemplo de Resposta (erro):**
```json
{
  "message": "Failed to create user.",
  "errors": {
    "username": ["Este campo é obrigatório."],
    "password": ["Este campo é obrigatório."]
  }
}
```

---

### 3. Atualizar Usuário
**Rota:** `PUT /users/<id>/` ou `PATCH /users/<id>/`

**Descrição:** Atualiza os dados de um usuário existente. Caso o campo `password` seja enviado, a senha será atualizada.

**Corpo da Requisição:**
```json
{
  "username": "usuario_atualizado",
  "password": "nova_senha123"
}
```

**Exemplo de Resposta (sucesso):**
```json
{
  "message": "User updated successfully.",
  "data": {
    "id": 2,
    "username": "usuario_atualizado",
    "email": "usuario@dominio.com",
    "is_active": true
  }
}
```

**Exemplo de Resposta (erro):**
```json
{
  "message": "Failed to update user.",
  "errors": {
    "email": ["Informe um endereço de e-mail válido."]
  }
}
```

---

### 4. Desativar Usuário
**Rota:** `DELETE /users/<id>/`

**Descrição:** Desativa um usuário existente (marca como inativo em vez de excluir).

**Exemplo de Resposta (sucesso):**
```json
{
  "message": "User deactivated successfully."
}
```

**Exemplo de Resposta (erro):**
```json
{
  "message": "Failed to deactivate user.",
  "error": "Descrição do erro"
}
```

---

## Regras de Permissão
- **Autenticado:** A maioria dos endpoints requer autenticação (`IsAuthenticated`).
- **Aberto:** Apenas o endpoint de criação de usuários (`POST /users/`) está disponível sem autenticação.

## Paginação
A classe `DefaultPagination` é utilizada para paginação. O número padrão de itens por página e outros parâmetros dependem da configuração desta classe no projeto.

---

## Observações
- Utilize autenticação JWT ou outro método configurado no projeto para acessar os endpoints protegidos.
- O campo `password` nunca é retornado nas respostas.
- Consulte os logs ou a documentação da API para mais detalhes sobre validações e erros específicos.

# Documentação - ProgrammerViewSet

Este documento descreve como utilizar o endpoint gerenciado pela classe `ProgrammerViewSet`, que fornece operações CRUD para o modelo de programadores no Django. Abaixo estão detalhadas as rotas disponíveis, parâmetros aceitos e comportamentos esperados.

## Endpoints Disponíveis

### 1. Listar Programadores
**Rota:** `GET /programmers/`

**Descrição:** Retorna a lista de programadores cadastrados, com paginação.

**Parâmetros de Query:**
- Qualquer campo do modelo `Programmer` pode ser utilizado como filtro. Por exemplo:
  - `name=Joao`
  - `technology__contains=Python`

**Exemplo de Resposta:**
```json
{
  "count": 5,
  "next": "http://api.exemplo.com/programmers/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Joao Silva",
      "technology": ["Python", "Django"]
    }
  ]
}
```

---

### 2. Criar Programador
**Rota:** `POST /programmers/`

**Descrição:** Cria um novo programador.

**Corpo da Requisição:**
```json
{
  "name": "Maria Oliveira",
  "technology": ["JavaScript", "React"]
}
```

**Exemplo de Resposta (sucesso):**
```json
{
  "id": 2,
  "name": "Maria Oliveira",
  "technology": ["JavaScript", "React"]
}
```

**Exemplo de Resposta (erro):**
```json
{
  "name": ["Este campo é obrigatório."],
  "technology": ["Este campo é obrigatório."]
}
```

---

### 3. Detalhar Programador
**Rota:** `GET /programmers/<id>/`

**Descrição:** Retorna os detalhes de um programador específico.

**Exemplo de Resposta:**
```json
{
  "id": 1,
  "name": "Joao Silva",
  "technology": ["Python", "Django"]
}
```

---

### 4. Atualizar Programador
**Rota:** `PUT /programmers/<id>/` ou `PATCH /programmers/<id>/`

**Descrição:** Atualiza os dados de um programador existente.

**Corpo da Requisição:**
```json
{
  "name": "Joao Atualizado",
  "technology": ["Flask"]
}
```

**Exemplo de Resposta (sucesso):**
```json
{
  "id": 1,
  "name": "Joao Atualizado",
  "technology": ["Flask"]
}
```

**Exemplo de Resposta (erro):**
```json
{
  "technology": ["A tecnologia 'InvalidTech' não existe."]
}
```

---

### 5. Excluir Programador
**Rota:** `DELETE /programmers/<id>/`

**Descrição:** Remove um programador do sistema.

**Exemplo de Resposta (sucesso):**
```json
{
  "message": "Programmer deleted successfully."
}
```

---

## Regras de Permissão
- **Autenticado:** Todos os endpoints requerem autenticação (`IsAuthenticated`).

## Paginação
A classe `DefaultPagination` é utilizada para paginação. O número padrão de itens por página e outros parâmetros dependem da configuração desta classe no projeto.

---

## Observações
- Utilize autenticação JWT ou outro método configurado no projeto para acessar os endpoints.
- Valide as tecnologias antes de enviá-las no campo `technology`, garantindo que elas existem no banco de dados.
- Consulte os logs ou a documentação da API para mais detalhes sobre validações e erros específicos.

# Documentação - ProjectViewSet

Este documento descreve como utilizar o endpoint gerenciado pela classe `ProjectViewSet`, que fornece operações CRUD para o modelo de projetos no Django. Abaixo estão detalhadas as rotas disponíveis, parâmetros aceitos e comportamentos esperados.

---

## Endpoints Disponíveis

### 1. Listar Projetos
**Rota:** `GET /projects/`  
**Descrição:** Retorna a lista de projetos cadastrados, com suporte a filtros e paginação.

**Parâmetros de Query:**
- Qualquer campo do modelo `Project` pode ser utilizado como filtro. Exemplos:
  - `name=Projeto1`
  - `status=PLANNED`
  - `start_date__gte=2025-01-01`

**Exemplo de Resposta:**
```json
{
  "count": 3,
  "next": "http://api.exemplo.com/projects/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Projeto 1",
      "start_date": "2025-01-01",
      "end_date": "2025-01-31",
      "status": "PLANNED",
      "required_technologies": ["Python", "Django"]
    }
  ]
}
```

---

### 2. Criar Projeto
**Rota:** `POST /projects/`  
**Descrição:** Cria um novo projeto.

**Corpo da Requisição:**
```json
{
  "name": "Projeto Novo",
  "start_date": "2025-01-01",
  "end_date": "2025-01-31",
  "required_technologies": ["Python", "Django"],
  "status": "PLANNED"
}
```

**Exemplo de Resposta (sucesso):**
```json
{
  "message": "Project created successfully.",
  "data": {
    "id": 4,
    "name": "Projeto Novo",
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "status": "PLANNED",
    "required_technologies": ["Python", "Django"]
  }
}
```

**Exemplo de Resposta (erro):**
```json
{
  "message": "Failed to create project.",
  "errors": {
    "name": ["Este campo é obrigatório."],
    "start_date": ["Este campo é obrigatório."]
  }
}
```

---

### 3. Atualizar Projeto
**Rota:** `PUT /projects/<id>/` ou `PATCH /projects/<id>/`  
**Descrição:** Atualiza os dados de um projeto existente.

**Corpo da Requisição:**
```json
{
  "name": "Projeto Atualizado",
  "end_date": "2025-02-01",
  "status": "IN_PROGRESS"
}
```

**Exemplo de Resposta (sucesso):**
```json
{
  "message": "Project updated successfully.",
  "data": {
    "id": 1,
    "name": "Projeto Atualizado",
    "start_date": "2025-01-01",
    "end_date": "2025-02-01",
    "status": "IN_PROGRESS",
    "required_technologies": ["Python", "Django"]
  }
}
```

**Exemplo de Resposta (erro):**
```json
{
  "message": "Failed to update project.",
  "errors": {
    "end_date": ["Data inválida."]
  }
}
```

---

### 4. Deletar Projeto
**Rota:** `DELETE /projects/<id>/`  
**Descrição:** Remove um projeto existente.

**Exemplo de Resposta (sucesso):**
```json
{
  "message": "Project deleted successfully."
}
```

**Exemplo de Resposta (erro):**
```json
{
  "message": "Failed to delete project.",
  "error": "Descrição do erro"
}
```

---

## Regras de Permissão
- **Autenticado:** Todos os endpoints requerem autenticação (`IsAuthenticated`).

---

## Paginação
A classe `DefaultPagination` é utilizada para paginação. O número padrão de itens por página e outros parâmetros dependem da configuração desta classe no projeto.

---

## Observações
- Utilize autenticação JWT ou outro método configurado no projeto para acessar os endpoints.
- O campo `required_technologies` aceita uma lista de tecnologias necessárias para o projeto.
- Consulte os logs ou a documentação da API para mais detalhes sobre validações e erros específicos.


# Documentação da API - Technology ViewSet

Esta documentação fornece uma visão geral de como interagir com o modelo **Technology** através do `TechnologyViewSet` no Django REST framework.

## Visão Geral

O `TechnologyViewSet` é um conjunto de endpoints da API projetado para realizar operações CRUD (Criar, Ler, Atualizar, Deletar) no modelo `Technology`, que consiste em um campo `name`. Esta API utiliza **autenticação**, **paginação** e suporta **filtragem**.

## Autenticação

Todos os endpoints desta API exigem que o usuário esteja autenticado. Se o usuário não estiver autenticado, ele receberá uma resposta `401 Unauthorized`.

## Endpoints

### 1. **Listar Tecnologias** (`GET /technologies/`)

- **Descrição**: Recupera uma lista de todas as tecnologias.
- **Paginação**: Este endpoint suporta paginação. Se o número de tecnologias for grande, a resposta será dividida em páginas.
- **Filtros**: Você pode aplicar parâmetros de consulta para filtrar os resultados com base no campo `name`. Os filtros incluem:
    - Correspondência exata (`name=<valor>`)
    - Filtro personalizado usando dois pontos (`name__icontains=<valor>`) para correspondência parcial.

**Exemplo de Requisição**:
```
GET /technologies/?name=Python
```

**Resposta**:
```json
[
    {
        "id": 1,
        "name": "Python"
    },
    {
        "id": 2,
        "name": "Django"
    }
]
```

### 2. **Criar Tecnologia** (`POST /technologies/`)

- **Descrição**: Cria um novo registro de tecnologia.
- **Campos Obrigatórios**: O campo `name` é obrigatório e deve ser único.
- **Exemplo de Requisição**:
```json
{
    "name": "React"
}
```

**Resposta**:
```json
{
    "id": 3,
    "name": "React"
}
```
**Status**: `201 Created`

### 3. **Visualizar Tecnologia Específica** (`GET /technologies/{id}/`)

- **Descrição**: Recupera os detalhes de uma tecnologia específica com base no `id`.
- **Exemplo de Requisição**:
```
GET /technologies/1/
```

**Resposta**:
```json
{
    "id": 1,
    "name": "Python"
}
```

### 4. **Atualizar Tecnologia** (`PUT /technologies/{id}/`)

- **Descrição**: Atualiza os dados de uma tecnologia específica. Todos os campos devem ser fornecidos.
- **Exemplo de Requisição**:
```json
{
    "name": "Django REST Framework"
}
```

**Resposta**:
```json
{
    "id": 1,
    "name": "Django REST Framework"
}
```

### 5. **Atualizar Tecnologia Parcialmente** (`PATCH /technologies/{id}/`)

- **Descrição**: Atualiza parcialmente os dados de uma tecnologia. Apenas os campos fornecidos serão atualizados.
- **Exemplo de Requisição**:
```json
{
    "name": "Flask"
}
```

**Resposta**:
```json
{
    "id": 1,
    "name": "Flask"
}
```

### 6. **Deletar Tecnologia** (`DELETE /technologies/{id}/`)

- **Descrição**: Deleta uma tecnologia específica com base no `id`.
- **Exemplo de Requisição**:
```
DELETE /technologies/1/
```

**Resposta**:
- **Status**: `204 No Content`

## Modelo Technology

A classe `Technology` tem o seguinte campo:

- **name**: Campo de texto (CharField) com um limite de 18 caracteres. Este campo é único, ou seja, não pode haver tecnologias com o mesmo nome.

### Exemplo de Resposta de Tecnologia:

```json
{
    "id": 1,
    "name": "Python"
}
```


# Documentação dos Testes de Alocação de Projetos

## Objetivo
Este conjunto de testes visa validar a alocação de programadores em projetos, levando em consideração as tecnologias requeridas, o período do projeto, e o limite de horas. Os testes verificam as regras de negócio implementadas nos modelos de **ProjectAllocation** e **Programmer**. 

## Testes

### 1. `test_developer_technology_validation`
Este teste valida se o desenvolvedor possui a tecnologia necessária para o projeto. Se o desenvolvedor tiver a tecnologia correta, a alocação do projeto será permitida. Caso contrário, uma exceção `ValidationError` será gerada.

### 2. `test_developer_technology_validation_serializer`
Aqui, testamos a validação usando o serializador para garantir que a alocação será aceita se o desenvolvedor tiver as tecnologias necessárias para o projeto. O serializador valida corretamente os dados fornecidos antes de permitir a alocação.

### 3. `test_developer_technology_validation_invalid`
Este teste verifica o caso em que um desenvolvedor não possui a tecnologia necessária para o projeto. Quando isso acontece, uma exceção `ValidationError` é levantada, informando que o desenvolvedor não possui a tecnologia necessária para o projeto.

### 4. `test_developer_technology_validation_invalid_serializer`
Testa o comportamento do serializador quando o desenvolvedor não tem as tecnologias exigidas para o projeto. Nesse caso, o serializador irá falhar na validação e não permitirá a criação da alocação.

### 5. `test_allocation_outside_project_period`
Valida que não é possível alocar um desenvolvedor fora do período de execução do projeto. Se a alocação estiver fora do intervalo de datas do projeto, uma exceção `ValidationError` será gerada.

### 6. `test_allocation_outside_project_period_serializer`
Verifica a validação do serializador quando se tenta alocar um desenvolvedor fora do período do projeto. O serializador também levanta um erro de validação se a alocação ocorrer fora das datas definidas para o projeto.

### 7. `setUp_hours_limit`
Este teste configura uma alocação de projeto com um limite de horas para um desenvolvedor, que deve ser respeitado durante a alocação. O objetivo é garantir que o número de horas alocadas seja controlado corretamente.

### 8. `test_hours_limit_exceeded`
Verifica se o sistema corretamente rejeita uma alocação de horas que exceda o limite estabelecido para o projeto. Se o número de horas alocadas for superior ao limite, uma exceção `ValidationError` será gerada.

### 9. `test_hours_limit_exceeded_serializer`
Este teste valida o comportamento do serializador quando o limite de horas do projeto é ultrapassado. O serializador irá levantar uma exceção de `ValidationError`, garantindo que o total de horas alocadas não ultrapasse o limite de horas definido para o projeto.

## Resumo
Esses testes cobrem as principais validações envolvidas na alocação de programadores em projetos, incluindo verificação de tecnologias requeridas, período de alocação, e limites de horas. Eles garantem que as regras de negócio sejam respeitadas, evitando alocações inválidas ou inconsistentes.



# Documentação da Tarefa Agendada: `mark_project_as_late`

## Objetivo
A tarefa `mark_project_as_late` é uma tarefa assíncrona configurada para ser executada automaticamente utilizando o **Celery**. O objetivo dessa tarefa é marcar projetos como "atrasados" (status `LATE`) quando a data atual for posterior à data de término do projeto e o status atual do projeto não for `LATE` ou `DONE`. Essa tarefa é programada para ser executada automaticamente de acordo com uma agenda definida no Celery Beat.

## Funcionamento

### 1. **Verificação de Projetos Atrasados**
A tarefa percorre todos os projetos no banco de dados que não estão com o status `LATE` ou `DONE` (excluindo esses status) e verifica se a data atual (`now.date()`) é maior que a data de término do projeto (`project.end_date`). Se o projeto estiver atrasado, o status do projeto é alterado para `LATE`, e a mudança é salva no banco de dados.

### 2. **Configuração do Celery Beat**
A tarefa `mark_project_as_late` é configurada no **Celery Beat** para ser executada de forma automática de acordo com a seguinte programação:

```python
CELERY_BEAT_SCHEDULE = {
    "mark_project_as_late": {
        "task": "apps.projects.tasks.mark_project_as_late",
        "schedule": crontab(hour=0, minute=0, day_of_week='*'),
    }
}
```

Com isso, a tarefa será executada todos os dias à meia-noite (`00:00`), sem restrição de dia da semana. Isso garante que a verificação dos projetos atrasados seja feita diariamente, sem a necessidade de intervenção manual.

### 3. **Log de Execução**
Um logger é configurado para essa tarefa, mas ele não está sendo usado explicitamente no código. Para futuros aprimoramentos, poderia ser interessante adicionar logs informando quando um projeto foi atualizado para o status `LATE`, garantindo melhor rastreabilidade da execução da tarefa.

## Resumo
A tarefa `mark_project_as_late` é uma tarefa agendada do Celery que verifica periodicamente os projetos e os marca como "atrasados" caso o projeto tenha ultrapassado a data de término. A tarefa é executada automaticamente todos os dias à meia-noite, de acordo com a configuração no Celery Beat.
