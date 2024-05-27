import tkinter as tk
from tkinter import messagebox, filedialog

class EntryGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SpeedyTreasure v.1.0")

        self.entries = []
        self.file_path = None

        self.create_widgets()

    def create_widgets(self):
        # Common Information
        self.btn_load = tk.Button(self.root, text="Load File", command=self.load_file)
        self.btn_load.grid(row=1, column=2, padx=5, pady=5)
        self.btn_modify = tk.Button(self.root, text="Modify Selected Entry", command=self.modify_entry)
        self.btn_modify.grid(row=0, column=2, padx=5, pady=5)

        self.btn_add = tk.Button(self.root, text="Add New Entry", command=self.add_entry)
        self.btn_add.grid(row=0, column=3, padx=5, pady=5)

        self.btn_save = tk.Button(self.root, text="Save", command=self.save_file)
        self.btn_save.grid(row=1, column=3, padx=5, pady=5)
        self.lbl_base_id = tk.Label(self.root, text="Base ID:")
        self.lbl_base_id.grid(row=0, column=0)
        self.ent_base_id = tk.Entry(self.root)
        self.ent_base_id.grid(row=0, column=1)

        self.lbl_name = tk.Label(self.root, text="Name:")
        self.lbl_name.grid(row=1, column=0)
        self.ent_name = tk.Entry(self.root)
        self.ent_name.grid(row=1, column=1)

        self.lbl_location = tk.Label(self.root, text="Location:")
        self.lbl_location.grid(row=2, column=0)
        self.ent_location = tk.Entry(self.root)
        self.ent_location.grid(row=2, column=1)

        self.lbl_value = tk.Label(self.root, text="Value:")
        self.lbl_value.grid(row=3, column=0)
        self.ent_value = tk.Entry(self.root)
        self.ent_value.grid(row=3, column=1)

        self.lbl_edible = tk.Label(self.root, text="Edible (Yes/No):")
        self.lbl_edible.grid(row=4, column=0)
        self.ent_edible = tk.Entry(self.root)
        self.ent_edible.grid(row=4, column=1)

        # Entries Fields
        self.entries_frame = tk.Frame(self.root)
        self.entries_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.entry_descriptions = []
        self.entry_speaker_ids = []

        for i in range(8):
            tk.Label(self.entries_frame, text=f"Entry {i+1} Description:").grid(row=i, column=0)
            desc_entry = tk.Entry(self.entries_frame, width=50)
            desc_entry.grid(row=i, column=1)
            self.entry_descriptions.append(desc_entry)

            tk.Label(self.entries_frame, text=f"Entry {i+1} Speaker ID:").grid(row=i, column=2)
            speaker_entry = tk.Entry(self.entries_frame, width=20)
            speaker_entry.grid(row=i, column=3)
            self.entry_speaker_ids.append(speaker_entry)

        # Load and Modify Entries

        self.lst_entries = tk.Listbox(self.root, height=10, width=50)
        self.lst_entries.grid(row=11, column=0, columnspan=2, padx=5, pady=5)


        
    def add_entries_to_listbox(self):
        self.lst_entries.delete(0, tk.END)
        for name in self.entries_dict.keys():
            self.lst_entries.insert(tk.END, name)


    def add_entry(self):
        base_id = self.ent_base_id.get()
        name = self.ent_name.get()
        location = self.ent_location.get()
        value = self.ent_value.get()
        edible = self.ent_edible.get()

        for i in range(7, -1, -1):  # Start at index 7 and decrement down to 0
            description = self.entry_descriptions[i].get()
            speaker_id = self.entry_speaker_ids[i].get()
            entry = self.generate_entry(base_id, name, description, speaker_id, location, value, edible, i)
            if name in self.entries_dict:
                # Append the new entry to the list for the specified name
                self.entries_dict[name].insert(0, entry)
            else:
                self.entries_dict[name] = [entry]

        self.add_entries_to_listbox()



    def generate_entry(self, base_id, name, description, speaker_id, location, value, edible, index):
        entry_id = f"{base_id}.{index}" if index != 0 else f"{base_id}"
        entry = {
            "id": entry_id,
            "name": name,
            "description": description,
            "speaker_id": speaker_id,
            "location": location,
            "value": str(value),  # Convert to string to handle non-numeric values
            "edible": edible
        }
        return entry

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return

        self.file_path = file_path
        self.entries_dict = {}

        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split("\t")
                name = parts[1]
                if name in self.entries_dict:
                    entry = {
                        "id": parts[0],
                        "description": parts[2].strip() if len(parts) > 2 else "",
                        "speaker_id": parts[3].strip() if len(parts) > 3 else "",
                        "location": parts[4].strip() if len(parts) > 4 else "",
                        "value": parts[5] if len(parts) > 5 else None,
                        "edible": parts[8].strip() if len(parts) > 8 else ""
                    }
                    self.entries_dict[name].append(entry)
                else:
                    self.entries_dict[name] = [{
                        "id": parts[0],
                        "description": parts[2].strip() if len(parts) > 2 else "",
                        "speaker_id": parts[3].strip() if len(parts) > 3 else "",
                        "location": parts[4].strip() if len(parts) > 4 else "",
                        "value": parts[5] if len(parts) > 5 else None,
                        "edible": parts[8].strip() if len(parts) > 8 else ""
                    }]

        self.add_entries_to_listbox()

    def modify_entry(self):
        selected_index = self.lst_entries.curselection()
        if not selected_index:
            messagebox.showwarning("No Entry Selected", "Please select an entry to modify.")
            return

        selected_name = self.lst_entries.get(selected_index)
        if selected_name.startswith("  - "):  # If selected entry is an instance, get its parent name
            selected_name = selected_name.split("  - ")[1]

        selected_entries = self.entries_dict[selected_name]

        # Update entry information in the existing list
        first_entry = selected_entries[0]
        self.ent_base_id.delete(0, tk.END)
        self.ent_base_id.insert(0, first_entry["id"])

        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, selected_name)

        # Load location, value, and edible (if available) from the first entry
        self.ent_location.delete(0, tk.END)
        self.ent_location.insert(0, first_entry.get("location", ""))

        self.ent_value.delete(0, tk.END)
        self.ent_value.insert(0, first_entry.get("value", ""))

        self.ent_edible.delete(0, tk.END)
        self.ent_edible.insert(0, first_entry.get("edible", ""))

        # Update entry descriptions and speaker IDs from each instance
        for i in range(8):
            if i < len(selected_entries):
                entry = selected_entries[i]
                self.entry_descriptions[i].delete(0, tk.END)
                self.entry_descriptions[i].insert(0, entry.get("description", ""))

                self.entry_speaker_ids[i].delete(0, tk.END)
                self.entry_speaker_ids[i].insert(0, entry.get("speaker_id", ""))
            else:
                self.entry_descriptions[i].delete(0, tk.END)
                self.entry_speaker_ids[i].delete(0, tk.END)
        
    def save_file(self):
        if not self.entries_dict:
            messagebox.showwarning("No Entries", "There are no entries to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return

        self.file_path = file_path

        with open(self.file_path, 'w') as file:
            for index in range(self.lst_entries.size()):
                name = self.lst_entries.get(index)
                entries = self.entries_dict[name]
                for entry in entries:
                    file.write("\t".join([
                        entry["id"],
                        name,
                        entry["description"],
                        entry["speaker_id"],
                        entry["location"],
                        str(entry["value"]) if entry["value"] is not None else "",
                        "IGNORE",
                        "IGNORE",# Handle None values
                        entry["edible"]
                    ]) + "\n")

        messagebox.showinfo("File Saved", f"Entries saved to {self.file_path}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = EntryGeneratorApp(root)
    root.mainloop()