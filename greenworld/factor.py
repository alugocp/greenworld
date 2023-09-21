from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class Factor:
    interval: Optional[Tuple[float, float]]
    reason: str
