from peewee import Model, SqliteDatabase, FloatField, DateTimeField
from datetime import datetime

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
        records = RackStatsModel.select()

        return ([record.timestamp.strftime('%Y-%m-%d %h:%M:%S') for record in records],
                [record.temperature for record in records],
                [record.humidity for record in records])