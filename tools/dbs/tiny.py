from typing import Optional, List
from tinydb import TinyDB, Query
from pathlib import Path
from pydantic import BaseModel, Field, model_validator, Extra

from tools.dbs.models import DBEntityStack
from tools.base import BaseEntity, BaseEntityStack, MaltegoSettingAttributes
from tools.utils import hash_fn

# set db
def get_tinydb(path: Path) -> TinyDB:
    return TinyDB(path)


def entities_to_results(entities: [BaseEntity], query_hash) -> List[dict]:
    results = [item.model_dump() for item in entities]
    for result in results:
        result.update({'query_hash': query_hash})
    return results


def insert_to_table(db: TinyDB, table: str, insert: List[dict]):
    db.table(table).insert_multiple(insert)


def get_records(db: TinyDB, table: str, query_hash, count) -> List[dict]:
    query = Query()
    return db.table(table).search(query.query_hash == query_hash)[:count]


def remove_records(db: TinyDB, table: str, records):
    # Remove retrieved answers from the database
    for record in records:
        db.table(table).remove(doc_ids=[record.doc_id])


def get_query_hash(query: dict, params: Optional[dict] = None) -> str:
    """ return hash of entity made entity properties """
    if params:
        query.update(params)
    return str(hash_fn(query))


class TiDBCache(BaseModel):
    db_path: Path
    @property
    def db(self) -> TinyDB:
        return get_tinydb(self.db_path)

    def get_records(self, query: BaseEntity, params: Optional[dict] = None, count: int = 12) -> DBEntityStack:
        # calculate query hash
        # TODO: Refactor
        query_hash = get_query_hash(query=query.entity_dump(exclude=[MaltegoSettingAttributes]), params=params)
        retrieved = get_records(db=self.db, table=query_hash, query_hash=query_hash, count=count)
        remove_records(db=self.db, table=query_hash, records=retrieved)
        if self.query_cache_size(query=query) == 0:
            self.db.drop_table(query_hash)

        return DBEntityStack(**{'results': len(retrieved), "data": retrieved})

    def save_to_cache(self, query: BaseEntity, entities: [BaseEntity], params: Optional[dict] = None) -> None:
        query_hash = get_query_hash(query=query.entity_dump(exclude=[MaltegoSettingAttributes]), params=params)
        results = entities_to_results(query_hash=query_hash, entities=entities)
        insert_to_table(db=self.db, table=query_hash, insert=results)

    def query_cache_size(self, query: BaseEntity, params: Optional[dict] = None) -> int:
        query_hash = get_query_hash(query=query.entity_dump(exclude=[MaltegoSettingAttributes]), params=params)
        return len(self.db.table(query_hash))

    def get_table_records(self, table: str, query: Query, value, count: int):
            return self.db.table(table).search(query == value)[:count]

    def insert_one_to_table(self, table: str, item: BaseEntity) -> None:
        self.db.table(table).insert(item.model_dump())

