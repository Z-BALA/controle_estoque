# Controle de Estoque — P2

Evolução do projeto Django da P1 para um mini-SaaS. Mantém o banco SQLite, os registros originais, as rotas e o visual das telas anteriores. Acrescenta organizações, perfis, autenticação, API REST, dashboard e CSV.

## Executar no Windows (Python 3.10 ou superior, recomendado 3.12/3.13)

Extraia o ZIP, abra a pasta que contém manage.py no VS Code e execute no PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py configurar_perfil admin --papel admin
.\venv\Scripts\python.exe manage.py runserver
```

Na criação do superusuário, escolha o nome `admin` ou ajuste o comando `configurar_perfil` para o nome escolhido. Abra http://127.0.0.1:8000/ e use as credenciais cadastradas.

Se já tem um banco SQLite da P1 ou P2, faça uma cópia antes de executar `migrate`. Mantenha o banco como `db.sqlite3` na pasta do projeto e use a conta existente. As migrações associam os registros da P1 à organização padrão e preservam os perfis que já existem na P2. O banco local fica fora do Git.

## Organizações e perfis

Em `/admin/`, o superusuário do sistema pode criar organizações, usuários e perfis. Para usuários de empresas, não marque superusuário nem equipe. Crie um Perfil para cada usuário e associe sua organização e papel. O superusuário pode consultar dados de todas as organizações no Admin, mas as telas de negócio exigem um perfil e respeitam a organização desse perfil. Usuários sem perfil recebem 403. A área administrativa é de consulta para registros de estoque; use as telas de negócio para alterações.

Administrador da empresa: consultas, CRUD de produtos/fornecedores/depósitos, registro de entradas e saídas, dashboard completo e CSV. Operador: consultas, movimentações, KPIs, ranking e distribuição; sem cadastro/edição/exclusão de produtos, fornecedores e depósitos, série mensal ou exportação. Movimentações são somente leitura/criação para preservar o histórico, como na P1. As exclusões de cadastros mantêm o comportamento em cascata da P1.

## API

Acesse `/api/` após login. Sessão Django e autenticação básica para testes locais. Em produção use HTTPS e configuração adequada. Recursos: `/api/produtos/`, `/api/fornecedores/`, `/api/depositos/`, `/api/movimentacoes/`, `/api/estoque/`, `/api/dashboard/`. Os três cadastros suportam GET, POST, PUT, PATCH, DELETE; movimentações suportam GET e POST. Estoque e dashboard são de leitura. Todos os endpoints de negócio exigem perfil e respeitam a organização.

Exemplo de POST para movimentações: `{"produto": 1, "deposito": 1, "tipo": "entrada", "quantidade": 5}` (use IDs da própria empresa). A saída superior ao saldo e quantidades não positivas são rejeitadas. O usuário não escolhe a organização no payload.

## Dashboard

Quatro perguntas de negócio: quantas movimentações e unidades entraram/saíram? Quais produtos têm mais saídas? Como entradas e saídas evoluem por mês? Qual a distribuição por tipo de movimentação? Indicadores calculados no ORM; filtro por datas `inicio` e `fim`, no formato AAAA-MM-DD. CSV em `/dashboard/exportar/`, somente administrador. Gráficos Chart.js carregados via CDN; sem internet, as tabelas e indicadores continuam disponíveis. A tela original de estoque mantém o alerta de estoque mínimo.

## Testes

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py test
```

Roteiro manual: crie duas organizações e um administrador em cada; cadastre produtos e depósitos em ambas; confirme que listas, selects, API e dashboard não misturam registros; tente editar um ID da outra organização (404); teste saída maior que o saldo; entre como operador e confirme bloqueio de cadastro, exportação e série mensal. Teste filtro válido, inválido e período vazio.

## Observações de entrega

- A migração 0001 original foi preservada. As migrações 0002–0004 adicionam FK opcional, migram dados e tornam FK obrigatória. A migração 0005 une essa sequência às migrações de categorias da P1.
- Não havia campos globalmente únicos nos models de negócio da P1; não se impôs unicidade de nomes para evitar alterar a regra original.
- Dependências ajustadas para Django 5.2 LTS e DRF 3.16; configurações locais de desenvolvimento. Em produção configure DJANGO_SECRET_KEY, DJANGO_DEBUG=0 e DJANGO_ALLOWED_HOSTS.
- Escopo baseado nas aulas 13, 14 e 17; enunciado específico do T2 e demais aulas não foram fornecidos.
