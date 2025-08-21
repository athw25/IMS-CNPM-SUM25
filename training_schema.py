#training_schema.py
from marshmallow import Schema, fields

class TrainingSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    status = fields.Str(required=True)

training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)
