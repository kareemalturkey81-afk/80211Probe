import struct
from .errors import FrameTruncatedError

class BinaryReader:
    """
    كلاس مسؤول عن قراءة البايتات الخام (Raw Bytes) بأمان.
    يتعامل مع الـ Offset (مؤشر القراءة) ويمنع القراءة خارج حدود البيانات.
    """
    
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0          # نبدأ القراءة من البداية (المؤشر صفر)
        self.length = len(data)  # الطول الإجمالي للبيانات

    def read_bytes(self, size: int) -> bytes:
        """يقرأ عدداً محدداً من البايتات ويحرك المؤشر للأمام."""
        # التحقق من أن لدينا بيانات كافية للقراءة
        if self.offset + size > self.length:
            raise FrameTruncatedError(
                f"بيانات ناقصة: مطلوب قراءة {size} بايت، والمتبقي {self.length - self.offset} بايت فقط."
            )
        
        result = self.data[self.offset : self.offset + size]
        self.offset += size
        return result

    def read_uint8(self) -> int:
        """يقرأ 1 بايت ويحوله إلى رقم صحيح."""
        chunk = self.read_bytes(1)
        return struct.unpack('<B', chunk)[0]

    def read_uint16(self) -> int:
        """يقرأ 2 بايت ويحولها إلى رقم صحيح باستخدام نظام Little-Endian."""
        chunk = self.read_bytes(2)
        return struct.unpack('<H', chunk)[0]

    def remaining_length(self) -> int:
        """يرجع عدد البايتات المتبقية التي لم تُقرأ بعد."""
        return self.length - self.offset