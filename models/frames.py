from dataclasses import dataclass

@dataclass
class FrameControl:
    protocol_version: int
    type: int
    subtype: int
    
    to_ds: bool
    from_ds: bool
    more_fragments: bool
    retry: bool
    power_management: bool
    more_data: bool
    protected_frame: bool
    order: bool

    def __str__(self) -> str:
        flags = []
        if self.to_ds: flags.append("To DS")
        if self.from_ds: flags.append("From DS")
        if self.protected_frame: flags.append("Protected")
        if self.retry: flags.append("Retry")
        
        flags_str = ", ".join(flags) if flags else "None"
        
        return (f"FrameControl(Version={self.protocol_version}, "
                f"Type={self.type}, Subtype={self.subtype}, Flags=[{flags_str}])")