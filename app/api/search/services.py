from fastapi import Depends
from db.db import db_session
from db.models.history import History
from db.models.people import People
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.processing.process import Process
from .schemas import SearchParamsSchema, SearchResponseSchema
from ..user.schemas import PeopleCreateSchema


class SearchService:
    def __init__(self, session: AsyncSession = Depends(db_session)):
        self.session = session

    async def search(self, query: SearchParamsSchema) -> SearchResponseSchema:
        # Check if the person exists in the database on single search case
        if type(query) != list:
            person = await self.session.execute(
                select(People)
                .where(People.name == str(query["name"]).lower())
                .where(People.age == query["age"])
                .where(People.gender == query["gender"])
                .where(People.occupation == query["occupation"])
            )

            person = person.scalars().first()

            # If the person exists, return the person
            if person:
                person = person.__dict__
                # Construct record to save to history
                record = {
                    "name": person["name"],
                    "age": person["age"],
                    "gender": person["gender"],
                    "occupation": person["occupation"],
                    "vip_score": person["vip_score"],
                    "is_vip": person["is_vip"],
                }

                query["result_id"] = person["id"]

                # Save query to history
                history = await self.save_query_record(query, record)

                # Construct response
                response = SearchResponseSchema(
                    name=person["name"],
                    age=person["age"],
                    occupation=person["occupation"],
                    gender=person["gender"],
                    is_vip=person["is_vip"],
                    vip_score=person["vip_score"],
                    created_at=str(history.__dict__["created_at"]),
                    updated_at=str(history.__dict__["updated_at"]),
                )

                return [response]

        # Instantiate processing class
        process = Process(query)

        # Call main method to get response
        response = await process.main()

        # Save the person to the database on single search case
        if type(query) != list:
            person = await self.save_people_record(response[0])

            # Add people id to the query
            query["result_id"] = person.id

            # Save query to history
            await self.save_query_record(query, response)

        # Return results
        return response

    async def save_query_record(self, query, response) -> History:
        # Convert query to jsonstring without result_id if it exists
        _query = {k: v for k, v in query.items() if k != "result_id"}
        query["input"] = str(_query)

        # Save query to history
        history = History(**query, result=response)
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(history)

        return history

    async def save_people_record(self, person: PeopleCreateSchema) -> People:
        saved_person = People(**person)
        self.session.add(saved_person)
        await self.session.commit()
        await self.session.refresh(saved_person)
        return saved_person
