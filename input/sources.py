# input/sources.py
import pathlib

def read_binary_file(file_path: str) -> bytes:
    """
    يقرأ الملف الثنائي (Raw Bytes) بأمان.
    يستخدم مكتبة pathlib لضمان توافق المسارات بين Windows و Linux.
    """
    path = pathlib.Path(file_path)
    
    # معالجة الأخطاء (Error Handling) قبل محاولة الفتح
    if not path.exists():
        raise FileNotFoundError(f"الملف غير موجود في المسار المحدد: '{file_path}'")
        
    if not path.is_file():
        raise IsADirectoryError(f"المسار يشير إلى مجلد وليس ملفاً: '{file_path}'")
        
    try:
        # فتح الملف بصيغة القراءة الثنائية (rb = Read Binary)
        with open(path, 'rb') as f:
            return f.read()
    except PermissionError:
        raise PermissionError(f"ليس لديك الصلاحيات الكافية لقراءة الملف: '{file_path}'")