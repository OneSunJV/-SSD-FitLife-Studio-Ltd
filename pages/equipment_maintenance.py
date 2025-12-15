import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror


class EquipmentMaintenancePage(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        # Configure grid
        self.columnconfigure(0, weight=3)  # Table area
        self.columnconfigure(1, weight=2)  # Form area
        self.rowconfigure(0, weight=1)

        # Build UI
        self.init_table_section()
        self.init_form_section()
        
    #Allow access to the frame
    def get_frame(self):
        return self

    # ----------- Left side - Equipment Table ----------- #
    def init_table_section(self):
        table_frame = ttk.Frame(self)
        table_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        title_label = ttk.Label(
            table_frame,
            text="Equipment Maintenance Records",
            font=('Arial', 14)
        )
        title_label.grid(row=0, column=0, sticky='w', pady=(0, 10))

        # Table (Treeview)
        columns = ("name", "type", "last_service", "next_service", "status")
        self.equipment_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            height=12
        )

        self.equipment_table.heading("name", text="Name")
        self.equipment_table.heading("type", text="Type")
        self.equipment_table.heading("last_service", text="Last Service")
        self.equipment_table.heading("next_service", text="Next Service")
        self.equipment_table.heading("status", text="Status")

        for col in columns:
            self.equipment_table.column(col, width=100, anchor='center')
    
        self.equipment_table.grid(row=1, column=0, sticky='nsew')

        # Scrollbar - Vertical scrollbar for the equipment table
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.equipment_table.yview
        )
        # Attach scrollbar to the equipment table
        self.equipment_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ns')

        table_frame.rowconfigure(1, weight=1)

        # Placeholder data - until database is connected
        demo_rows = [
            ("Treadmill 1", "Cardio", "01-10-2025", "15-07-2025", "Ok"),
            ("Rowing Machine 2", "Cardio", "01-01-2025", "15-02-2025", "Due Soon"),
            ("Leg Press 1", "Strength", "18-12-2024", "18-03-2025", "Ok")
        ]
        for row in demo_rows:
            self.equipment_table.insert("", "end", values=row)

    # ----------- Right side - Add/Edit Form ----------- #
    def init_form_section(self):
        form_frame = ttk.Frame(self)
        form_frame.grid(row=0, column=1, sticky='nsew', padx=(0, 10), pady=10)

        form_frame.columnconfigure(1, weight=1)

        title_label = ttk.Label(
            form_frame,
            text="Add / Edit Equipment",
            font=('Arial', 12, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 10))

        # Labels & Entries
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky='e', pady=2)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=1, column=1, sticky='ew', pady=2)

        ttk.Label(form_frame, text="Type:").grid(row=2, column=0, sticky='e', pady=2)
        self.type_entry = ttk.Entry(form_frame)
        self.type_entry.grid(row=2, column=1, sticky='ew', pady=2)

        ttk.Label(form_frame, text="Last Service (DD-MM-YYYY):").grid(row=3, column=0, sticky='e', pady=2)
        self.last_service_entry = ttk.Entry(form_frame)
        self.last_service_entry.grid(row=3, column=1, sticky='ew', pady=2)

        ttk.Label(form_frame, text="Next Service (DD-MM-YYYY):").grid(row=4, column=0, sticky='e', pady=2)
        self.next_service_entry = ttk.Entry(form_frame)
        self.next_service_entry.grid(row=4, column=1, sticky='ew', pady=2)

        ttk.Label(form_frame, text="Status:").grid(row=5, column=0, sticky='e', pady=2)
        self.status_combo = ttk.Combobox(
            form_frame,
            values=["Ok", "Due Soon", "Overdue"],
            state="readonly"
        )
        self.status_combo.grid(row=5, column=1, sticky='ew', pady=2)
        self.status_combo.set("Ok")

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0), sticky='ew')

        add_button = ttk.Button(button_frame, text="Add Equipment", command=self.on_add_clicked)
        add_button.grid(row=0, column=0, padx=5)

        update_button = ttk.Button(button_frame, text="Update Equipment", command=self.on_update_clicked)
        update_button.grid(row=0, column=1, padx=5)

        delete_button = ttk.Button(button_frame, text="Delete Equipment", command=self.on_delete_clicked)
        delete_button.grid(row=0, column=2, padx=5)

        mark_service_button = ttk.Button(button_frame, text="Mark as Serviced", command=self.on_mark_serviced_clicked)
        mark_service_button.grid(row=0, column=3, padx=5)

    # ----------- Button Callbacks ----------- #
    def on_add_clicked(self):
        name = self.name_entry.get().strip()
        type_ = self.type_entry.get().strip()
        last = self.last_service_entry.get().strip()
        next_ = self.next_service_entry.get().strip()
        status = self.status_combo.get().strip()

        if not name:
            showerror("Input Error", "Equipment name is required.")
            return
        
        self.equipment_table.insert("", "end", values=(name, type_, last, next_, status))
        showinfo("Success", "Equipment added successfully (demo only).")

    def on_update_clicked(self):
        selected = self.equipment_table.selection()
        if not selected:
            showerror("No Selection", "Please select a row to update.")
            return
        
        name = self.name_entry.get().strip()
        type_ = self.type_entry.get().strip()
        last_ = self.last_service_entry.get().strip()
        next_ = self.next_service_entry.get().strip()
        status = self.status_combo.get().strip()

        self.equipment_table.item(selected[0], values=(name, type_, last_, next_, status))
        showinfo("Updated", "Equipment updated successfully (demo only).")

    def on_delete_clicked(self):
        selected = self.equipment_table.selection()
        if not selected:
            showerror("No Selection", "Please select a row to delete.")
            return
        
        self.equipment_table.delete(selected[0])
        showinfo("Deleted", "Equipment deleted successfully (demo only).")

    def on_mark_serviced_clicked(self):
        selected = self.equipment_table.selection()
        if not selected:
            showerror("No Selection", "Please select a row to mark as serviced.")
            return
        
        values = list(self.equipment_table.item(selected[0], "values"))
        values[4] = "Ok"
        self.equipment_table.item(selected[0], values=values)
        showinfo("Serviced", "Equipment marked as serviced (demo only).")

