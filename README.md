# WebFilms API

Uma API para salvar filmes e séries do seu gosto!

Uma versão atualizada está sempre postada em [https://web-films-api.vercel.app/](https://web-films-api.vercel.app/)

## Usabilidade

Esta API oferece vários endpoints para recuperar dados de filmes e séries.
Ela **NÃO** interage diretamente com plataformas de streaming, apenas oferece dados estáticos para exibição.

## Endpoints

:information_source: **Aviso:** Substitua `<baseUrl>` pelo URL base da API para acessar os endpoints.

### Filmes

| Endpoint | Descrição | Exemplo de Uso (bash) |
|----------|-----------|-----------------------|
| `/movies/found` | Retorna os filmes salvos. | `curl <baseUrl>/movies/found` |
| `/movies/search/{title}` | Pesquisa filmes por título específico. | `curl <baseUrl>/movies/search/Inception` |
| `/movies/search/{genre}` | Pesquisa filmes por genero. | `curl <baseUrl>/movies/search/genero/comédia` |

### Séries

| Endpoint | Descrição | Exemplo de Uso (bash) |
|----------|-----------|-----------------------|
| `/series/found` | Retorna as séries salvas. | `curl <baseUrl>/series/found` |
| `/series/search/{title}` | Pesquisa séries por título específico. | `curl <baseUrl>/series/search/Breaking Bad` |
| `/series/search/{genre}` | Pesquisa séries por genero. | `curl <baseUrl>/series/search/comédia` |

### Canais

| Endpoint | Descrição | Exemplo de Uso (bash) |
|----------|-----------|-----------------------|
| `/channels/found` | Retorna os canais salvos. | `curl <baseUrl>/channels` |
| `/channels/search/{channel_id}` | Pesquisa canal por ID. | `curl <baseUrl>/channels/{28shudhwue982jijwz}` |
| `/channels/search/{genre}` | Pesquisa canais por categoria específica. | `curl <baseUrl>/channels/search/abertos` |


## Swagger

- O projeto contém um Swagger que fica em **`<baseUrl>`/docs** para melhor ultilização dos endpoints e para ajudar os novos usuários da API.

## Funcionalidades Planejadas

- Relacionamento entre entidades (por exemplo, recomendações de filmes/séries semelhantes)
- Interface Web para facilitar a adição de novos dados

## Funcionalidades Planejadas

- Relacionamento entre entidades (por exemplo, recomendações de filmes/séries semelhantes)
- Interface Web para facilitar a adição de novos dados

## Pré-requisitos

- Python: ^3.8
- Poetry

## Instalação

Instale as dependências utilizando Poetry:

```bash
poetry install
```

Dependendo do ambiente (produção ou desenvolvimento), o processo de inicialização varia.

## Produção e Desenvolvimento

Nesse projeto foi usado um lynt para otimizar os comandos de run.
Para rodar a API em produção, use o seguinte comando para iniciar o servidor:

```bash
task run
```

Este comando iniciará o servidor com recarregamento automático sempre que alterações forem feitas no código.

O Projeto inclui mais alguns comandos para melhorar a experiência de desenvolvimento para futuras contribuições que são:

<h4> Pré Formatação </h4>

```bash
task pre_format
```

<h4> Formatação </h4>

```bash
task format
```

<h4> Execução de testes </h4>

```bash
task test
```

<h4> Pré Formatação </h4>

```bash
task post_test
```

Obs: o comando acima é para arquivo de coverage.

## Contribuindo

Contribuições são bem-vindas! Se você deseja adicionar novos filmes, séries, ou fazer melhorias, basta criar um Pull Request e daremos uma olhada o quanto antes.

## Licença
Licenciado sob a Open Software License v3.0.