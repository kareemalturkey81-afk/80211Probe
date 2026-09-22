# parser/sequence.py
from dataclasses import dataclass

@dataclass
class SequenceControl:
    """نموذج بيانات لتخزين معلومات التسلسل."""
    fragment_number: int
    sequence_number: int

    def __str__(self) -> str:
        return f"SequenceControl(Sequence Number: {self.sequence_number}, Fragment Number: {self.fragment_number})"

def parse_sequence_control(seq_value: int) -> SequenceControl:
    """
    يحلل حقل Sequence Control (16 بت) إلى:
    - Fragment Number: يأخذ أول 4 بت (نستخدم القناع 0x000F)
    - Sequence Number: يأخذ الـ 12 بت المتبقية (نستخدم القناع 0xFFF0 ثم نزيح لليمين بـ 4)
    """
    # 0x000F بالثنائي تعني 0000000000001111 (لعزل أول 4 بت)
    fragment_number = seq_value & 0x000F 
    
    # 0xFFF0 بالثنائي تعني 1111111111110000 (لعزل باقي البتات ثم دفعها لليمين)
    sequence_number = (seq_value & 0xFFF0) >> 4 
    
    return SequenceControl(
        fragment_number=fragment_number,
        sequence_number=sequence_number
    )