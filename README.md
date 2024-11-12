Project Overview

The Diia API SDK allows developers to integrate with the Diia digital services platform for functionalities like document signing and sharing. This SDK enables:
- Authentication to securely access API.
- Document signing with multiple algorithm options.
- Branch and Offer Management.
- Obtaining deeplinks for document signing scenario.

Project Contents

The SDK includes the following files and folders:
- `diia_client/sdk/diia.py`: Main API client class for interacting with the Diia platform.
- `tests/`: A collection of test files for ensuring parsing and handling metadata in documents.
- `poetry.lock` and `pyproject.toml`: Configuration files for managing dependencies.
- `README.md`: Project documentation with usage instructions.

Dependencies

Use [poetry](https://github.com/sdispater/poetry) to manage dependencies

```shell
poetry install

poetry run isort diia_client
poetry run black -t py37 diia_client
poetry run flake8 diia_client
poetry run mypy diia_client
poetry run pytest
```

Configuration Details
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

## Build

```shell
poetry build
```


Testing

The SDK includes test files to validate its functionality, such as parsing and handling metadata in documents. These tests are located in the tests/ directory.

```test_parse_metadata_data_all()``` checks if the Metadata model can parse and validate a complete metadata document, ensuring that fields like foreign_passport, internal_passport, and taxpayer_card are correctly loaded.
```test_parse_metadata_data_part()``` tests partial metadata data parsing, confirming that optional fields can be handled gracefully when absent, with normalization applied through normalize_meta().

Our scenarios: 
Sharing scenario
Review Technical Documentation
Please review the general technical documentation available here.
Diia Signature scenario
Review Technical Documentation
Please review the general technical documentation available here.

Obtaining a Test Token
To obtain a test token, please complete the application form here.
These steps provide initial access to the API for testing and preparing your integration with the system.

Important links
https://integration.diia.gov.ua/en/home.html - description of all available services
https://t.me/AiDiiaStartBot -reach us out to start the integration
