from enum import Enum

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

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


class OutputTeacher(BaseModel):
    name: str
    nip: str


class OutputProposal(Proposal):
    id: PydanticObjectId = Field(alias="_id")
    advisorOneTeacher: OutputTeacher = None
    advisorTwoTeacher: OutputTeacher = None
    examinerOneTeacher: OutputTeacher = None
    examinerTwoTeacher: OutputTeacher = None
    examinerThreeTeacher: OutputTeacher = None


class OutputGetProposal(BaseModel):
    title: str
    advisorOneTeacher: OutputTeacher = None
    advisorTwoTeacher: OutputTeacher = None
    examinerOneTeacher: OutputTeacher = None
    examinerTwoTeacher: OutputTeacher = None
    examinerThreeTeacher: OutputTeacher = None
    thesisDocumentURL: str
    presentationSlideURL: str
    internshipCompletionCertificateURL: str
    status: Status = Status.WAITING
