# tests/test_parser.py
import unittest
from parser.reader import BinaryReader
from parser.control import parse_frame_control
from parser.errors import FrameTruncatedError

class TestParser(unittest.TestCase):
    
    def test_binary_reader_success(self):
        """اختبار قدرة القارئ على قراءة البايتات بشكل صحيح."""
        data = b'\x80\x00\x11\x22'
        reader = BinaryReader(data)
        
        # قراءة أول 2 بايت (حسب نظام Little-Endian ستكون قيمتها 128)
        fc = reader.read_uint16()
        self.assertEqual(fc, 128)
        
        # قراءة بايت واحد
        b1 = reader.read_uint8()
        self.assertEqual(b1, 0x11)
        
        # التأكد من عدد البايتات المتبقية (يجب أن يبقى 1 بايت فقط)
        self.assertEqual(reader.remaining_length(), 1)
        
    def test_binary_reader_error(self):
        """اختبار معالجة الأخطاء عند إدخال بيانات ناقصة (FrameTruncatedError)."""
        data = b'\x80' # بايت واحد فقط
        reader = BinaryReader(data)
        
        # محاولة قراءة 2 بايت يجب أن تطلق خطأ بشكل آمن
        with self.assertRaises(FrameTruncatedError):
            reader.read_uint16()
            
    def test_frame_control_parsing(self):
        """اختبار صحة تحليل العمليات الثنائية لاكتشاف نوع الإطار."""
        # الرقم 128 (0x0080) يمثل إطار Beacon
        fc = parse_frame_control(128)
        
        # نؤكد للمختبر أن النوع يجب أن يكون 0 والنوع الفرعي 8
        self.assertEqual(fc.type, 0)
        self.assertEqual(fc.subtype, 8)
        self.assertFalse(fc.protected_frame) # التأكد أن الإطار غير مشفر

if __name__ == '__main__':
    unittest.main()