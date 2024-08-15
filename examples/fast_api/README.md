# Diia SDK FastAPI Example

## Usage

We use [poetry](https://github.com/sdispater/poetry) to manage dependencies

```shell
poetry install --no-root

export DIIA_HOST='https://api2.diia.gov.ua'
export DIIA_ACQUIRER_TOKEN='_token_'
export DIIA_KEY=''
export DIIA_PASSWORD=''
export DIIA_CERTIFICATE=''
export DIIA_SUBJECT_KEY_ID=''
export DIIA_DIIA_CERTIFICATE=''
export DIIA_DIIA_CERTIFICATE_KEP=''
export DIIA_DIIA_ISSUER_CERTIFICATE=''  # Optional
export DIIA_BASIC_AUTH_USERNAME='user'
export DIIA_BASIC_AUTH_PASSWORD='password'
export DIIA_DEBUG=true

uvicorn app.main:app --reload
```

http://127.0.0.1:8000

http://127.0.0.1:8000/docs


## Development
```shell
poetry run isort app
poetry run black -t py37 app
poetry run flake8 app
poetry run mypy app
```
