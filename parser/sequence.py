# parser/sequence.py
from dataclasses import dataclass

@dataclass
class SequenceControl:
    """نموذج لتمثيل حقل التحكم في التسلسل (Sequence Control)"""
    fragment_number: int
    sequence_number: int

    def __str__(self) -> str:
        return f"Seq: {self.sequence_number}, Frag: {self.fragment_number}"

def parse_sequence_control(seq_value: int) -> SequenceControl:
    """
    يحلل 16 بت باستخدام Bitwise Operations:
    - أول 4 بت: Fragment Number
    - الـ 12 بت المتبقية: Sequence Number
    """
    frag_num = seq_value & 0b0000000000001111        # قناع لأول 4 بت
    seq_num  = (seq_value & 0b1111111111110000) >> 4 # قناع وإزاحة لآخر 12 بت
    
    return SequenceControl(fragment_number=frag_num, sequence_number=seq_num)