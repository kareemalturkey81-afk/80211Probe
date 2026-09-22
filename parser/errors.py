class ParserError(Exception):
    """الفئة الأساسية لجميع أخطاء التحليل في المشروع."""
    pass

class FrameTruncatedError(ParserError):
    """يحدث عندما يكون الإطار أقصر من المتوقع (بيانات ناقصة)."""
    pass

class InvalidFrameFormat(ParserError):
    """يحدث عندما تكون البيانات غير صالحة أو لا تطابق معايير 802.11."""
    pass