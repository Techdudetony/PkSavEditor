# -*- coding: utf-8 -*-
import struct
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

class PokemonSaveEditor:
    def __init__(self, save_file):
        """
        Initializes the editor with the given .sav file.
        """
        if not os.path.exists(save_file):
            raise FileNotFoundError("Save file not found!")
        
        self.save_file = save_file
        self.data = self.load_save_file()
    
    def load_save_file(self):
        """
        Loads the binary data from the save file.
        """
        with open(self.save_file, 'rb') as file:  # Ensure it's opened as binary
            return bytearray(file.read())
    
    def get_trainer_name(self):
        """
        Extracts the trainer's name from the save file.
        """
        offset = 0x0000  # Example offset; actual offsets vary by game version.
        length = 7       # Max trainer name length in older Pokémon games.
        
        trainer_name = self.data[offset:offset+length].decode('latin-1', errors='ignore')
        return trainer_name.strip('\x00')
    
    def set_trainer_name(self, new_name):
        """
        Modifies the trainer's name in the save file.
        """
        offset = 0x0000  # Example offset for trainer name.
        length = 7       # Ensure new name fits within the allocated space.
        
        new_name_bytes = new_name.encode('utf-8')[:length]  # Trim if too long.
        new_name_bytes += b'\x00' * (length - len(new_name_bytes))  # Pad with nulls.
        
        self.data[offset:offset+length] = new_name_bytes
    
    def save_changes(self, output_file):
        """
        Writes modified data back to a new save file.
        """
        with open(output_file, 'wb') as file:
            file.write(self.data)
        print(f"Changes saved to {output_file}")

# Function to select a .sav file
def select_sav_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a Pokémon Save File", filetypes=[("SAV files", "*.sav")])
    return file_path

# Example usage
if __name__ == "__main__":
    save_file = select_sav_file()
    if save_file:
        save_editor = PokemonSaveEditor(save_file)
        current_name = save_editor.get_trainer_name()
        print("Current Trainer Name:", current_name)
        
        new_name = simpledialog.askstring("Trainer Name", f"Current Trainer Name: {current_name}\nEnter new trainer name:")
        if new_name:
            save_editor.set_trainer_name(new_name)
            
            save_option = simpledialog.askstring("Save File", "Enter 'overwrite' to replace the original file or a new filename to save a copy:")
            if save_option.lower() == "overwrite":
                save_editor.save_changes(save_file)
            else:
                save_editor.save_changes(save_option if save_option else "modified_game.sav")
        else:
            print("No new name entered. Exiting.")
    else:
        print("No file selected. Exiting.")
