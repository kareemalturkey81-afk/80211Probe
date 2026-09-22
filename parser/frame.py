# parser/frame.py
from dataclasses import dataclass
from typing import List, Any
from .reader import BinaryReader
from .control import parse_frame_control
from .addresses import parse_addresses
from .sequence import parse_sequence_control
from .management import parse_beacon_fixed_params
from .information_elements import parse_information_elements

@dataclass
class ParsedFrame:
    """
    نموذج بيانات موحد (Unified Model) يضم جميع أجزاء الإطار.
    هذا ما سيتم تمريره لاحقاً إلى نظام التقارير (JSON/HTML).
    """
    frame_control: Any
    duration: int
    addresses: Any
    sequence: Any = None
    beacon_params: Any = None
    elements: List[Any] = None

def parse_80211_frame(data: bytes) -> ParsedFrame:
    """
    الدالة الرئيسية التي تربط جميع أجزاء المحلل معاً.
    تستقبل البايتات الخام، وتقوم بالتحليل بناءً على نوع الإطار.
    """
    reader = BinaryReader(data)
    
    # 1. تحليل Frame Control و Duration (موجودة في جميع الإطارات)
    fc_bytes = reader.read_uint16()
    fc = parse_frame_control(fc_bytes)
    duration = reader.read_uint16()
    
    # 2. تحليل العناوين
    addresses = parse_addresses(reader, to_ds=fc.to_ds, from_ds=fc.from_ds)
    
    # 3. تحليل التسلسل (Sequence)
    # إطارات التحكم (Control Frames) غالباً لا تحتوي على حقل Sequence
    sequence = None
    if fc.type == 0 or fc.type == 2:  # Management (0) or Data (2)
        sequence = parse_sequence_control(reader.read_uint16())
        
    # 4. تحليل محتوى الإطار بناءً على النوع (Frame Body)
    beacon_params = None
    elements = []
    
    # إذا كان الإطار من نوع Management (0) وتحديداً Beacon (8)
    if fc.type == 0 and fc.subtype == 8:
        beacon_params = parse_beacon_fixed_params(reader)
        elements = parse_information_elements(reader)
        
    return ParsedFrame(
        frame_control=fc,
        duration=duration,
        addresses=addresses,
        sequence=sequence,
        beacon_params=beacon_params,
        elements=elements
    )