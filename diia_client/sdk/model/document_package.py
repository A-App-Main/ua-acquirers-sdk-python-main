from dataclasses import dataclass
from typing import List, Optional

from diia_client.sdk.model.decoded_file import DecodedFile
from diia_client.sdk.model.metadata import Metadata


@dataclass
class DocumentPackage:
    request_id: Optional[str]
    files: List[DecodedFile]
    data: Metadata
