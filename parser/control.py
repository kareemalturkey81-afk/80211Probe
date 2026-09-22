# parser/control.py
from models.frames import FrameControl

def parse_frame_control(fc_value: int) -> FrameControl:
    """
    يحلل قيمة الـ Frame Control (16 بت) باستخدام Bitwise Operations.
    بروتوكول 802.11 يقسم هذه الـ 16 بت كالتالي:
    
    البايت الأول:
    - Protocol Version: 2 bits
    - Type: 2 bits
    - Subtype: 4 bits
    
    البايت الثاني (Flags):
    - To DS, From DS, More Frag, Retry, Power Mgmt, More Data, Protected, Order (1 بت لكل منها)
    """
    
    # استخراج الحقول من البايت الأول (البتات من 0 إلى 7)
    protocol_version = fc_value & 0b00000011                  # قناع لأول 2 بت
    frame_type       = (fc_value & 0b00001100) >> 2           # إزاحة بمقدار 2
    frame_subtype    = (fc_value & 0b11110000) >> 4           # إزاحة بمقدار 4

    # استخراج الـ Flags من البايت الثاني (البتات من 8 إلى 15)
    to_ds            = bool(fc_value & (1 << 8))
    from_ds          = bool(fc_value & (1 << 9))
    more_fragments   = bool(fc_value & (1 << 10))
    retry            = bool(fc_value & (1 << 11))
    power_management = bool(fc_value & (1 << 12))
    more_data        = bool(fc_value & (1 << 13))
    protected_frame  = bool(fc_value & (1 << 14))
    order            = bool(fc_value & (1 << 15))

    return FrameControl(
        protocol_version=protocol_version,
        type=frame_type,
        subtype=frame_subtype,
        to_ds=to_ds,
        from_ds=from_ds,
        more_fragments=more_fragments,
        retry=retry,
        power_management=power_management,
        more_data=more_data,
        protected_frame=protected_frame,
        order=order
    )