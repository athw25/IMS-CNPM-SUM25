from dataclasses import dataclass

@dataclass
class EvaluationDomain:
    evalID: int | None
    internID: int
    score: float
