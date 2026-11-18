from typing import NamedTuple, Literal
EXPECTED_v = "  -v, --verbose...               Use verbose output (-vv very verbose/build.rs output)\n"
#def test_v():
#    assert eco_returns("cargo -v", EXPECTED_v)

# Requires man fallback & no results for either mode fallback
EXPECTED_pkgid = """     cargo-pkgid(1)
         Print a fully qualified package specification.
"""

class Scenario(NamedTuple):
    command: str
    expected: str
    more_found_in: Literal["N/A", "More found in manual", "More found in help"]="N/A"

    
#raise ValueError(Scenario("cargo -v", "meow", more_found_in=""))


TESTS = [
    Scenario("cargo -v",EXPECTED_v),
    Scenario("cargo pkgid", EXPECTED_pkgid)  # Test searching in man cargo pkgid too
]

 
