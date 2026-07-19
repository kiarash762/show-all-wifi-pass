import subprocess
import re

def get_wifi_passwords():
    print("===============================")
    print("      Saved WiFi Passwords     ")
    print("===============================")

    # Get the list of all profiles
    try:
        profiles_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace")
        profile_names = re.findall(r"All User Profile\s+:\s(.*)", profiles_data)

        for name in profile_names:
            # Clean up trailing carriage returns
            name = name.strip()
            
            # Get detailed info for each profile
            profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', name, 'key=clear']).decode('utf-8', errors="backslashreplace")
            
            # Find the password (Key Content)
            password_search = re.search(r"Key Content\s+:\s(.*)", profile_info)
            
            if password_search:
                password = password_search.group(1).strip()
            else:
                password = "[No Password Found/Open Network]"

            print(f"SSID: {name}")
            print(f"Password: {password}")
            print("-" * 30)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_wifi_passwords()
    input("\nPress Enter to exit...")