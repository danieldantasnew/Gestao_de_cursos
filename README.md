# 🎓 Gestão de Cursos

Aplicação web desenvolvida com **Django** para gerenciamento de cursos, disciplinas e perfis acadêmicos. O projeto está containerizado com **Docker** e utiliza **Tailwind CSS** no frontend para estilização moderna e responsiva.

---

## Como rodar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/danieldantasnew/Gestao_de_cursos.git
cd Gestao_de_cursos
```

### 2. Construa e suba os containers
```bash
docker compose up --build -d
```

### 3. Execute as migrações e crie o superusuário (API)
```bash
docker compose exec api python manage.py migrate
docker compose exec api python manage.py createsuperuser
```

### 4. Acessos
```bash
API: http://localhost:8000/

Documentação Swagger: http://localhost:8000/api/swagger/

Frontend (Django + Tailwind): http://localhost:8001/

```

## Estrutura do Projeto
```bash
api/: Backend Django REST (serviço API)

frontend/: Frontend Django com Tailwind CSS (serviço frontend)

catalogo/: App principal com modelos, views, templates e arquivos estáticos

setup/: Configurações globais do projeto Django

docker-compose.yml: Orquestração dos serviços

Dockerfile: Build do ambiente Python + Node para Tailwind

.env: Variáveis de ambiente

package.json: Dependências JS (Tailwind CLI)

Tecnologias
Python 3.11

Django 5.2

PostgreSQL

Tailwind CSS

Docker & Docker Compose

```