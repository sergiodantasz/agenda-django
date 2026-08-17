# Agenda (Django)

Agenda de contatos construída com Django 6, Python 3.14, HTML e CSS, com um
design system próprio e suporte a tema escuro.

## Funcionalidades

- Cadastro, login e edição de perfil de usuários, com foto de perfil;
- CRUD completo de contatos privados (somente o dono visualiza, edita e exclui);
- Busca por nome, sobrenome, telefone ou e-mail;
- Paginação (20 contatos por página);
- Categorias e upload de foto para os contatos;
- Formulários com validação nativa do navegador e interface moderna;
- Admin do Django configurado em português;
- Páginas de erro 404 e 500 customizadas.

## Requisitos

- Python 3.14+;
- [uv](https://docs.astral.sh/uv/).

## Instalação

```bash
uv sync
cp .env.example .env
```

Edite o `.env` e defina uma `SECRET_KEY` aleatória. As demais variáveis já
possuem valores adequados para desenvolvimento.

## Executando

```bash
poe migrate
poe runserver
```

Acesse <http://127.0.0.1:8000>.

Para acessar o admin, crie um superusuário com
`python manage.py createsuperuser`.

## Ferramentas

- `ruff` para lint e formatação de código;
- `djade` e `djangofmt` para formatação de templates;
- `poethepoet` como executor de tarefas (`poe runserver`, `poe migrate`, `poe format`).

```bash
ruff check .
poe format
```