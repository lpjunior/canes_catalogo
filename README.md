# CANES — Catálogo e pedidos

Projeto didático de Django para estudo de views, rotas, cálculos em Python e templates. Apresenta um catálogo de produtos e um painel de pedidos com dados fictícios definidos em memória.

## Funcionalidades

- Página inicial com apresentação do projeto.
- Catálogo com preços, estoque, situação dos produtos e indicadores.
- Painel de pedidos com clientes, quantidades, situações e totais calculados com `Decimal`.
- Mensagens alternativas para listas vazias.
- Saudação personalizada pelo nome informado na URL.
- Herança de templates com `base.html`, componentes reutilizáveis de navbar, rodapé e aviso, e estilos em `core/static/core/css/style.css`.

Os produtos e pedidos são definidos no código. Não há formulário de cadastro nem persistência desses dados no banco. O SQLite é utilizado pela infraestrutura padrão do Django.

## Instalação e execução

É necessário ter Python instalado, com suporte à versão do Django declarada em `requirements.txt` (`Django==6.1.2`), e acesso ao `pip`. Execute os comandos na pasta que contém `manage.py`.

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

### Linux e macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Acesse [a página inicial](http://127.0.0.1:8000/). Para encerrar o servidor, pressione `Ctrl+C`.

Se um ambiente virtual existente apontar para um Python removido ou inacessível, recrie-o com uma instalação válida do Python antes de instalar as dependências.

## Rotas

| Endereço | Página |
| --- | --- |
| `/` | Início |
| `/catalogo/` | Catálogo de produtos |
| `/pedidos/` | Painel de pedidos |
| `/ola/Maria/` | Exemplo de saudação personalizada |
| `/admin/` | Administração padrão do Django |

Para acessar a administração, crie um usuário após executar as migrações:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## Estrutura

```text
canes_catalogo/
├── config/                     # Configurações e URLs principais
├── core/
│   ├── migrations/             # Migrações do aplicativo
│   ├── static/core/css/
│   │   └── style.css           # Estilos compartilhados
│   ├── templates/core/
│   │   ├── base.html           # Estrutura HTML compartilhada
│   │   ├── index.html
│   │   ├── catalogo.html
│   │   ├── pedidos.html
│   │   ├── saudacao.html
│   │   └── partials/           # Navbar, rodapé e aviso
│   ├── services.py             # Cálculos e resumo do catálogo
│   ├── views.py                # Dados e contexto das páginas
│   ├── urls.py                 # Rotas do aplicativo
│   └── tests.py                # Testes existentes
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

Para alterar os dados de demonstração, edite as listas em `core/views.py`. Os cálculos do catálogo estão em `core/services.py`; os indicadores de pedidos são calculados em `calcular_indicadores_pedidos`, em `core/views.py`.

## Verificações

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

No Linux e macOS, substitua `.\.venv\Scripts\python.exe` por `.venv/bin/python`.

Os testes existentes cobrem a página de pedidos, seus indicadores e valores, cálculos com outros dados, lista vazia e links de navegação. Os comandos acima permitem verificar o estado atual do projeto; esta documentação não representa uma execução bem-sucedida dos testes.

## Configuração local

`config/settings.py` lê a variável de ambiente `DJANGO_SECRET_KEY`. Quando ela não está definida, gera uma chave temporária. Para definir uma chave estável na sessão do PowerShell antes de iniciar o servidor:

```powershell
$env:DJANGO_SECRET_KEY = 'substitua-por-uma-chave-secreta-propria'
```

Arquivos `.env` não são carregados automaticamente pela configuração atual. As configurações presentes usam `DEBUG = True` e destinam-se ao desenvolvimento. Uma implantação exige configurar a chave, os hosts permitidos, os arquivos estáticos e desativar o modo de depuração.

O `.gitignore` exclui ambientes virtuais, caches, banco SQLite local, logs, variáveis de ambiente e diretórios de arquivos gerados. As migrações e os arquivos de código, templates e CSS devem ser versionados. Arquivos que já estejam rastreados pelo Git não deixam de ser rastreados apenas por serem adicionados ao `.gitignore`.

## Autoria

Projeto educacional desenvolvido com auxílio de IA. Se utilizado em uma atividade com regras específicas sobre autoria ou uso de IA, informe esse auxílio ao professor.
