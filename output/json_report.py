# output/json_report.py
import json

def frame_to_dict(parsed_frame) -> dict:
    """
    يحول كائن ParsedFrame إلى قاموس بايثون (Dictionary)
    لتسهيل تصديره إلى صيغة JSON.
    """
    data = {
        "frame_control": {
            "type": parsed_frame.frame_control.type,
            "subtype": parsed_frame.frame_control.subtype,
            "flags": {
                "to_ds": parsed_frame.frame_control.to_ds,
                "from_ds": parsed_frame.frame_control.from_ds,
                "protected_frame": parsed_frame.frame_control.protected_frame
            }
        },
        "duration": parsed_frame.duration,
        "mac_addresses": {
            "receiver": parsed_frame.addresses.addr1,
            "transmitter": parsed_frame.addresses.addr2,
            "bssid": parsed_frame.addresses.addr3,
        }
    }

    # إضافة التسلسل إذا كان موجوداً
    if parsed_frame.sequence:
        data["sequence_control"] = {
            "sequence_number": parsed_frame.sequence.sequence_number,
            "fragment_number": parsed_frame.sequence.fragment_number
        }

    # إضافة عناصر المعلومات (مثل اسم الشبكة SSID)
    if parsed_frame.elements:
        data["information_elements"] = []
        for ie in parsed_frame.elements:
            ie_dict = {"id": ie.id, "length": ie.length}
            
            # إذا كان العنصر هو SSID (رقم 0)، نحاول تحويله لنص مقروء
            if ie.id == 0:
                try:
                    ie_dict["ssid_name"] = ie.data.decode('utf-8')
                except UnicodeDecodeError:
                    ie_dict["ssid_hex"] = ie.data.hex()
            else:
                ie_dict["data_hex"] = ie.data.hex()
                
            data["information_elements"].append(ie_dict)

    return data

def generate_json(parsed_frame) -> str:
    """يحول القاموس إلى نص JSON مرتب ومقروء."""
    frame_dict = frame_to_dict(parsed_frame)
    # indent=4 تجعل شكل الـ JSON مرتباً بمساحات بادئة (Pretty Print)
    return json.dumps(frame_dict, indent=4)