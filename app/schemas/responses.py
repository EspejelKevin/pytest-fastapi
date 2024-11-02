from typing import Any

from fastapi.encoders import jsonable_encoder


class MetadataResponse:
    def __init__(self, transaction_id: str) -> None:
        self.transaction_id = transaction_id


class BaseResponse:
    def __init__(self, data: Any, meta: MetadataResponse) -> None:
        self.response = data
        self.metadata = meta


class Response:
    def __init__(self, data: Any, transaction_id: str, status_code: int = 200) -> None:
        self.__meta = MetadataResponse(transaction_id)
        self.__base_response = BaseResponse(data, self.__meta)
        self.content = jsonable_encoder(self.__base_response)
        self.status_code = status_code
