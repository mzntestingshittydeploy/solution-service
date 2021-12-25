import logging

from fastapi import FastAPI, Request, HTTPException
from sqlalchemy import create_engine

from .models import SolutionInformation, SolutionInformationInput, PastComputations
from .database import Session, Base, Solution
from .file_storage import drop_file


app = FastAPI()
logging.basicConfig(level=logging.INFO)


@app.on_event("startup")
async def init() -> None:
    engine = create_engine('sqlite:///solutions.db', echo=True)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)


@app.get("/api/solutions/user/{user_id}/", response_model=PastComputations)
@app.get("/api/solutions/user/{user_id}", include_in_schema=False, response_model=PastComputations)
def get_computations(user_id: str, http_req: Request):
    """
    Given a user, returns meta information about past computation runs
    """
    userId = http_req.headers.get("UserId")
    role = http_req.headers.get("Role")

    if userId != user_id and role != "admin":
        raise HTTPException(status_code=401)

    with Session() as session:
        solutions = session.query(Solution).filter_by(user_id=user_id)

    solution_information = list()
    for solution in solutions:
        solution_information.append(SolutionInformation(computation_id=solution.computation_id,
                                                        user_id=solution.user_id,
                                                        status=solution.status,
                                                        reason=solution.reason,
                                                        solver=solution.solver,
                                                        file_uuid=solution.file_uuid))

    return PastComputations(computations=solution_information)


@app.post("/api/solutions/upload/", include_in_schema=False)
@app.post("/api/solutions/upload", include_in_schema=False)
def add_solution(solution_request: SolutionInformationInput, http_req: Request):
    role = http_req.headers.get("Role")

    if role != "admin":
        raise HTTPException(status_code=401)

    if solution_request.body:
        file_uuid = drop_file(solution_request.body, solution_request.user_id, solution_request.computation_id)

    with Session() as session:
        solution = session.query(Solution).filter_by(computation_id=solution_request.computation_id).first()

        if solution is None:
            solution = Solution(user_id=solution_request.user_id, computation_id=solution_request.computation_id)
            session.add(solution)

        if file_uuid:
            solution.file_uuid = file_uuid

        if solution_request.status:
            solution.status = solution_request.status

        if solution_request.reason:
            solution.reason = solution_request.reason

        if solution_request.solver:
            solution.solver = solution_request.solver

        session.commit()
