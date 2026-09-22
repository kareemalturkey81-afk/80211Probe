# parser/addresses.py
from dataclasses import dataclass

@dataclass
class MacAddress:
    """نموذج لتمثيل عنوان MAC"""
    mac_bytes: bytes

    def __str__(self) -> str:
        # تحويل البايتات إلى الصيغة المألوفة (مثال: aa:bb:cc:dd:ee:ff)
        return ":".join(f"{b:02x}" for b in self.mac_bytes)

@dataclass
class FrameAddresses:
    """يحتوي على عناوين MAC المستخرجة من الإطار"""
    address1: MacAddress
    address2: MacAddress
    address3: MacAddress
    address4: MacAddress = None  # قد لا يكون موجوداً دائماً

def parse_addresses(reader, to_ds: bool, from_ds: bool) -> FrameAddresses:
    """
    يقرأ عناوين MAC بناءً على معايير 802.11.
    العنوان الرابع يظهر فقط إذا كان الإطار مرسلاً بين نقطتي وصول (WDS)،
    أي عندما يكون to_ds=True و from_ds=True.
    """
    addr1 = MacAddress(reader.read_bytes(6))
    addr2 = MacAddress(reader.read_bytes(6))
    addr3 = MacAddress(reader.read_bytes(6))
    
    addr4 = None
    if to_ds and from_ds:
        addr4 = MacAddress(reader.read_bytes(6))
        
    return FrameAddresses(address1=addr1, address2=addr2, address3=addr3, address4=addr4)