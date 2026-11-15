from testutils import eco

EXPECTED_project_multiline = """      --project <PROJECT>
          Discover a project in the given directory [env: UV_PROJECT=]
"""
EXPECTED_project_oneline = "      --project <PROJECT>                          Discover a project in the given directory [env: UV_PROJECT=]\n"

def test_project():
    out = eco("uv --project")
    assert out in [EXPECTED_project_multiline, EXPECTED_project_oneline]
