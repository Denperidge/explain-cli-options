from typing import NamedTuple, Literal

class Scenario(NamedTuple):
    command: str
    expected: str
    more_found_in: Literal["N/A", "More found in manual", "More found in help"]="N/A"


