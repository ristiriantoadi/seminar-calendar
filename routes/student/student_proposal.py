from typing import Union

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, File, Form, UploadFile

from controllers.auth.student import get_current_user_student
from controllers.proposal.crud import (
    find_proposal_on_db,
    insert_proposal_to_db,
    update_proposal_on_db,
)
from controllers.teacher.crud_helper import find_teacher_on_db
from controllers.util.upload_file import upload_file
from models.authentication.authentication import TokenData
from models.proposal import OutputGetProposal, OutputTeacher, Proposal, Status

route_student_proposal = APIRouter(
    prefix="/student/proposal",
    tags=["Student Proposal"],
    responses={404: {"description": "Not found"}},
)


@route_student_proposal.post("")
async def add_proposal(
    title: str = Form(...),
    advisorOne: str = Form(...),
    advisorTwo: str = Form(...),
    examinerOne: str = Form(...),
    examinerTwo: str = Form(...),
    examinerThree: str = Form(...),
    thesisDocument: UploadFile = File(...),
    presentationSlide: UploadFile = File(...),
    internshipCompletionCertificate: UploadFile = File(...),
    currentUser: TokenData = Depends(get_current_user_student),
):
    thesisDocumentURL = await upload_file(
        file=thesisDocument,
        featureFolder="proposal/{userId}".format(userId=currentUser.userId),
    )
    presentationSlideURL = await upload_file(
        file=presentationSlide,
        featureFolder="proposal/{userId}".format(userId=currentUser.userId),
    )
    internshipCompletionCertificateURL = await upload_file(
        file=internshipCompletionCertificate,
        featureFolder="proposal/{userId}".format(userId=currentUser.userId),
    )
    proposal = await find_proposal_on_db({"creatorId": currentUser.userId})
    if proposal is None:
        await insert_proposal_to_db(
            proposal=Proposal(
                title=title,
                advisorOne=advisorOne,
                advisorTwo=advisorTwo,
                examinerOne=examinerOne,
                examinerTwo=examinerTwo,
                examinerThree=examinerThree,
                thesisDocumentURL=thesisDocumentURL,
                presentationSlideURL=presentationSlideURL,
                internshipCompletionCertificateURL=internshipCompletionCertificateURL,
            ),
            currentUser=currentUser,
        )
    else:
        await update_proposal_on_db(
            updateData={
                "title": title,
                "advisorOne": PydanticObjectId(advisorOne),
                "advisorTwo": PydanticObjectId(advisorTwo),
                "examinerOne": PydanticObjectId(examinerOne),
                "examinerTwo": PydanticObjectId(examinerTwo),
                "examinerThree": PydanticObjectId(examinerThree),
                "thesisDocumentURL": thesisDocumentURL,
                "presentationSlideURL": presentationSlideURL,
                "internshipCompletionCertificateURL": internshipCompletionCertificateURL,
                "status": Status.WAITING,
            },
            currentUser=currentUser,
            criteria={"creatorId": currentUser.userId},
        )
        return "OK"


@route_student_proposal.get("", response_model=Union[OutputGetProposal, None])
async def get_proposal(
    currentUser: TokenData = Depends(get_current_user_student),
):
    proposal = await find_proposal_on_db({"creatorId": currentUser.userId})
    if proposal is None:
        return None

    teacher = await find_teacher_on_db({"_id": PydanticObjectId(proposal.advisorOne)})
    if teacher:
        proposal.advisorOneTeacher = OutputTeacher(**teacher.dict())
    teacher = await find_teacher_on_db({"_id": PydanticObjectId(proposal.advisorTwo)})
    if teacher:
        proposal.advisorTwoTeacher = OutputTeacher(**teacher.dict())
    teacher = await find_teacher_on_db({"_id": PydanticObjectId(proposal.examinerOne)})
    if teacher:
        proposal.examinerOneTeacher = OutputTeacher(**teacher.dict())
    teacher = await find_teacher_on_db({"_id": PydanticObjectId(proposal.examinerTwo)})
    if teacher:
        proposal.examinerTwoTeacher = OutputTeacher(**teacher.dict())
    teacher = await find_teacher_on_db(
        {"_id": PydanticObjectId(proposal.examinerThree)}
    )
    if teacher:
        proposal.examinerThreeTeacher = OutputTeacher(**teacher.dict())

    return proposal
