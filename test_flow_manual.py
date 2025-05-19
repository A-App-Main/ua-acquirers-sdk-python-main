#!/usr/bin/env python

"""
Usage:

export DIIA_ACQUIRER_TOKEN=token

# install requirements:
pip install requests pyqrcode[png]

# run script with desirable mode:
python3 test_flow_manual.py deep_link
python3 test_flow_manual.py validate_barcode
python3 test_flow_manual.py sharing_barcode
python3 test_flow_manual.py sign_files

python3 test_flow_manual.py clear_branches
"""


import base64
import os
import sys
import uuid
from enum import Enum

import pyqrcode

from diia_client import Diia, DiiaIDAction, DocumentType
from diia_client.crypto.base_service import AbstractCryptoService
from diia_client.sdk.http.requests import RequestsHTTPClient
from diia_client.sdk.model import File


DIIA_HOST = "https://api2.diia.gov.ua"
TEST_HASH = b"HCJOaeQHM/5LwMr7Mfj7mA7q8l6Dt6ADHUW76Lwv+J4="  # 'test data'


class EmptyCryptoService(AbstractCryptoService):
    """Empty crypto service for testing API without decrypt part."""

    def decrypt(self, encrypted_data: str) -> str:
        raise NotImplementedError()

    def calc_hash(self, data: str) -> str:
        return data


class Mode(Enum):
    deep_link = "deep_link"
    validate_barcode = "validate_barcode"
    sharing_barcode = "sharing_barcode"
    sign_files = "sign_files"
    clear_branches = "clear_branches"


def main(*, mode: Mode, acquirer_token: str, auth_acquirer_token: str) -> None:
    print(f"Run in mode: {mode}")

    http_client = RequestsHTTPClient()

    crypto_service = EmptyCryptoService()

    diia = Diia(
        acquirer_token=acquirer_token,
        auth_acquirer_token=auth_acquirer_token,
        diia_host=DIIA_HOST,
        http_client=http_client,
        crypto_service=crypto_service,
    )

    if mode == Mode.clear_branches:
        branches = diia.get_branches()
        for branch in branches.branches:
            print(f"delete_branch:  {branch.id}")
            diia.delete_branch(branch.id)
        print("### BranchList after deletion: ", diia.get_branches())
        exit()

    if mode == Mode.sign_files:
        sharing = None
        document_identification = None
        diia_id = [DiiaIDAction.HASHED_FILES_SIGNING]
    else:
        sharing = [DocumentType.INTERNAL_PASSPORT]
        document_identification = [DocumentType.INTERNAL_PASSPORT]
        diia_id = None

    print("### create_branch")
    branch = diia.create_branch(
        name="Вчасно Тест",
        email="test@vchasno.ua",
        region="Київська обл.",
        district="Києво-Святошинський р-н",
        location="м. Вишневе",
        street="вул. Київська",
        house="2г",
        sharing=sharing,
        document_identification=document_identification,
        diia_id=diia_id,
    )
    print("Branch: ", branch)
    branch_id = branch.id

    print("### get_branch")
    print("Branch: ", diia.get_branch(branch_id=branch.id))

    print("### update_branch")

    branch.house = "3г"
    branch_updated = diia.update_branch(branch)
    assert branch_updated.id == branch_id
    assert branch_updated.house == branch.house

    print("### get_branches")
    print("BranchList: ", diia.get_branches())

    print("### create_offer")
    offer = diia.create_offer(
        branch_id=branch_id,
        name="Тестовий офер",
        return_link=None,
        sharing=sharing,
        diia_id=diia_id,
    )
    print("Offer: ", offer)
    offer_id = offer.id

    print("### get_offers")
    print("OfferList: ", diia.get_offers(branch_id=branch_id, skip=0, limit=10))

    request_id = str(uuid.uuid4())

    try:
        if mode == Mode.deep_link:
            print("### request_id: ", request_id)
            deep_link = diia.get_deep_link(
                branch_id=branch_id,
                offer_id=offer_id,
                request_id=request_id,
            )
            print("### deep_link: ", deep_link)
            pyqrcode.create(deep_link).show()

        elif mode == Mode.sign_files:
            print("### request_id: ", request_id)
            deep_link = diia.get_sign_deep_link(
                branch_id=branch_id,
                offer_id=offer_id,
                request_id=request_id,
                files=[
                    File(filename="test_data.txt", data=base64.b64decode(TEST_HASH))
                ],
            )
            print("### deep_link: ", deep_link)
            pyqrcode.create(deep_link).show()

        else:
            barcode = input("Input Diia App barcode and press Enter: ")
            if mode == Mode.sharing_barcode:
                print("### request_id: ", request_id)
                print(
                    "request_document_by_barcode: ",
                    diia.request_document_by_barcode(
                        branch_id=branch_id,
                        barcode=barcode,
                        request_id=request_id,
                    ),
                )
            if mode == Mode.validate_barcode:
                print(
                    "validate_document_by_barcode: ",
                    diia.validate_document_by_barcode(
                        branch_id=branch_id,
                        barcode=barcode,
                    ),
                )
    except Exception as e:
        raise e

    finally:
        input("\nPress Enter to finish script (delete created branch/offer) ")

        print("### delete_offer")
        diia.delete_offer(branch_id=branch_id, offer_id=offer_id)
        print(
            "### OfferList after deletion: ",
            diia.get_offers(branch_id=branch_id, skip=0, limit=10),
        )

        print("### delete_branch")
        diia.delete_branch(branch_id)
        print("### BranchList after deletion: ", diia.get_branches())


if __name__ == "__main__":
    acquirer_token = os.environ["DIIA_ACQUIRER_TOKEN"]
    mode = Mode(sys.argv[1]) if len(sys.argv) == 2 else Mode.deep_link
    main(mode=mode, acquirer_token=acquirer_token)
