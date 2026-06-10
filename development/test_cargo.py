from testutils import eco

EXPECTED_v = "  -v, --verbose...               Use verbose output (-vv very verbose/build.rs output)\n"
def test_v():
    assert eco("cargo -v") == EXPECTED_v

# Requires man fallback & no results for either mode fallback
EXPECTED_pkgid = """     cargo-pkgid(1)
         Print a fully qualified package specification.
"""
def test_pkgid():
    assert eco("cargo pkgid") == EXPECTED_pkgid