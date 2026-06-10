from subprocess import run
import pytest

@pytest.mark.parametrize("command", ["uv", "cargo", "man", "rsync", "tar"])
def test_command_exists(command: str):
    assert run(command + " --help", shell=True).returncode == 0
