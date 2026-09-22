# parser/information_elements.py
from dataclasses import dataclass
from typing import List

@dataclass
class InformationElement:
    """نموذج يمثل عنصر معلومات واحد (TLV) داخل الإطار."""
    id: int
    length: int
    data: bytes

    def __str__(self) -> str:
        # إذا كان الـ ID يساوي 0، فهذا يعني أنه اسم الشبكة (SSID)
        if self.id == 0:
            try:
                # نحاول تحويل البايتات إلى نص مقروء
                ssid_name = self.data.decode('utf-8')
                return f"[SSID] Name: '{ssid_name}' (Length: {self.length})"
            except UnicodeDecodeError:
                return f"[SSID] Hidden/Invalid (Length: {self.length})"
                
        # لأي عنصر آخر، نعرض رقمه وبياناته الخام
        return f"[Element ID: {self.id}] Length: {self.length}, Data(Hex): {self.data.hex()}"

def parse_information_elements(reader) -> List[InformationElement]:
    """
    يقرأ جميع عناصر المعلومات (IEs) المتبقية في الإطار.
    يستمر في القراءة في حلقة (Loop) طالما توجد بايتات متبقية.
    """
    elements = []
    
    # نحتاج على الأقل 2 بايت (للـ ID والـ Length) لنستمر
    while reader.remaining_length() >= 2:
        element_id = reader.read_uint8()
        length = reader.read_uint8()
        
        # قراءة البيانات بناءً على الطول المستخرج
        if length > 0:
            data = reader.read_bytes(length)
        else:
            data = b''
            
        elements.append(InformationElement(id=element_id, length=length, data=data))
        
    return elements