from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
Session = sessionmaker()


class Solution(Base):
    __tablename__: str = 'solutions'

    computation_id = Column(String, primary_key=True)
    user_id = Column(String, primary_key=True)
    reason = Column(String)
    status = Column(String)
    solver = Column(String)
    file_uuid = Column(String)

    def __repr__(self):
        return "<Solution(user_id='{}', computation_id='{}')>".format(
                                self.user_id, self.computation_id)
