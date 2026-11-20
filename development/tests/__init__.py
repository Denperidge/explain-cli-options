from typing import NamedTuple, Literal

MoreFoundIn = Literal["N/A", "More found in manual", "More found in help"]

class Scenario(NamedTuple):
    command: str
    expected: str
    more_found_in: MoreFoundIn = "N/A"


