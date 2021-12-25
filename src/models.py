from typing import List, Optional

from pydantic import BaseModel


class SolutionInformationInput(BaseModel):
    user_id: str
    computation_id: str
    status: Optional[str]
    reason: Optional[str]
    solver: Optional[str]
    body: Optional[str]


class SolutionInformation(BaseModel):
    user_id: str
    computation_id: str
    status: str
    reason: Optional[str]
    solver: Optional[str]
    file_uuid: Optional[str]


class PastComputations(BaseModel):
    computations: List[SolutionInformation]


class SignedUrl(BaseModel):
    fileUUID: str
    url: str


class File(BaseModel):
    userID: str
    fileName: str
    fileUUID: str
