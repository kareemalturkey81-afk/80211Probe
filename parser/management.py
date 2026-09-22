# parser/management.py
from dataclasses import dataclass
import struct

@dataclass
class BeaconFixedParameters:
    """نموذج بيانات لتخزين المعلمات الثابتة لإطار الـ Beacon."""
    timestamp: int
    beacon_interval: int
    capabilities: int

    def __str__(self) -> str:
        return (f"Timestamp: {self.timestamp}, "
                f"Beacon Interval: {self.beacon_interval} (x 1024 microseconds), "
                f"Capabilities: 0x{self.capabilities:04x}")

def parse_beacon_fixed_params(reader) -> BeaconFixedParameters:
    """
    يقرأ الحقول الثابتة الخاصة بإطار الـ Beacon (حجمها الإجمالي 12 بايت).
    """
    # 1. Timestamp (8 bytes) 
    # نستخدم الحرف 'Q' في مكتبة struct لأنه يمثل رقم كبير جداً (8 بايت / 64 بت)
    timestamp_bytes = reader.read_bytes(8)
    timestamp = struct.unpack('<Q', timestamp_bytes)[0]
    
    # 2. Beacon Interval (2 bytes)
    interval = reader.read_uint16()
    
    # 3. Capability Information (2 bytes)
    capabilities = reader.read_uint16()
    
    return BeaconFixedParameters(
        timestamp=timestamp, 
        beacon_interval=interval, 
        capabilities=capabilities
    )