# Diia SDK

## Usage

```python
from diia_client import Diia
from diia_client.crypto.uapki import UAPKICryptoService
from diia_client.sdk.http.requests import RequestsHTTPClient


ACQUIRER_TOKEN = '__token__'
DIIA_HOST = "https://api2.diia.gov.ua"

http_client = RequestsHTTPClient()

crypto_service = UAPKICryptoService(
    key="base64_encoded_key",
    password="password",
    certificate="base64_encoded_key_certificate",
    subject_key_id="subject_key_id",
    diia_certificate="base64_encoded_diia_certificate",
    diia_certificate_kep="base64_encoded_diia_kep_certificate",
    diia_issuer_certificate=None,
)

diia = Diia(
    acquirer_token=ACQUIRER_TOKEN,
    diia_host=DIIA_HOST,
    http_client=http_client,
    crypto_service=crypto_service,
)
print(diia.get_branches())
```


## Development

We use [poetry](https://github.com/sdispater/poetry) to manage dependencies

```shell
poetry install

poetry run isort diia_client
poetry run black -t py37 diia_client
poetry run flake8 diia_client
poetry run mypy diia_client
poetry run pytest
```

## Build

```shell
poetry build
```
