from config.mongo_collection import PROPOSAL
from controllers.util.crud import find_one_on_db, insert_one_on_db, update_on_db
from models.authentication.authentication import TokenData
from models.proposal import OutputProposal, Proposal


async def insert_proposal_to_db(
    proposal: Proposal,
    currentUser: TokenData,
):
    await insert_one_on_db(
        collection=PROPOSAL, data=proposal.dict(), currentUser=currentUser
    )


async def find_proposal_on_db(criteria: dict):
    proposal = await find_one_on_db(collection=PROPOSAL, criteria=criteria)
    if proposal:
        return OutputProposal(**proposal)


async def update_proposal_on_db(
    criteria: dict, updateData: dict, currentUser: TokenData
):
    await update_on_db(
        collection=PROPOSAL,
        updateData=updateData,
        currentUser=currentUser,
        criteria=criteria,
    )
