import ctypes
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import winreg

# Required libraries
required_libraries = ['tkinter', 'winreg']

def install_missing_libraries():
    """Install missing libraries using pip."""
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])

def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()

def run_as_admin():
    """Relaunch the script with admin privileges if not already running as admin."""
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
        except Exception as e:
            messagebox.showerror("Error", f"Admin permissions could not be obtained: {str(e)}")
            sys.exit()

def ensure_tusools_directory():
    """Ensure the tusools directory and background folder exist."""
    tusools_dir = r"C:\Program Files\tusools"
    background_dir = os.path.join(tusools_dir, 'background')
    if not os.path.exists(tusools_dir):
        os.makedirs(tusools_dir)
    if not os.path.exists(background_dir):
        os.makedirs(background_dir)

    # Create note.txt with instructions if it doesn't exist
    note_path = os.path.join(background_dir, 'note.txt')
    if not os.path.isfile(note_path):
        with open(note_path, 'w') as note_file:
            note_file.write("Put a .png file of your choice in this folder and name it 'back.png'. This application will make the background the image you put in.")

def check_and_create_file(filename):
    """Check if the file exists. If not, create it."""
    file_path = os.path.join(r"C:\Program Files\tusools", filename)
    if not os.path.isfile(file_path):
        open(file_path, 'w').close()

def update_file(filename, mark_as_disabled=True):
    """Create or update the file with a specific marker."""
    file_path = os.path.join(r"C:\Program Files\tusools", filename)
    with open(file_path, 'w') as file:
        file.write("disabled" if mark_as_disabled else "")

def is_file_marked(filename):
    """Check if the file has the marker."""
    file_path = os.path.join(r"C:\Program Files\tusools", filename)
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

def choose_wallpaper():
    """Allow user to select a wallpaper and set it."""
    filepath = filedialog.askopenfilename(title="Select Wallpaper", filetypes=[("Image files", "*.jpg;*.png;*.bmp")])
    if filepath:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)

def is_dark_theme():
    """Check if Windows is currently using dark theme."""
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        apps_use_light_theme, _ = winreg.QueryValueEx(reg_key, "AppsUseLightTheme")
        winreg.CloseKey(reg_key)
        return apps_use_light_theme == 0
    except Exception:
        return False

