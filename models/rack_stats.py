from peewee import Model, SqliteDatabase, FloatField, DateTimeField, fn
from datetime import datetime, timedelta

# SQLite database
_db = SqliteDatabase('rack_data.db')

class RackStatsModel(Model):
    temperature = FloatField()
    humidity = FloatField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = _db


class RackStats:
    def __init__(self):
        _db.connect()
        _db.create_tables([RackStatsModel], safe=True)

    def addRecord(self, temperature:float, humidity:float):
        new_entry = RackStatsModel.create(temperature=temperature, humidity=humidity)
        return {"temperature": new_entry.temperature, "humidity": new_entry.humidity}
    
    def readRecord(self):
        one_week_ago = datetime.now() - timedelta(days=7)

        records = RackStatsModel.select(
            RackStatsModel.timestamp,
            fn.ROUND(RackStatsModel.temperature, 2).alias('temperature'),
            fn.ROUND(RackStatsModel.humidity, 2).alias('humidity')
        ).where(
            RackStatsModel.timestamp >= one_week_ago
        )

        return ([record.timestamp.strftime('%Y-%m-%d %H:%M:%S') for record in records],
                [record.temperature for record in records],
                [record.humidity for record in records])