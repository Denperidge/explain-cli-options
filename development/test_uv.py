from testutils import eco

EXPECTED_project = """      --project <PROJECT>
          Discover a project in the given directory [env: UV_PROJECT=]
"""
def test_project():
    assert eco("uv --project") == EXPECTED_project
