import json
from pathlib import Path

from diia_client.sdk.model.metadata import Metadata
from diia_client.sdk.service.document_service import normalize_meta


DATA_PATH = Path(__file__).parent / "data"


def test_parse_metadata_data_all():
    with open(DATA_PATH / "metadata_all.json") as f:
        raw_data = json.load(f)

    meta = Metadata(**raw_data)

    assert meta.request_id == raw_data["requestId"]

    assert meta.data.foreign_passport is not None
    assert meta.data.internal_passport is not None
    assert meta.data.taxpayer_card is not None
    assert meta.data.reference_internally_displaced_person is not None
    assert meta.data.birth_certificate is not None

    assert meta.data.foreign_passport[0].first_name_en == "NADIIA"


def test_parse_metadata_data_part():
    with open(DATA_PATH / "metadata_part.json") as f:
        raw_data = json.load(f)

    raw_data = normalize_meta(raw_data)
    meta = Metadata(**raw_data)

    assert meta.request_id == raw_data["requestId"]
    assert meta.barcode is None

    assert meta.data.foreign_passport is not None
    assert meta.data.internal_passport is None
    assert meta.data.taxpayer_card is None
    assert meta.data.reference_internally_displaced_person is None
    assert meta.data.birth_certificate is None

    assert meta.data.foreign_passport[0].first_name_en == "NADIIA"
