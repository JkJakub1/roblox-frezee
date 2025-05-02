import psutil
import keyboard
import time
import sys

# Global variable to track the state (whether we suspended Roblox)
roblox_suspended_by_script = False
target_process_name = "RobloxPlayerBeta.exe"  # This may need to be adjusted!

def find_roblox_process():
    """Finds the running Roblox process."""
    for proc in psutil.process_iter(['pid', 'name']):
        # Case-insensitive name comparison
        if target_process_name.lower() in proc.info['name'].lower():
            print(f"Found Roblox process: PID={proc.info['pid']}, Name={proc.info['name']}")
            return psutil.Process(proc.info['pid'])
    print(f"Process '{target_process_name}' was not found.")
    return None

def toggle_roblox_suspend_resume():
    """Toggles Roblox process between suspended and resumed."""
    global roblox_suspended_by_script  # Allow modifying the global variable

    process = find_roblox_process()

    if process:
        try:
            if not roblox_suspended_by_script:
                # If not already suspended by us, suspend it
                print(f"Suspending Roblox process (PID: {process.pid})...")
                process.suspend()
                roblox_suspended_by_script = True
                print("Roblox has been suspended.")
            else:
                # If already suspended by us, resume it
                print(f"Resuming Roblox process (PID: {process.pid})...")
                process.resume()
                roblox_suspended_by_script = False
                print("Roblox has been resumed.")
        except psutil.NoSuchProcess:
            print(f"Error: Roblox process (PID: {process.pid}) no longer exists.")
            roblox_suspended_by_script = False  # Reset state just in case
        except psutil.AccessDenied:
            print("Error: Access denied. The script lacks sufficient privileges (Try running as Administrator).")
            sys.exit("Exiting script due to insufficient permissions.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Attempt to reset state if an error occurs during operation
            if process.is_running():
                if process.status() == psutil.STATUS_STOPPED:
                    roblox_suspended_by_script = True
                else:
                    roblox_suspended_by_script = False
            else:
                roblox_suspended_by_script = False

    # If the process wasn't found, do nothing (message already shown in find_roblox_process())


# --- Main script section ---
if __name__ == "__main__":
    print("--- Roblox Suspend/Resume Script by @JkJakub11 ---")
    print(f"The script will search for a process with a name containing: '{target_process_name}'")
    print("WARNING: This script will likely require Administrator privileges!")

    while True:  # Loop until a valid keybind is entered
        try:
            keybind = input("Enter a keybind for suspend/resume (e.g., 'ctrl+alt+p', 'f10'): ").strip().lower()
            if not keybind:
                print("No keybind entered, please try again.")
                continue

            # Try registering a temporary hotkey to validate the format
            def test_func(): pass
            keyboard.add_hotkey(keybind, test_func)
            keyboard.remove_hotkey(keybind)
            print(f"Keybind '{keybind}' recognized successfully.")
            break
        except ValueError:
            print("Invalid keybind format. Use modifiers like 'ctrl', 'alt', 'shift' joined with '+' and a key (e.g., 'a', 'b', 'f1', 'space').")
        except Exception as e:
            print(f"An error occurred while registering the keybind: {e}")

    # Register the actual hotkey
    try:
        keyboard.add_hotkey(keybind, toggle_roblox_suspend_resume)
        print(f"\nScript is active. Press '{keybind}' to suspend/resume Roblox.")
        print("The script is running in the background. To stop it, close this window or press Ctrl+C.")

        while True:
            time.sleep(1)  # Sleep to avoid high CPU usage

    except Exception as e:
        print(f"\nA critical error occurred during script execution: {e}")
        input("Press Enter to exit.")
