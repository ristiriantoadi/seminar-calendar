from fastapi import APIRouter, Depends, File, Form, UploadFile

from controllers.auth.student import get_current_user_student
from controllers.proposal.crud import insert_proposal_to_db
from controllers.util.upload_file import upload_file
from models.authentication.authentication import TokenData
from models.proposal import Proposal

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
    return "OK"
