from subprocess import run
import pytest

@pytest.mark.parametrize("command", ["uv", "cargo", "man", "rsync", "tar", "docker-compose"])
def test_command_exists(command: str):
    assert run(command + " --help", shell=True).returncode == 0

@pytest.mark.parametrize("command", ["cargo"])
def test_man_exists(command: str):
    assert run("man " + command, shell=True).returncode == 0
