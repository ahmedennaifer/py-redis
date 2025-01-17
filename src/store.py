from parse import CommandResult, Command
from enum import Enum
from typing import Union
"""
client = sends payload like REPS(SET 1 2)
store = store k,v (1,2)
if ok 
    server = responds with +OK 
else:
    500 
=========================================
1 - decode the message, then into command result
2 - store in dict with k=k, v=v 
3 - return result 
"""

class RESPResponse(Enum):
    OK = '+OK'
    ERR = '-ERR'
    #TODO: status code in err
class KVStore:
    def __init__(self):
        self.store = {}

    def decode_resp_string(self, resp_string: str) -> Union[CommandResult, RESPResponse]:
        cleaned = resp_string.strip("b'").replace('\\r\\n', '\r\n')
        parts = cleaned.split("\r\n")       
        instruction = parts[2]
        # TODO : clean this => fn for decode set, get, del etc... declutter code 
        if instruction == "SET":
            n_parts = parts[1]
            k_length = int(parts[3][1:])
            k = parts[4]
            v_length = int(parts[5][1:])
            v = parts[6]
            assert len(v) == v_length
            assert len(k) == k_length
            assert instruction in [member.value for member in Command]
            return CommandResult(command=instruction, key=k, value=v)
            
        elif instruction == "GET":
            n_parts = parts[1]
            instruction = parts[2]
            k_length = int(parts[3][1:])
            k = parts[4]
            assert len(k) == k_length
            assert instruction in [member.value for member in Command]
            return CommandResult(command=instruction, key=k, value=None)
        
    def insert(self, parsed_resp: CommandResult):
        if not isinstance(parsed_resp, CommandResult):
            raise TypeError(f"Argument of type {type(decoded_resp_string)} is not the expected format CommandResult")
        
        if parsed_resp is None:
            raise TypeError("Expected CommandResult, got None")
        try:
            self.store[parsed_resp.key] = parsed_resp.value
            return RESPResponse.OK
        except Exception as e:
            print(f"Error inserting: {e}")
              
    def get(self, parsed_resp: CommandResult) -> Union[CommandResult, RESPResponse]:
        if self.store.get(parsed_resp.key):
            v = self.store.get(parsed_resp.key)
            return CommandResult(command=Command.RES, key=parsed_resp.key, value=v)
        else:
            raise TypeError(f"Key {parsed_resp.key} not found")
            return RESPResponse.ERR        
        
        
if __name__ == "__main__":
    kv = KVStore()
    query = "*3\r\n$3\r\nSET\r\n$4\r\nPoop\r\n$4\r\nPoop\r\n"
    print(kv.decode_resp_string(query))    
    test = CommandResult(command=Command.SET, key="1", value="2")
    print(kv.insert(test))
    print(kv.store)
    print(kv.get(test))
