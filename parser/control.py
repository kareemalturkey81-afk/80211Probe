from models.frames import FrameControl

def parse_frame_control(fc_value: int) -> FrameControl:
    """
    يحلل قيمة الـ Frame Control (16 بت) ويستخرج الحقول والـ Flags
    باستخدام العمليات الثنائية (Bitwise Operations).
    """
    # استخراج الحقول الأساسية
    # نستخدم (Bitmask) لعزل البتات، ثم الإزاحة لليمين (>>) لقراءة قيمتها
    protocol_version = fc_value & 0b0000000000000011         # أول 2 بت
    frame_type       = (fc_value & 0b0000000000001100) >> 2  # البتات 2-3
    frame_subtype    = (fc_value & 0b0000000011110000) >> 4  # البتات 4-7
    
    # استخراج الـ Flags (كل فلاج يمثل بت واحد فقط)
    # نستخدم الإزاحة لليسار (<<) للتحقق مما إذا كان البت مفعل (1) أم لا (0)
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