#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socketIO_client import SocketIO

# cl tool for meatspac.es
class SocketStream(object):

  def __init__(self, address, port):
    # connect to socket
    self.socket = SocketIO(address, port)

  def apply(self, func):
    # trigger events
    self.socket.on('message', func)

    # wait forever...
    self.socket.wait()