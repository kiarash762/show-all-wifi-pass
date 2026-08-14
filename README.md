# Show All Wi-Fi Passwords (Python Script)

A simple, robust, and optimized Python script to extract and display all saved Wi-Fi networks along with their passwords on Windows OS.

---

## 📋 Features & Enhancements

- **Encoding Support:** Uses UTF-8 (`chcp 65001`) to properly handle special characters, non-English SSID names, and emojis.
- **Robust Parsing:** Uses regular expressions (Regex) and safe string splitting to accurately parse network profiles and passwords regardless of system language.
- **CSV Export:** Option to save extracted network details directly into a clean `wifi_passwords.csv` file for logging or backup.
- **Error Handling:** Safely handles open networks (no password) and execution exceptions.

---

## 💻 Python Source Code (`show_wifi_pass.py`)

```python
import subprocess
import re
import csv
from typing import List, Dict

def run_command(command: str) -> str:
    # Executes OS commands with UTF-8 encoding configuration.
    full_cmd = f"chcp 65001 > nul && {command}"
    try:
        return subprocess.check_output(full_cmd, shell=True, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
    except subprocess.CalledProcessError:
        return ""

def get_wifi_profiles() -> List[str]:
    # Retrieves all saved Wi-Fi profile names.
    output = run_command("netsh wlan show profiles")
    profiles = []
    
    for line in output.splitlines():
        if ":" in line:
            parts = line.split(":", 1)
            key, val = parts[0].strip(), parts[1].strip()
            if val and not any(kw in key.lower() for kw in ["interface", "hosted"]):
                if "profile" in key.lower() or "user" in key.lower():
                    profiles.append(val)
    return profiles

def get_wifi_passwords() -> List[Dict[str, str]]:
    # Extracts passwords for each Wi-Fi profile.
    profiles = get_wifi_profiles()
    results = []

    print(f"\n{'Wi-Fi Name (SSID)':<35} | {'Password':<25}")
    print("-" * 63)

    for profile in profiles:
        cmd = f'netsh wlan show profile name="{profile}" key=clear'
        profile_info = run_command(cmd)

        password_match = re.search(r"(?:Key Content|محتوای کلید)\s*:\s*(.*)", profile_info, re.IGNORECASE)
        
        if password_match:
            password = password_match.group(1).strip()
        else:
            password = "<Open / No Password>"

        results.append({"ssid": profile, "password": password})
        print(f"{profile:<35} | {password:<25}")

    return results

def save_to_csv(data: List[Dict[str, str]], filename: str = "wifi_passwords.csv") -> None:
    # Saves extracted data to a CSV file.
    try:
        with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=["ssid", "password"])
            writer.writeheader()
            writer.writerows(data)
        print(f"\n✅ Results successfully saved to '{filename}'.")
    except Exception as e:
        print(f"\n❌ Error saving file: {e}")

if __name__ == "__main__":
    wifi_data = get_wifi_passwords()
    
    save_choice = input("\nDo you want to save the results to a CSV file? (y/n): ").strip().lower()
    if save_choice == 'y':
        save_to_csv(wifi_data)
```

---

## 🚀 Usage Instructions

1. **Prerequisites:** Ensure Python 3.x is installed on your Windows system.
2. **Run the Script:** Open Command Prompt or Terminal in the script directory and run:

```bash
python show_wifi_pass.py
```

---

## ⚠️ Notes & Requirements

- **OS Compatibility:** Designed specifically for **Windows** (utilizes the `netsh` CLI tool).
- **Administrator Privileges:** To view passwords for all stored network profiles, run Command Prompt / Terminal as **Administrator**.