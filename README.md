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
| `/series/found` | Retorna as séries salvas. | `curl <baseUrl>/api/series/found` |
| `/series/search/{title}` | Pesquisa séries por título específico. | `curl <baseUrl>/series/search/Breaking Bad` |
| `/series/search/{genre}` | Pesquisa séries por genero. | `curl <baseUrl>/series/search/comédia` |

### Canais

| Endpoint | Descrição | Exemplo de Uso (bash) |
|----------|-----------|-----------------------|
| `/channels/found` | Retorna os canais salvos. | `curl <baseUrl>/channels` |
| `/channels/search/{ciid}` | Pesquisa canal por ID. | `curl <baseUrl>/channels/{28shudhwue982jijwz}` |
| `/channels/search/{genre}` | Pesquisa canais por categoria específica. | `curl <baseUrl>/channels/search/abertos` |


## Funcionalidades Planejadas

- Relacionamento entre entidades (por exemplo, recomendações de filmes/séries semelhantes)
- Interface Web para facilitar a adição de novos dados

## Pré-requisitos

- Python: ^3.8
- Pip

## Instalação

Instale as dependências utilizando pip:

```bash
pip install -r requirements.txt
```

Caso queira alterar a porta padrão, renomeie o arquivo .env.example para .env e modifique o campo `API_PORT` para a porta desejada.

Dependendo do ambiente (produção ou desenvolvimento), o processo de inicialização varia.

## Produção

Para rodar a API em produção, use o seguinte comando para iniciar o servidor:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Desenvolvimento

Para iniciar o ambiente de desenvolvimento, utilize o comando:

```bash
python -m uvicorn app.main:app --reload
```

Este comando iniciará o servidor com recarregamento automático sempre que alterações forem feitas no código.

## Contribuindo

Contribuições são bem-vindas! Se você deseja adicionar novos filmes, séries, ou fazer melhorias, basta criar um Pull Request e daremos uma olhada o quanto antes.

## Licença
Licenciado sob a Open Software License v3.0.