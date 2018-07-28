"""
@software: PyCharm
@file: async_ssh_connect.py
@time: 2018/7/26 9:51
"""
import paramiko
import asyncio
import socket

import functools

loop=asyncio.get_event_loop()
# future = asyncio.Future(loop=loop)

def new_future(loop=loop):
    return asyncio.Future(loop=loop)

async def seleep1():
    i=0
    while True:
        i+=1
        await asyncio.sleep(1)
        print(i,end=' '),

async def connect_ssh():
    future=new_future()
    address = ('127.0.0.1', 22)
    sock = socket.socket()
    _connect_ssh(future,sock,address)
    print("Wait to connect...")
    await asyncio.wait_for(future,3)
    # print(sock)
    s=paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect('127.0.0.1',22,'quxf', '1111',sock=sock)
    # print("Connect done.")
    # s.exec_command("echo a>/tmp/bb")
    shell=s.invoke_shell()
    shell.send("ls\n")
    await asyncio.sleep(1)
    print(shell.recv(65535))
    # print(sock.recv(100))
    await asyncio.sleep(1)
    # s.makefile()
    # print(shell.recv(65535))

    shell_fd=shell.makefile()

def _connect_ssh(fut,sock,address):

    fd=sock.fileno()
    sock.setblocking(False)
    try:
        sock.connect(address)
    except (BlockingIOError,IndentationError):
        fut.add_done_callback(functools.partial(_remove_writer, fd))
        loop.add_writer(fd,_sock_connect_cb,fut,sock,address)


def _remove_writer(fd,*args):
    # print(args)
    loop.remove_writer(fd)

def _sock_connect_cb(fut,sock,address):
    if fut.cancelled():
        return
    try:
        err=sock.getsockopt(socket.SOL_SOCKET,socket.SO_ERROR)
        if err!=0:
            raise OSError(err,f"Connect call failed {address}")
    except (BlockingIOError,IndentationError):
        pass
    except Exception as exc:
        # print()
        fut.set_exception(exc)
    else:
        fut.set_result(None)
        loop.remove_writer(sock.fileno())

# async def check()

# asyncio.ensure_future(connect_ssh())
# asyncio.ensure_future(seleep1())
# loop.run_forever()
loop.run_until_complete(connect_ssh())
