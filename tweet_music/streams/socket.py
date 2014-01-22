#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socketIO_client import SocketIO

# cl tool for meatspac.es
class Socket(object):

  def __init__(self, address, port, func):
    # connect to socket
    socketIO = SocketIO(address, port)

    # trigger events
    socketIO.on('message', func)

    # wait forever...
    socketIO.wait()