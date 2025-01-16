from parse import CommandResult, Command
from typing import Union


# TODO: empty strings
# TODO: null strings
# TODO: arrays
# TODO: null array
# TODO: empty array


class RESP:
    RESP_CRLF = r"\r\n"
    RESP_STRING_START = "+"
    RESP_ERROR_START = "-"
    RESP_INT_START = ":"

    def __init__(self, command: CommandResult):
        self.k = command.key
        self.v = command.value
        self.instruction = command.command

    def get_length(self, part: Union[str, None]):
        if isinstance(part, str):
            return len(part)
        elif isinstance(part, None):
            raise ValueError("Got empty part")
        else:
            raise TypeError(f"Expected a string, got {type(part)}")

    def get_bulk_string_start(self, part) -> str:
        length = self.get_length(part)
        return f"${length}{self.RESP_CRLF}{part}"


if __name__ == "__main__":
    test_cr = CommandResult(command=Command.SET, key="1", value="Hello")
    resp = RESP(test_cr)
    print(resp.get_length(resp.v))
    print(resp.v)
    print(resp.k)
    print(resp.get_bulk_string_start(resp.v))
