import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror


class EquipmentMaintenancePage:
    """
    Simple Equipment Maintenance page wired to the SQLite database.

    Uses these tables:
    - Equipment(EquipmentID, EquipmentTypeID, RecentMaintenanceLogID, EquipmentStatus, PurchaseDate)
    - EquipmentTypes(EquipmentTypeID, EquipmentManufacturer, EquipmentModel, EquipmentSubModel)

    IMPORTANT:
    This connects to the DB at project root: "SystemDatabase.db"
    (NOT "database/SystemDatabase.db")
    """

    DB_PATH = "SystemDatabase.db"

    def __init__(self, parent, controller=None):
        # Keep this exactly as requested
        self.frame = parent
        self.controller = controller

        # Configure grid
        self.frame.columnconfigure(0, weight=3)  # Table area
        self.frame.columnconfigure(1, weight=2)  # Form area
        self.frame.rowconfigure(0, weight=1)

        # Build UI
        self.init_table_section()
        self.init_form_section()

        # Load initial data
        self.load_equipment_from_db()

    # Allow access to the frame (required by your PageController)
    def get_frame(self):
        return self.frame

    # ---------- DB helpers ---------- #
    def _connect(self):
        # Small helper to avoid repeating connection boilerplate
        return sqlite3.connect(self.DB_PATH)

    def load_equipment_from_db(self):
        """Populate the Treeview from the Equipment + EquipmentTypes tables."""
        # Clear existing rows
        for item in self.equipment_table.get_children():
            self.equipment_table.delete(item)

        try:
            conn = self._connect()
            cur = conn.cursor()

            query = """
                SELECT
                    e.EquipmentID,
                    e.EquipmentTypeID,
                    e.EquipmentStatus,
                    e.PurchaseDate
                FROM Equipment e
                ORDER BY e.EquipmentID ASC
            """
            rows = cur.execute(query).fetchall()

            for row in rows:
                self.equipment_table.insert("", "end", values=row)

            conn.close()

        except sqlite3.Error as ex:
            showerror("Database Error", f"Failed to load equipment.\n\n{ex}")

    # ---------- Left side - Equipment Table ---------- #
    def init_table_section(self):
        table_frame = ttk.Frame(self.frame)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        title_label = ttk.Label(
            table_frame,
            text="Equipment Maintenance Records",
            font=("Arial", 14),
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Columns match the real database table Equipment
        columns = ("id", "type_id", "status", "purchase_date")
        self.equipment_table = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=18
        )

        self.equipment_table.heading("id", text="ID")
        self.equipment_table.heading("type_id", text="Type ID")
        self.equipment_table.heading("status", text="Status")
        self.equipment_table.heading("purchase_date", text="Purchase Date")

        self.equipment_table.column("id", width=70, anchor="center")
        self.equipment_table.column("type_id", width=90, anchor="center")
        self.equipment_table.column("status", width=120, anchor="center")
        self.equipment_table.column("purchase_date", width=140, anchor="center")

        self.equipment_table.grid(row=1, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.equipment_table.yview)
        self.equipment_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        table_frame.rowconfigure(1, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # When user selects a row, populate the form
        self.equipment_table.bind("<<TreeviewSelect>>", self.on_row_selected)

    # ---------- Right side - Add/Edit Form ---------- #
    def init_form_section(self):
        form_frame = ttk.Frame(self.frame)
        form_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        form_frame.columnconfigure(1, weight=1)

        title_label = ttk.Label(
            form_frame,
            text="Add / Edit Equipment",
            font=("Arial", 12, "bold"),
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Hidden / read-only selected EquipmentID
        ttk.Label(form_frame, text="Selected ID:").grid(row=1, column=0, sticky="e", pady=2)
        self.selected_id_var = tk.StringVar(value="")
        self.selected_id_entry = ttk.Entry(form_frame, textvariable=self.selected_id_var, state="readonly")
        self.selected_id_entry.grid(row=1, column=1, sticky="ew", pady=2)

        # EquipmentTypeID (FK)
        ttk.Label(form_frame, text="Equipment Type ID:").grid(row=2, column=0, sticky="e", pady=2)
        self.type_id_entry = ttk.Entry(form_frame)
        self.type_id_entry.grid(row=2, column=1, sticky="ew", pady=2)

        # Status
        ttk.Label(form_frame, text="Status:").grid(row=3, column=0, sticky="e", pady=2)
        self.status_combo = ttk.Combobox(
            form_frame,
            values=["Ok", "Due Soon", "Overdue"],
            state="readonly",
        )
        self.status_combo.grid(row=3, column=1, sticky="ew", pady=2)
        self.status_combo.set("Ok")

        # PurchaseDate
        ttk.Label(form_frame, text="Purchase Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="e", pady=2)
        self.purchase_date_entry = ttk.Entry(form_frame)
        self.purchase_date_entry.grid(row=4, column=1, sticky="ew", pady=2)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(12, 0), sticky="ew")

        add_button = ttk.Button(button_frame, text="Add", command=self.on_add_clicked)
        add_button.grid(row=0, column=0, padx=5)

        update_button = ttk.Button(button_frame, text="Update", command=self.on_update_clicked)
        update_button.grid(row=0, column=1, padx=5)

        delete_button = ttk.Button(button_frame, text="Delete", command=self.on_delete_clicked)
        delete_button.grid(row=0, column=2, padx=5)

        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.load_equipment_from_db)
        refresh_button.grid(row=0, column=3, padx=5)

        # Make form stretch nicely
        form_frame.rowconfigure(6, weight=1)

    # ---------- UI helpers ---------- #
    def clear_form(self):
        self.selected_id_var.set("")
        self.type_id_entry.delete(0, tk.END)
        self.purchase_date_entry.delete(0, tk.END)
        self.status_combo.set("Ok")

    def on_row_selected(self, _event=None):
        selected = self.equipment_table.selection()
        if not selected:
            return

        values = self.equipment_table.item(selected[0], "values")
        # values = (EquipmentID, EquipmentTypeID, EquipmentStatus, PurchaseDate)
        self.selected_id_var.set(str(values[0]))

        self.type_id_entry.delete(0, tk.END)
        self.type_id_entry.insert(0, str(values[1]) if values[1] is not None else "")

        self.status_combo.set(values[2] if values[2] else "Ok")

        self.purchase_date_entry.delete(0, tk.END)
        self.purchase_date_entry.insert(0, values[3] if values[3] else "")

    # ---------- Button callbacks (DB-backed) ---------- #
    def on_add_clicked(self):
        type_id = self.type_id_entry.get().strip()
        status = self.status_combo.get().strip()
        purchase_date = self.purchase_date_entry.get().strip()

        # Basic validation
        if not type_id.isdigit():
            showerror("Input Error", "Equipment Type ID must be a number.")
            return
        if not purchase_date:
            showerror("Input Error", "Purchase Date is required (YYYY-MM-DD).")
            return

        try:
            conn = self._connect()
            cur = conn.cursor()

            # Ensure the EquipmentType exists (simple FK safety check)
            exists = cur.execute(
                "SELECT 1 FROM EquipmentTypes WHERE EquipmentTypeID = ?",
                (int(type_id),),
            ).fetchone()
            if not exists:
                conn.close()
                showerror("Input Error", f"EquipmentTypeID {type_id} does not exist in EquipmentTypes.")
                return

            cur.execute(
                """
                INSERT INTO Equipment (EquipmentTypeID, EquipmentStatus, PurchaseDate)
                VALUES (?, ?, ?)
                """,
                (int(type_id), status, purchase_date),
            )
            conn.commit()
            conn.close()

            self.load_equipment_from_db()
            self.clear_form()
            showinfo("Success", "Equipment added successfully.")

        except sqlite3.Error as ex:
            showerror("Database Error", f"Failed to add equipment.\n\n{ex}")

    def on_update_clicked(self):
        equipment_id = self.selected_id_var.get().strip()
        if not equipment_id.isdigit():
            showerror("No Selection", "Please select a row to update.")
            return

        type_id = self.type_id_entry.get().strip()
        status = self.status_combo.get().strip()
        purchase_date = self.purchase_date_entry.get().strip()

        if not type_id.isdigit():
            showerror("Input Error", "Equipment Type ID must be a number.")
            return
        if not purchase_date:
            showerror("Input Error", "Purchase Date is required (YYYY-MM-DD).")
            return

        try:
            conn = self._connect()
            cur = conn.cursor()

            # Ensure the EquipmentType exists
            exists = cur.execute(
                "SELECT 1 FROM EquipmentTypes WHERE EquipmentTypeID = ?",
                (int(type_id),),
            ).fetchone()
            if not exists:
                conn.close()
                showerror("Input Error", f"EquipmentTypeID {type_id} does not exist in EquipmentTypes.")
                return

            cur.execute(
                """
                UPDATE Equipment
                SET EquipmentTypeID = ?, EquipmentStatus = ?, PurchaseDate = ?
                WHERE EquipmentID = ?
                """,
                (int(type_id), status, purchase_date, int(equipment_id)),
            )
            conn.commit()
            conn.close()

            self.load_equipment_from_db()
            showinfo("Updated", "Equipment updated successfully.")

        except sqlite3.Error as ex:
            showerror("Database Error", f"Failed to update equipment.\n\n{ex}")

    def on_delete_clicked(self):
        equipment_id = self.selected_id_var.get().strip()
        if not equipment_id.isdigit():
            showerror("No Selection", "Please select a row to delete.")
            return

        try:
            conn = self._connect()
            cur = conn.cursor()

            # NOTE: If maintenance logs exist referencing this equipment,
            # this delete may fail due to FK constraints depending on schema/settings.
            cur.execute("DELETE FROM Equipment WHERE EquipmentID = ?", (int(equipment_id),))
            conn.commit()
            conn.close()

            self.load_equipment_from_db()
            self.clear_form()
            showinfo("Deleted", "Equipment deleted successfully.")

        except sqlite3.Error as ex:
            showerror("Database Error", f"Failed to delete equipment.\n\n{ex}")
