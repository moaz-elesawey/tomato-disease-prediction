from sqlalchemy.util.langhelpers import class_hierarchy
from database import Base

from sqlalchemy import Column, Integer, String, Float

class Prediction(Base):
    __tablename__ = 'predictions'

    id          = Column(Integer(), primary_key=True)
    image_name  = Column(String(255), unique=True, nullable=False)
    class_name  = Column(String(255), nullable=False)
    confidance  = Column(Float(), nullable=False)
    took        = Column(Float(), nullable=True, default=1.0)

    def __repr__(self) -> str:
        return f'Prediction({self.image_name}, {self.class_name}, {round(self.confidance, 1)})'
