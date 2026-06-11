from testutils import eco
import pytest

COMMANDS = [
    {
        "command": "watch",
        "expected": "  watch                   Watch build context for service and rebuild/refresh containers when files are updated\n"
    }
]
command_names = map(lambda command: command["command"].replace(" ", "_"), COMMANDS)

@pytest.mark.parametrize("command", COMMANDS, ids=command_names)
def test_watch(command:dict):
    assert eco(f"docker-compose {command["command"]}") == command["expected"]
