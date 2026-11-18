from . import Scenario

    

CARGO_TESTS = [
    Scenario("cargo -v", "  -v, --verbose...               Use verbose output (-vv very verbose/build.rs output)\n"),

    # Requires man fallback & no results for either mode fallback
    Scenario("cargo pkgid", """     cargo-pkgid(1)
         Print a fully qualified package specification.
""")
    # Test searching in man cargo pkgid too
]

 
