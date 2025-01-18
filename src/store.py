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
 
=========     DONE    ==================
========================================
=======================================
=              RDB
======================================
1 - convert RESP to binary X
2 - add crc64 -
3 - decode back X
4 - binary file I/O -
"""

class RESPResponse(Enum):
    OK = '+OK'
    ERR = '-ERR'
    ERR_NOT_FOUND= '-ERR Key not found'
    ERR_SYNTAX_UNKNOWN = '-ERR Wrong Syntax'
    ERR_BROKEN_COMMAND = '-ERR Broken command'

    
# [REDIS][VERSION][DBNUM][KEY-TYPE][KEY][VALUE]...[EOF][CHECK]

class RedisConfig:
    REDIS_STR = b"REDIS"
    REDIS_VERSION = bytes([0,1])
    REDIS_DBNUM = bytes([1])
    RDB_STRING_TYPE = bytes([0])
    EOF = bytes([255])
    
    def convert_conf_to_binary(self):
        return b"".join([
                            self.REDIS_STR,
                            self.REDIS_VERSION,
                            self.REDIS_DBNUM,
                        ])
class KVStore:
    def __init__(self):
        self.store = {}


    def read_from_rdb_snapshot(self, file_path):
        ...
    
    def convert_store_to_binary(self):
            rs = RedisConfig()
            rdb = rs.convert_conf_to_binary()
            for k, v in self.store.items():
                key_bytes = k.encode('utf-8')
                if isinstance(v, int):
                    val_bytes = bytes([v])
                else:
                    val_bytes = str(v).encode('utf-8')
                kv_entry = b"".join([
                    rs.RDB_STRING_TYPE,
                    bytes([len(key_bytes)]),
                    key_bytes,
                    bytes([len(val_bytes)]),
                    val_bytes
                ])
                rdb += kv_entry
            rdb += rs.EOF
            return rdb 
        
    def decode_header_from_binary(self, data):
            return {
                "magic": data[0:5].decode(),
                "version": data[5:7],
                "db": data[7]
            }
        
    def decode_kvs_from_binary(self, data, start=8):
           result = {}
           pos = start
           while pos < len(data) and data[pos] != 255:
               type_marker = data[pos]
               key_len = data[pos + 1]
               key = data[pos + 2:pos + 2 + key_len].decode()
               val_len = data[pos + 2 + key_len]
               val = data[pos + 2 + key_len + 1:pos + 2 + key_len + 1 + val_len]
               result[key] = val.decode() if val_len > 1 else val[0]
               pos = pos + 2 + key_len + 1 + val_len
            self.store = result
                             
        
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

        elif instruction == "DEL":
            n_parts = parts[1]
            instruction = parts[2]
            k_length = int(parts[3][1:])
            k = parts[4]
            assert len(k) == k_length
            assert instruction in [member.value for member in Command]
            return CommandResult(command=instruction, key=k, value=None)

    def insert(self, parsed_resp: CommandResult):
        if not isinstance(parsed_resp, CommandResult):
            return RESPResponse.ERR_SYNTAX_UNKNOWN
        if parsed_resp is None:
            return RESPResponse.ERR_BROKEN_COMMAND
        try:
            self.store[parsed_resp.key] = parsed_resp.value
            return RESPResponse.OK
        except Exception as e:
            print(f"Error inserting: {e}")
              
    def get(self, parsed_resp: CommandResult) -> Union[CommandResult, RESPResponse]:
        v = self.store.get(parsed_resp.key)
        if v is not None: 
            return CommandResult(command=Command.RES, key=parsed_resp.key, value=v)
        else:
            return RESPResponse.ERR_NOT_FOUND
    
    def delete(self, parsed_resp: CommandResult) -> Union[CommandResult, RESPResponse]:
            if self.store.get(parsed_resp.key):
                self.store.pop(parsed_resp.key)
                return RESPResponse.OK
            else:
                return RESPResponse.ERR_NOT_FOUND        
             
