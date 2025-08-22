from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateEvaluationDTO:
    internID: int
    score: float   # [0..100]

@dataclass
class UpdateEvaluationDTO:
    score: float   # [0..100]

@dataclass
class EvaluationResponseDTO:
    evalID: int
    internID: int
    score: float

@dataclass
class AvgEvaluationResponseDTO:
    internID: int
    avgScore: Optional[float]