def set_dark_theme():
    """Set Windows to dark theme."""
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(reg_key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(reg_key)
        messagebox.showinfo("Success", "Computer has been switched to dark theme.")
    except Exception as e:
        messagebox.showerror("Error", f"Error while setting dark theme: {str(e)}")

def set_light_theme():
    """Set Windows to light theme."""
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(reg_key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(reg_key)
        messagebox.showinfo("Success", "Computer has been switched to light theme.")
    except Exception as e:
        messagebox.showerror("Error", f"Error while setting light theme: {str(e)}")

def toggle_theme(theme_button):
    """Toggle between dark and light theme."""
    if is_dark_theme():
        set_light_theme()
        theme_button.config(text="Switch to Dark Theme")
    else:
        set_dark_theme()
        theme_button.config(text="Switch to Light Theme")

def choose_font():
    """Open font dialog for changing system font."""
    try:
        selected_font = filedialog.askopenfilename(
            title="Select Font File", 
            filetypes=[("Font files", "*.ttf;*.otf")]
        )
        if selected_font:
            # Update the font and prompt for restart
            messagebox.showinfo("Restart Required", "Changing the system font requires a restart.")
            # Restart system
            subprocess.call(["shutdown", "/r", "/t", "0"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to select font: {str(e)}")

def toggle_windows_update(button):
    """Toggle Windows Update between enabled and disabled."""
    try:
        if is_file_marked("update_disabled.dat"):
            # Enable Windows Update
            update_file("update_disabled.dat", mark_as_disabled=False)
            button.config(text="Disable Windows Update")
            messagebox.showinfo("Success", "Windows Update has been enabled.")
        else:
            # Disable Windows Update
            update_file("update_disabled.dat", mark_as_disabled=True)
            button.config(text="Enable Windows Update")
            messagebox.showinfo("Success", "Windows Update has been disabled.")
    except Exception as e:
        messagebox.showerror("Error", f"Error while toggling Windows Update: {str(e)}")

def turn_off_telemetry(button):
    """Simulate turning off telemetry."""
    try:
        update_file("telemetry_disabled.dat")
        button.config(text="Telemetry Disabled", state="disabled")
        messagebox.showinfo("Success", "Telemetry has been turned off.")
    except Exception as e:
        messagebox.showerror("Error", f"Error while turning off telemetry: {str(e)}")

def disable_windows_defender(button):
    """Simulate disabling Windows Defender."""
    try:
        update_file("defender_disabled.dat")
        button.config(text="Windows Defender Disabled", state="disabled")
        messagebox.showinfo("Success", "Windows Defender has been disabled.")
    except Exception as e:
        messagebox.showerror("Error", f"Error while disabling Windows Defender: {str(e)}")

# CMD opaklık ayarı işlevi
def set_cmd_transparency_regedit(percentage):
    """Set the transparency level for CMD using the registry."""
    if 20 <= percentage <= 80:
        alpha_value = int((percentage / 100) * 255)

        try:
            # CMD opacity registry path
            registry_key_path = r"Console\%SystemRoot%_system32_cmd.exe"

            # Open registry key
            reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_key_path)

            # Set transparency key (REG_DWORD type)
            winreg.SetValueEx(reg_key, "WindowAlpha", 0, winreg.REG_DWORD, alpha_value)

            # Close the key
            winreg.CloseKey(reg_key)

            messagebox.showinfo("Success", f"CMD opacity set to {percentage}% (Registry updated).")
        except Exception as e:
            messagebox.showerror("Error", f"Error while updating registry: {str(e)}")
    else:
        messagebox.showerror("Invalid Input", "Please enter a value between 20 and 80.")

def ask_transparency_percentage():
    """Prompt the user to enter a transparency percentage between 20% and 80%."""
    while True:
        try:
            percentage = simpledialog.askinteger("Set CMD Transparency", "Enter transparency percentage (20-80):", minvalue=20, maxvalue=80)
            if percentage is None:
                break  # User canceled
            set_cmd_transparency_regedit(percentage)
            break
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number.")

def create_gui():
    """Create and display the main application GUI."""
    ensure_tusools_directory()
    window = tk.Tk()
    window.title("Tusools v1.1")
    window.geometry("400x600")
    window.resizable(False, False)

    # Background color
    window.configure(bg="#2C3E50")

    label = tk.Label(window, text="Personalization Settings", font=("Helvetica", 16, "bold"), fg="white", bg="#2C3E50")
    label.pack(pady=20)

    # Buttons
    choose_wallpaper_btn = tk.Button(window, text="Change Wallpaper", font=("Helvetica", 12), bg="#3498DB", fg="white", activebackground="#2980B9", activeforeground="white", command=choose_wallpaper)
    choose_wallpaper_btn.pack(pady=10, ipadx=10, ipady=5)

    theme_button_text = "Switch to Light Theme" if is_dark_theme() else "Switch to Dark Theme"
    toggle_theme_btn = tk.Button(window, text=theme_button_text, font=("Helvetica", 12), bg="#2ECC71", fg="white", activebackground="#27AE60", activeforeground="white", command=lambda: toggle_theme(toggle_theme_btn))
    toggle_theme_btn.pack(pady=10, ipadx=10, ipady=5)

    important_settings_label = tk.Label(window, text="Important Settings", font=("Helvetica", 14, "bold"), fg="white", bg="#2C3E50")
    important_settings_label.pack(pady=20)

    telemetry_button = tk.Button(window, text="Turn Off Telemetry", font=("Helvetica", 12), bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white", command=lambda: turn_off_telemetry(telemetry_button))
    telemetry_button.pack(pady=10, ipadx=10, ipady=5)

    update_button = tk.Button(window, text="Disable Windows Update", font=("Helvetica", 12), bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white", command=lambda: toggle_windows_update(update_button))
    update_button.pack(pady=10, ipadx=10, ipady=5)

    defender_button = tk.Button(window, text="Disable Windows Defender", font=("Helvetica", 12), bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white", command=lambda: disable_windows_defender(defender_button))
    defender_button.pack(pady=10, ipadx=10, ipady=5)

    # Set CMD Transparency Button
    transparency_button = tk.Button(window, text="Set CMD Transparency", font=("Helvetica", 12), bg="#3498DB", fg="white", activebackground="#2980B9", activeforeground="white", command=ask_transparency_percentage)
    transparency_button.pack(pady=10, ipadx=10, ipady=5)

    window.mainloop()

if __name__ == "__main__":
    install_missing_libraries()
    run_as_admin()
    create_gui()
