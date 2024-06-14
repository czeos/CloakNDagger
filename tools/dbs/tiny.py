from typing import Optional, List, Union
from tinydb import TinyDB, Query
from config import config
from pathlib import Path
from pydantic import BaseModel, Field, model_validator, Extra
from tools.utils import hash_fn
from tools.base import BaseEntity, BaseEntityStack, EntityRegister


# set db
def get_tinydb(path: Path) -> TinyDB:
    return TinyDB(path)

def get_query_hash(model: BaseEntity, params: Optional[dict] = None):
    """ create query record from entity and ditional params. Main query id is hash of model and prms dict"""
    query = {name: model.__getattribute__(name) for name in model.property_fields}
    if params:
        query.update(params)
    return str(hash_fn(query))


def entities_stack_to_results(stack: BaseEntityStack, query_hash) -> List[dict]:
    results = [item.dict() for item in stack.data]
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


def is_table_empty(db: TinyDB, table: str) -> bool:
    table = db.table(table)
    # Check if the table is empty
    if len(table) == 0:
        return True
    else:
        return False


class TiniDBTransitingEntity(BaseEntity, extra='allow'):
    pass


class TiniDBTransitingStack(BaseEntityStack):
    data: List[TiniDBTransitingEntity] = Field(default_factory=list)


def retrive_cnd_entity(register: EntityRegister, stack: TiniDBTransitingStack) -> List[BaseEntity]:
    if stack.data:
        return [register.get_item(item.setting.type)(**item.dict()) for item in stack.data]
    else:
        return []


class TiDBCache(BaseModel):
    db_path: Path
    entity_register: EntityRegister
    @property
    def db(self) -> TinyDB:
        return get_tinydb(self.db_path)

    def __call__(self, query: BaseEntity, params: Optional[dict] = None, count: int = 12) -> List[BaseEntity]:
        # calculate query hash
        # TODO: Refactor
        query_hash = get_query_hash(model=query, params=params)

        if not is_table_empty(self.db, table=query_hash):
            retrived = get_records(db=self.db, table=query_hash, query_hash=query_hash, count=count)
            transition = TiniDBTransitingStack(**{'results': len(retrived), "data": retrived})
            remove_records(db=self.db, table=query_hash, records=retrived)
            return retrive_cnd_entity(register=self.entity_register, stack=transition)
        else:
            self.db.drop_table(query_hash)

    def save_to_cache(self, query: BaseEntity, stack: BaseEntityStack, params: Optional[dict] = None) -> None:
        query_hash = get_query_hash(model=query, params=params)
        results = entities_stack_to_results(query_hash=query_hash, stack=stack)
        insert_to_table(db=self.db, table=query_hash, insert=results)

    def query_cache_size(self, query: BaseEntity, params: Optional[dict] = None) -> int:
        query_hash = get_query_hash(model=query, params=params)
        return len(self.db.table(query_hash))

    def exist_table(self, query: BaseEntity, params: Optional[dict] = None) -> bool:
        table = get_query_hash(model=query, params=params)
        if len(self.db.table(table)) > 0:
            return True
        else:
            return False

    def get_table_records(self, table: str, query: Query, value, count: int):
            return self.db.table(table).search(query == value)[:count]

    def insert_one_to_table(self, table: str, item: BaseEntity) -> None:
        self.db.table(table).insert(item.dict())



if __name__ == '__main__':
    from modules.hunchly.models import HunchlyFacebookPixel, HunchlyCase, HunchlyPageDatas
    from tools.entities import entity_register


    f1 = HunchlyFacebookPixel(data_record='a', data_extractor='Facebook Tracking Pixel ID', data_type='type')
    f2 = HunchlyFacebookPixel(data_record='b', data_extractor='Facebook Tracking Pixel ID', data_type='type')
    c = HunchlyCase(id=20, name='test')
    d = HunchlyPageDatas(number_of_results=2, data=[f1,f2])

    cache = TiDBCache(db_path=config.db.db_path, entity_register=entity_register)
    cache.save_to_cache(query=c, stack=d)
    cached_entities = cache(query=c)

    pass