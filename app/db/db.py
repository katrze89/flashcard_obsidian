from functools import reduce
from pathlib import Path
from typing import Any, cast

from tinydb import Query, TinyDB
from tinydb.table import Document


class DB:
    def __init__(self, db_dir: Path, db_file_name: str):
        self._db = TinyDB(db_dir / f"{db_file_name}.json", create_dirs=True)

    def create(self, item: dict) -> int:
        return cast(int, self._db.insert(item))

    def create_many(self, items: list[dict]) -> list[int]:
        return cast(list[int], self._db.insert_multiple(items))

    def get(self, idx: int) -> dict:
        return self._transform_result(self._db.get(doc_id=idx))

    def read(self, ids: list[int]) -> list[dict]:
        return self._transform_results(self._db.get(doc_ids=ids))

    def filter(self, **kwargs: dict) -> list[dict]:
        query = Query()
        response = self._db.search(reduce(lambda x, y: x & y, [getattr(query, k) == v for k, v in kwargs.items()]))
        return self._transform_results(response)

    def read_all(self) -> list[dict]:
        return self._transform_results(self._db.all())

    def count(self) -> int:
        return len(self._db)

    def __enter__(self) -> "DB":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        self._db.close()

    def _transform_result(self, result: Document) -> dict:
        return {**result, "id": result.doc_id}

    def _transform_results(self, result: list[Document]) -> list[dict]:
        return [{**c, "id": c.doc_id} for c in result]
