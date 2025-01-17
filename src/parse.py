from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Command(Enum):
    GET = "GET"
    SET = "SET"
    DEL = "DEL"
    RES = "RES" # for returning a response 


@dataclass
class CommandResult:
    command: Command
    key: str
    value: Optional[str] = None


def parse_sub_command(sub_command: str) -> tuple[str, Optional[str]]:
    sub = sub_command.split(" ", 1)
    if len(sub) == 1:
        return sub[0], None
    return sub[0], sub[1]


def parse_command(command: str) -> Optional[CommandResult]:
    try:
        cmd, rest = command.split(" ", 1)
        if cmd not in [member.value for member in Command]:
            print(f"Instruction {cmd} does not exist")
            return None

        key, value = parse_sub_command(rest)
        return CommandResult(command=Command(cmd), key=key, value=value)
    except ValueError:
        print("Invalid command format")
        return None
