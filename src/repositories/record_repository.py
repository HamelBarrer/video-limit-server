from ..db import sqlite
from ..schemas import record_schema


def read_record():
    with sqlite.conn:
        cursor = sqlite.conn.execute(
            'select * from records order by record_id desc'
        )
        rows = cursor.fetchall()

        record_models = [record_schema.Record(
            record_id=row[0],
            name=row[1],
            location=row[2]
        ) for row in rows]

        return record_models


def record(record_id: int):
    with sqlite.conn:
        cursor = sqlite.conn.execute(
            'select * from records r where r.record_id = ?',
            (record_id,)
        )
        row = cursor.fetchone()
        if row:
            return record_schema.Record(record_id=row[0], name=row[1], location=row[2])


def registered_record(name: str, location: str):
    with sqlite.conn as conn:
        cursor = conn.cursor()
        cursor.execute(
            'insert into records(name, location) values (?, ?)', (name, location)),
        return record(cursor.lastrowid)
