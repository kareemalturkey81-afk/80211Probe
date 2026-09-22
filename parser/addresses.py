# parser/addresses.py

def format_mac(mac_bytes: bytes) -> str:
    """يحول 6 بايت إلى صيغة عنوان MAC مقروءة (مثال: 00:11:22:aa:bb:cc)."""
    return ':'.join(f'{b:02x}' for b in mac_bytes)

class MacAddresses:
    """نموذج لتخزين عناوين MAC المستخرجة من الإطار."""
    def __init__(self):
        self.addr1: str = ""
        self.addr2: str = ""
        self.addr3: str = ""
        self.addr4: str = ""

    def __str__(self) -> str:
        result = f"Address 1 (Receiver):    {self.addr1}\n"
        result += f"  Address 2 (Transmitter): {self.addr2}\n"
        result += f"  Address 3 (BSSID):       {self.addr3}"
        # العنوان الرابع يستخدم فقط في حالات التوجيه اللاسلكي (WDS)
        if self.addr4:
            result += f"\n  Address 4:               {self.addr4}"
        return result

def parse_addresses(reader, to_ds: bool, from_ds: bool) -> MacAddresses:
    """
    يقرأ عناوين MAC من البيانات الثنائية.
    يعتمد عدد العناوين على مؤشرات To DS و From DS.
    """
    macs = MacAddresses()
    
    # قراءة 3 عناوين أساسية (كل عنوان يأخذ 6 بايت)
    macs.addr1 = format_mac(reader.read_bytes(6))
    macs.addr2 = format_mac(reader.read_bytes(6))
    macs.addr3 = format_mac(reader.read_bytes(6))
    
    # العنوان الرابع يظهر فقط إذا كان To DS = 1 و From DS = 1
    if to_ds and from_ds:
        macs.addr4 = format_mac(reader.read_bytes(6))
        
    return macs