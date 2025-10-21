from typing import Type, TypeVar, Generic, Protocol, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.database import engine
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy import select

T = TypeVar("T")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ReadSchemaType = TypeVar("ReadSchemaType")

class BaseRepositoryProtocol(Generic[T, CreateSchemaType, UpdateSchemaType], Protocol):
    def create(self, obj_in: CreateSchemaType) -> T: ...
    def find_by_id(self, id: int) -> Optional[T]: ...
    def update(self, id: int, obj_in: UpdateSchemaType) -> T: ...
    def delete(self, id: int) -> None: ...
    def paginate(self, query: Optional[dict] ) -> Page[T]: ...


class BaseSQLAlchemyRepository(Generic[T, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[T], session: Session = Session(engine)):
        self.model = model
        self.session = session

    def paginate(self,query: Optional[dict]) -> Page[T]:
        if query:
            return paginate(self.session, select(self.model).order_by(self.model.id))
        return paginate(self.session, select(self.model).order_by(self.model.id))

    def create(self, obj_in: CreateSchemaType) -> T:
        """Default create"""
        db_obj = self.model(**obj_in.dict())  # untuk Pydantic schema
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def find_by_id(self, id: int) -> Optional[T]:
        """Default find by id"""
        return self.session.query(self.model).filter(self.model.id == id).first()

    def update(self, id: int, obj_in: UpdateSchemaType) -> T:
        """Default update"""
        db_obj = self.find_by_id(id)
        if not db_obj:
            raise NoResultFound(f"{self.model.__name__} with id {id} not found")

        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> None:
        """Default delete"""
        db_obj = self.find_by_id(id)
        if not db_obj:
            raise NoResultFound(f"{self.model.__name__} with id {id} not found")

        self.session.delete(db_obj)
        self.session.commit()
