from enum import Enum

from beanie import PydanticObjectId
from pydantic import Field

from models.default.base import DefaultModel


class Status(str, Enum):
    WAITING = "WAITING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class Proposal(DefaultModel):
    title: str
    advisorOne: PydanticObjectId
    advisorTwo: PydanticObjectId
    examinerOne: PydanticObjectId
    examinerTwo: PydanticObjectId
    examinerThree: PydanticObjectId
    thesisDocumentURL: str
    presentationSlideURL: str
    internshipCompletionCertificateURL: str
    status: Status = Status.WAITING

class OutputProposal(Proposal):
    id: PydanticObjectId = Field(alias="_id")