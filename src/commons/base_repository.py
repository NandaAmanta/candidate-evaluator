from typing import Type, TypeVar, Generic, Protocol, Optional, Dict, Any, List
from math import ceil
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.database import engine
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy import select, asc, desc, or_
from src.commons.schemas import PaginatedResponse

T = TypeVar("T")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")
ReadSchemaType = TypeVar("ReadSchemaType")

class BaseRepositoryProtocol(Generic[T, CreateSchemaType, UpdateSchemaType], Protocol):
    def create(self, obj_in: CreateSchemaType) -> T: ...
    def find_by_id(self, id: int) -> Optional[T]: ...
    def update(self, id: int, obj_in: UpdateSchemaType | dict) -> T: ...
    def delete(self, id: int) -> None: ...
    def paginate(self, query: Optional[dict] ) -> PaginatedResponse[T]: ...


class BaseSQLAlchemyRepository(Generic[T, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[T], session: Session = Session(engine)):
        self.model = model
        self.session = session

    def paginate(self, query: Dict[str, Any]) -> PaginatedResponse[T]:
        page = int(query.get("page", 1))
        limit = int(query.get("limit", 10))
        search = query.get("search")
        sort_by = query.get("sort_by", "id")
        order = query.get("order", "desc")

        q = self.session.query(self.model)

        if search and self.searchable_fields:
            search_conditions = [
                getattr(self.model, field).ilike(f"%{search}%")
                for field in self.searchable_fields
                if hasattr(self.model, field)
            ]
            if search_conditions:
                q = q.filter(or_(*search_conditions))

        reserved_keys = {"page", "limit", "search", "sort_by", "order"}
        for key, value in query.items():
            if key not in reserved_keys and hasattr(self.model, key):
                column = getattr(self.model, key)
                q = q.filter(column == value)

        if hasattr(self.model, sort_by):
            sort_column = getattr(self.model, sort_by)
            q = q.order_by(asc(sort_column) if order.lower() == "asc" else desc(sort_column))

        total = q.count()
        items: List[T] = (
            q.offset((page - 1) * limit).limit(limit).all()
        )
        
        return PaginatedResponse(
            total=total,
            page=page,
            pages=ceil(total / limit),
            limit=limit,
            items=items
        )

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

    def update(self, id: int, obj_in: UpdateSchemaType | dict) -> T:
        """Default update"""
        db_obj = self.find_by_id(id)
        if not db_obj:
            raise NoResultFound(f"{self.model.__name__} with id {id} not found")

        if isinstance(obj_in, dict):
            obj_data = obj_in
        else:
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
