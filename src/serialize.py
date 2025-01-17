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
        else:
            raise TypeError(f"Expected a string, got {type(part)}")

    def serialize_to_resp(self) -> str:
        k_length = self.get_length(self.k)
        v_length = self.get_length(self.v) if self.v is not None else " "
        if self.instruction == Command.GET:
                return f"*2{self.RESP_CRLF}${len(Command.GET.value)}{self.RESP_CRLF}{Command.GET.value}{self.RESP_CRLF}${k_length}{self.RESP_CRLF}{self.k}{self.RESP_CRLF}"
                
        elif self.instruction == Command.DEL:
                return f"*2{self.RESP_CRLF}${len(Command.DEL.value)}{self.RESP_CRLF}{Command.DEL.value}{self.RESP_CRLF}${k_length}{self.RESP_CRLF}{self.k}{self.RESP_CRLF}"
                
        elif self.instruction == Command.SET:
                return f"*3{self.RESP_CRLF}${len(Command.SET.value)}{self.RESP_CRLF}{Command.SET.value}{self.RESP_CRLF}${k_length}{self.RESP_CRLF}{self.k}{self.RESP_CRLF}${v_length}{self.RESP_CRLF}{self.v}{self.RESP_CRLF}"
            
            

if __name__ == "__main__":
    test_cr = CommandResult(command=Command.GET, key="1", value="Hello")
    resp = RESP(test_cr)
    print(resp.get_length(resp.v))
    print(resp.instruction)
    print(resp.v)
    print(resp.k)
    # print(resp.get_bulk_string())
