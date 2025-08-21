from marshmallow import Schema, fields, validate
from src.enums import AssignmentStatus

class CreateAssignmentSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(required=False, allow_none=True)
    project_id = fields.Int(required=True)
    intern_id = fields.Int(required=True)

class AssignmentResponseSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    project_id = fields.Int(required=True)
    intern_id = fields.Int(required=True)
    status = fields.Str(required=True, validate=validate.OneOf([s.value for s in AssignmentStatus]))

class UpdateAssignmentStatusSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf([s.value for s in AssignmentStatus]))
