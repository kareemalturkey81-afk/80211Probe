from enum import IntEnum

class FrameType(IntEnum):
    MANAGEMENT = 0  # 00
    CONTROL = 1     # 01
    DATA = 2        # 10
    EXTENSION = 3   # 11

class ManagementSubtype(IntEnum):
    ASSOCIATION_REQUEST = 0
    ASSOCIATION_RESPONSE = 1
    REASSOCIATION_REQUEST = 2
    REASSOCIATION_RESPONSE = 3
    PROBE_REQUEST = 4
    PROBE_RESPONSE = 5
    BEACON = 8
    ATIM = 9
    DISASSOCIATION = 10
    AUTHENTICATION = 11
    DEAUTHENTICATION = 12
    ACTION = 13

class ControlSubtype(IntEnum):
    BLOCK_ACK_REQ = 8
    BLOCK_ACK = 9
    PS_POLL = 10
    RTS = 11
    CTS = 12
    ACK = 13
    CF_END = 14
    CF_END_CF_ACK = 15

class DataSubtype(IntEnum):
    DATA = 0
    DATA_CF_ACK = 1
    DATA_CF_POLL = 2
    DATA_CF_ACK_CF_POLL = 3
    NULL = 4
    CF_ACK = 5
    CF_POLL = 6
    CF_ACK_CF_POLL = 7
    QOS_DATA = 8
    QOS_NULL = 12