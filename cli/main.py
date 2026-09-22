# cli/main.py
import argparse
import sys
from parser.frame import parse_80211_frame
from output.json_report import generate_json
from output.html_report import generate_html
from input.sources import read_binary_file

__version__ = "1.0.0"

def setup_cli():
    parser = argparse.ArgumentParser(description="80211Probe - Advanced IEEE 802.11 Parser")
    parser.add_argument('--version', action='version', version=f'80211Probe v{__version__}')
    
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")
    
    parse_parser = subparsers.add_parser('parse', help='Parse an 802.11 binary file')
    parse_parser.add_argument('file', help='Path to the binary file')
    parse_parser.add_argument('--json', action='store_true', help='Output results in JSON format')
    parse_parser.add_argument('--html', action='store_true', help='Generate an HTML report file')

    return parser

def main():
    parser = setup_cli()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    if args.command == 'parse':
        try:
            raw_bytes = read_binary_file(args.file)
            parsed_frame = parse_80211_frame(raw_bytes)
            
            # إذا طلب المستخدم تقرير HTML
            if args.html:
                html_content = generate_html(parsed_frame)
                report_name = f"report_{args.file}.html".replace("\\", "").replace("/", "")
                with open(report_name, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"[+] تم إنشاء تقرير HTML بنجاح: {report_name}")
                
            # إذا طلب المستخدم JSON
            elif args.json:
                print(generate_json(parsed_frame))
                
            # الوضع الافتراضي (نص عادي)
            else:
                print(f"[*] Successfully parsed file: {args.file}\n")
                print(f"Type:      {parsed_frame.frame_control.type}")
                print(f"Subtype:   {parsed_frame.frame_control.subtype}")
                print(f"Source:    {parsed_frame.addresses.addr2}")
                if parsed_frame.elements:
                    print(f"Network:   {parsed_frame.elements[0]}")
                    
        except Exception as e:
            print(f"[-] خطأ: {e}")