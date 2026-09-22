# parser/reader.py
import struct

class BinaryReader:
    """
    كلاس مسؤول عن قراءة البيانات الثنائية (Raw Bytes) الخاصة بإطارات 802.11 بطريقة آمنة.
    يحتفظ بمؤشر (offset) لمعرفة المكان الحالي للقراءة ويمنع تجاوز حدود البيانات.
    """
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0
        self.length = len(data)

    def read_bytes(self, size: int) -> bytes:
        """يقرأ عدداً محدداً من البايتات ويحرك المؤشر للأمام."""
        if self.offset + size > self.length:
            raise ValueError(f"محاولة قراءة {size} بايت ولكن المتبقي {self.length - self.offset} فقط.")
        
        result = self.data[self.offset : self.offset + size]
        self.offset += size
        return result

    def read_uint8(self) -> int:
        """يقرأ 1 بايت ويحوله إلى رقم صحيح (Unsigned 8-bit Integer)."""
        chunk = self.read_bytes(1)
        # 'B' تعني Unsigned Char (1 byte)
        return struct.unpack('<B', chunk)[0]

    def read_uint16(self) -> int:
        """
        يقرأ 2 بايت ويحولها إلى رقم صحيح.
        بروتوكول 802.11 يستخدم Little-Endian (<) للبيانات.
        """
        chunk = self.read_bytes(2)
        # '<H' تعني Little-Endian Unsigned Short (2 bytes)
        return struct.unpack('<H', chunk)[0]

    def is_eof(self) -> bool:
        """يتحقق مما إذا كنا قد وصلنا لنهاية البيانات."""
        return self.offset >= self.length