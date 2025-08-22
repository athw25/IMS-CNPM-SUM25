from dataclasses import dataclass
from marshmallow import class_schema

# ---- Request DTOs
@dataclass
class CreateEvaluationDTO:
    internID: int
    score: float

CreateEvaluationSchema = class_schema(CreateEvaluationDTO)

@dataclass
class UpdateEvaluationDTO:
    score: float

UpdateEvaluationSchema = class_schema(UpdateEvaluationDTO)

# ---- Response DTOs
@dataclass
class EvaluationResponseDTO:
    evalID: int
    internID: int
    score: float

EvaluationResponseSchema = class_schema(EvaluationResponseDTO)

@dataclass
class AvgResponseDTO:
    internID: int
    avgScore: float | None

AvgResponseSchema = class_schema(AvgResponseDTO)
