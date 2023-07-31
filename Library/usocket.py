import logging
import machine
import time
import uasyncio as asyncio
import _thread

try:
    from mpy_builtins import *
    from typing import Tuple, Callable, List
except:
    pass


AF_INET = const(1)
SOCK_STREAM = const(0)
SOCK_DGRAM  = const(1)
IPPROTO_TCP = const(1)
IPPROTO_UDP = const(2)

__dns_cache = {}

async def __wrap_async(f):
    try:
        return await f()
    except BaseException as e:
        return e

class socket(object):
    def __init__(self, af:int=AF_INET, type:int=SOCK_STREAM, proto:int=IPPROTO_TCP):
        import wiolte
        self.__lte = wiolte.wiolte.get_comm() # type: wiolte.LTEModule
        self.__loop = asyncio.get_event_loop()
        self.__conn = None
        self.__thread = None
        self.__socket_type = type

    def __run_async(self, f):
        result = self.__loop.run_until_complete(__wrap_async(f))
        if isinstance(result, BaseException):
            raise result
        return result
    
    def connect(self, address:Tuple[str,int]):
        conn = self.__run_async(lambda: self.__lte.socket_open(host=address[0], port=address[1], socket_type=self.__socket_type, timeout=10000))
        if conn is None:
            raise OSError("Failed to connect")
        self.__conn = conn
        
    def send(self, data:bytes) -> int:
        if self.__conn is None:
            raise OSError("Not connected")
        result = self.__run_async(lambda: self.__lte.socket_send(connect_id=self.__conn, data=data, timeout=10000))
        return len(data) if result is not None else 0

    def sendall(self, data:bytes):
        self.send(data)

    def recv(self, bufsize:int):
        buffer = bytearray(bufsize)
        length = self.__run_async(lambda: self.__lte.socket_receive(connect_id=self.__conn, buffer=buffer, timeout=10000))
        mv = memoryview(buffer)
        return mv[:length] if length is not None else mv[:0]
    
    def read(self, size:int):
        bytes_read = 0
        buffer = None
        while True:
            data = self.recv(size - bytes_read)
            
            if len(data) == size:
                return data
            elif bytes_read + len(data) == size:
                return buffer
            else:
                if buffer is None:
                    buffer = bytearray(size)
                buffer[bytes_read:bytes_read+len(data)] = data
            bytes_read += len(data)



    def readinto(self, buf:bytearray, nbytes:int=None) -> int:
        nbytes = len(buf) if nbytes is None else nbytes
        mv = memoryview(buf)
        length = self.__run_async(lambda: self.__lte.socket_receive(connect_id=self.__conn, buffer=mv[:nbytes], offset=0))
        return 0 if length is None else length
    
    def write(self, buf:bytes, *args) -> int:
        if len(args) == 1:
            length = args[0]
            mv = memoryview(buf)
            return self.send(mv[:length])
        elif len(args) == 2:
            offset = args[2]
            length = args[1]
            mv = memoryview(buf)
            return self.send(mv[offset:offset+length])
        else:
            return self.send(buf)

    def close(self) -> None:
        self.__run_async(lambda: self.__lte.socket_close(connect_id=self.__conn, timeout=10000))

def getaddrinfo(host:str, port:int, family:int=0, type_:int=0, proto:int=0, flags:int=0):
    import wiolte
    lte = wiolte.wiolte.get_comm()
    loop = asyncio.get_event_loop()
    if host in __dns_cache:
        return __dns_cache[host]
    
    ipaddrs = loop.run_until_complete(lte.get_ip_address(host=host))
    addrs = []
    if ipaddrs is not None:
        for ipaddr in ipaddrs:
            addrs.append((family, type_, proto, host, (ipaddr, port)))
    if len(addrs) > 0:
        __dns_cache[host] = addrs
    return addrs