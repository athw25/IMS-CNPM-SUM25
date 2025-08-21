from marshmallow import Schema, fields

# Schema cho TrainingProgram
class CreateProgramSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

class ProgramResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()


# Schema cho Project
class CreateProjectSchema(Schema):
    program_id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=False)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

class ProjectResponseSchema(Schema):
    id = fields.Int()
    program_id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
