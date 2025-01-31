import os
import hashlib
import tkinter as tk
from tkinter import messagebox
from plyer import notification
import shutil
import sys

# Sample virus signature database (MD5 hashes of known threats)
VIRUS_SIGNATURES = {
    "eicar_test_file": "44d88612fea8a8f36de82e1278abb02f"  # EICAR test file hash
}

# Function to calculate the MD5 hash of a file
def calculate_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            hasher = hashlib.md5()
            hasher.update(f.read())
            return hasher.hexdigest()
    except Exception as e:
        return None

# Function to scan a directory for viruses
def scan_directory(directory):
    detected_viruses = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_md5(file_path)
            if file_hash in VIRUS_SIGNATURES.values():
                detected_viruses.append((file, file_path))
    return detected_viruses

# Function to show notification and provide delete option
def show_notification(virus_name, virus_path):
    notification.notify(
        title="Virus Detected!",
        message=f"There's a virus on your computer: {virus_name}. Click to delete.",
        timeout=10
    )
    
    # GUI for delete confirmation
    root = tk.Tk()
    root.withdraw()
    if messagebox.askyesno("Virus Found", f"Virus detected: {virus_name}\nDo you want to delete it?"):
        try:
            os.remove(virus_path)
            messagebox.showinfo("Success", "Virus deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete the file: {e}")

# Function to add itself to startup
def add_to_startup():
    startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    script_path = os.path.abspath(sys.argv[0])
    dest_path = os.path.join(startup_path, os.path.basename(script_path))
    
    if not os.path.exists(dest_path):
        shutil.copy(script_path, dest_path)

# Main function to scan and handle detections
def main():
    add_to_startup()
    scan_path = input("Enter directory to scan: ")
    viruses = scan_directory(scan_path)
    
    if not viruses:
        print("No threats detected.")
    else:
        for virus_name, virus_path in viruses:
            print(f"Threat found: {virus_name} ({virus_path})")
            show_notification(virus_name, virus_path)

if __name__ == "__main__":
    main()
