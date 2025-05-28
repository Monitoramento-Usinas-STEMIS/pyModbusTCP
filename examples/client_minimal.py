#!/usr/bin/env python3

"""Minimal code example."""

from tecscipyModbusTCP.client import ModbusClient

# read 3 coils at @0 on localhost server
print("coils=%s" % ModbusClient().read_coils(0, 3))
