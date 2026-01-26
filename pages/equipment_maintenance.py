import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
from datetime import datetime, date


class EquipmentMaintenancePage:
    """
    Equipment Maintenance page (Tkinter/ttk) wired to SQLite.

    UI date format: DD-MM-YYYY
    Stored in DB as ISO: YYYY-MM-DD
    Allows past dates; blocks future dates only.

    Seeds *at least 10* EquipmentTypes if the table has fewer than 10 rows.
    """

    DB_PATH = "SystemDatabase.db"

    def __init__(self, parent, controller=None):
        self.frame = parent
        self.controller = controller

        self.frame.columnconfigure(0, weight=4)
        self.frame.columnconfigure(1, weight=2)
        self.frame.rowconfigure(0, weight=1)

        self.type_display_to_id = {}
        self.type_id_to_display = {}

        self._setup_style()
        self._build_root_panes()

        # Data
        self.seed_equipment_types_minimum(min_count=10)
        self.load_equipment_types_dropdown()
        self.load_equipment_from_db()

    def get_frame(self):
        return self.frame

    # ---------------- Style ---------------- #
    def _setup_style(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.style.configure("Section.TLabelframe", padding=10)
        self.style.configure("Hint.TLabel", font=("Arial", 9))
        self.style.configure("Danger.TButton", foreground="#a00")

    # ---------------- DB helpers ---------------- #
    def _connect(self):
        return sqlite3.connect(self.DB_PATH)

    def seed_equipment_types_minimum(self, min_count=10):
        """
        Ensures EquipmentTypes contains at least `min_count` rows.
        If fewer exist, inserts more (no dedupe needed for MVP).
        """
        seed_rows = [
            ("LifeFitness", "Treadmill", "T5"),
            ("Concept2", "Rower", "Model D"),
            ("HammerStrength", "Leg Press", "HS-LP"),
            ("Technogym", "Elliptical", "Excite 700"),
            ("Precor", "Bike", "RBK 885"),
            ("Rogue", "Power Rack", "RML-390F"),
            ("LifeFitness", "Cable Machine", "Signature Cable"),
            ("Matrix", "Stair Climber", "C50"),
            ("Nautilus", "Smith Machine", "SM-500"),
            ("NordicTrack", "Treadmill", "Commercial 1750"),
            ("Cybex", "Arc Trainer", "770A"),
            ("Bowflex", "Dumbbells", "SelectTech 552"),
        ]

        try:
            conn = self._connect()
            cur = conn.cursor()

            current = cur.execute("SELECT COUNT(*) FROM EquipmentTypes").fetchone()[0]
            if current < min_count:
                needed = min_count - current
                # Insert only as many as needed
                cur.executemany(
                    """
                    INSERT INTO EquipmentTypes (EquipmentManufacturer, EquipmentModel, EquipmentSubModel)
                    VALUES (?, ?, ?)
                    """,
                    seed_rows[:needed],
                )
                conn.commit()

            conn.close()
        except sqlite3.Error as ex:
            showerror("Database Error", f"Failed to seed EquipmentTypes.\n\n{ex}")

    # ---------------- Date helpers ---------------- #
    @staticmethod
    def _parse_ddmmyyyy_to_iso(date_str: str) -> str:
        s = date_str.strip()
        dt = datetime.strptime(s, "%d-%m-%Y").date()
        if dt > date.today():
            raise ValueError("future_date")
        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def _iso_to_ddmmyyyy(iso_str: str) -> str:
        if not iso_str:
            return ""
        try:
            dt = datetime.strptime(iso_str.strip(), "%Y-%m-%d").date()
            return dt.strftime("%d-%m-%Y")
        except ValueError:
            return iso_str

    # ---------------- Build UI ---------------- #
    def _build_root_panes(self):
        root_pad = ttk.Frame(self.frame, padding=8)
        root_pad.grid(row=0, column=0, columnspan=2, sticky="nsew")
        root_pad.columnconfigure(0, weight=4)
        root_pad.columnconfigure(1, weight=2)
        root_pad.rowconfigure(0, weight=1)

        self.table_section = ttk.Labelframe(root_pad, text="Equipment Maintenance Records", style="Section.TLabelframe")
        self.table_section.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.table_section.columnconfigure(0, weight=1)
        self.table_section.rowconfigure(1, weight=1)

        self.form_section = ttk.Labelframe(root_pad, text="Add / Edit Equipment", style="Section.TLabelframe")
        self.form_section.grid(row=0, column=1, sticky="nsew")
        self.form_section.columnconfigure(0, weight=1)

        self._build_table(self.table_section)
        self._build_form(self.form_section)

    def _build_table(self, parent):
        top = ttk.Frame(parent)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top.columnconfigure(0, weight=1)

        ttk.Label(top, text="Click a row to edit →", style="Hint.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(top, text="Refresh", command=self.on_refresh_clicked).grid(row=0, column=1, sticky="e")

        tree_wrap = ttk.Frame(parent)
        tree_wrap.grid(row=1, column=0, sticky="nsew")
        tree_wrap.columnconfigure(0, weight=1)
        tree_wrap.rowconfigure(0, weight=1)

        columns = ("id", "type", "status", "purchase_date")
        self.equipment_table = ttk.Treeview(tree_wrap, columns=columns, show="headings")

        self.equipment_table.heading("id", text="ID")
        self.equipment_table.heading("type", text="Type (Manufacturer Model SubModel)")
        self.equipment_table.heading("status", text="Status")
        self.equipment_table.heading("purchase_date", text="Purchased")

        self.equipment_table.column("id", width=60, anchor="center", stretch=False)
        self.equipment_table.column("type", width=360, anchor="w", stretch=True)
        self.equipment_table.column("status", width=90, anchor="center", stretch=False)
        self.equipment_table.column("purchase_date", width=110, anchor="center", stretch=False)

        yscroll = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.equipment_table.yview)
        self.equipment_table.configure(yscrollcommand=yscroll.set)

        self.equipment_table.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")

        self.equipment_table.bind("<<TreeviewSelect>>", self.on_row_selected)

    def _build_form(self, parent):
        fields = ttk.Frame(parent)
        fields.grid(row=0, column=0, sticky="ew")
        fields.columnconfigure(1, weight=1)

        ttk.Label(fields, text="Selected ID:").grid(row=0, column=0, sticky="w", pady=3)
        self.selected_id_var = tk.StringVar(value="")
        self.selected_id_entry = ttk.Entry(fields, textvariable=self.selected_id_var, state="readonly")
        self.selected_id_entry.grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Label(fields, text="Equipment Type:").grid(row=1, column=0, sticky="w", pady=3)
        self.type_combo = ttk.Combobox(fields, state="readonly")
        self.type_combo.grid(row=1, column=1, sticky="ew", pady=3)

        ttk.Label(fields, text="Status:").grid(row=2, column=0, sticky="w", pady=3)
        self.status_combo = ttk.Combobox(fields, values=["Ok", "Due Soon", "Overdue"], state="readonly")
        self.status_combo.grid(row=2, column=1, sticky="ew", pady=3)
        self.status_combo.set("Ok")

        ttk.Label(fields, text="Purchase Date:").grid(row=3, column=0, sticky="w", pady=3)
        self.purchase_date_entry = ttk.Entry(fields)
        self.purchase_date_entry.grid(row=3, column=1, sticky="ew", pady=3)

        ttk.Label(fields, text="DD-MM-YYYY (past ok; future blocked)", style="Hint.TLabel").grid(
            row=4, column=1, sticky="w", pady=(0, 6)
        )

        btns = ttk.Frame(parent)
        btns.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        ttk.Button(btns, text="Add", command=self.on_add_clicked).grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=4)
        ttk.Button(btns, text="Update", command=self.on_update_clicked).grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=4)
        ttk.Button(btns, text="Delete", command=self.on_delete_clicked, style="Danger.TButton").grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=4)
        ttk.Button(btns, text="Clear", command=self.clear_form).grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=4)

        parent.rowconfigure(2, weight=1)

    # ---------------- Data loading ---------------- #
    def load_equipment_types_dropdown(self):
        try:
            conn = self._connect()
            cur = conn.cursor()

            rows = cur.execute(
                """
                SELECT EquipmentTypeID, EquipmentManufacturer, EquipmentModel, EquipmentSubModel
                FROM EquipmentTypes
                ORDER BY EquipmentTypeID ASC
                """
            ).fetchall()
            conn.close()

            self.type_display_to_id.clear()
            self.type_id_to_display.clear()

            display_values = []
            for type_id, manu, model, sub in rows:
                sub_part = f" ({sub})" if sub else ""
                display = f"{type_id} - {manu} {model}{sub_part}"
                display_values.append(display)
                self.type_display_to_id[display] = int(type_id)
                self.type_id_to_display[int(type_id)] = display

            self.type_combo["values"] = display_values
            if display_values and (self.type_combo.get().strip() == ""):
                self.type_combo.set(display_values[0])

        except sqlite3.Error as ex:
            showerror("Database Error", f"Failed to load EquipmentTypes.\n\n{ex}")

    def load_equipment_from_db(self):
        for item in self.equipment_table.get_children():
            self.equipment_table.delete(item)

        try:
            conn = self._connect()
            cur = conn.cursor()

            rows = cur.execute(
                """
                SELECT
                    e.EquipmentID,
                    e.EquipmentTypeID,
                    et.EquipmentManufacturer,
                    et.EquipmentModel,
                    et.EquipmentSubModel,
                    e.EquipmentStatus,
                    e.PurchaseDate
                FROM Equipment e
                LEFT JOIN EquipmentTypes et ON et.EquipmentTypeID = e.EquipmentTypeID
                ORDER BY e.EquipmentID ASC
                """
            ).fetchall()
            conn.close()

            for equipment_id, type_id, manu, model, sub, status, purchase_iso in rows:
                sub_part = f" ({sub})" if sub else ""
                type_display = (
                    f"{type_id} - {manu} {model}{sub_part}"
                    if (manu or model or sub)
                    else str(type_id)
                )
                purchase_display = self._iso_to_ddmmyyyy(purchase_iso)

                self.equipment_table.insert(
                    "",
                    "end",
                    values=(equipment_id, type_display, status or "", purchase_display),
                )

        except sqlite3.Error as ex:
            showerror("Database Error", f"Failed to load equipment.\n\n{ex}")

    # ---------------- UI helpers ---------------- #
    def on_refresh_clicked(self):
        self.seed_equipment_types_minimum(min_count=10)  # keep ensuring minimum exists
        self.load_equipment_types_dropdown()
        self.load_equipment_from_db()

    def clear_form(self):
        self.selected_id_var.set("")
        self.status_combo.set("Ok")
        self.purchase_date_entry.delete(0, tk.END)

    def _get_selected_type_id(self):
        display = self.type_combo.get().strip()
        if not display:
            return None
        return self.type_display_to_id.get(display)

    def on_row_selected(self, _event=None):
        selected = self.equipment_table.selection()
        if not selected:
            return

        equipment_id, type_display, status, purchase_ddmmyyyy = self.equipment_table.item(selected[0], "values")
        self.selected_id_var.set(str(equipment_id))

        try:
            parsed_id = int(str(type_display).split(" - ")[0])
            if parsed_id in self.type_id_to_display:
                self.type_combo.set(self.type_id_to_display[parsed_id])
        except Exception:
            pass

        self.status_combo.set(status if status else "Ok")
        self.purchase_date_entry.delete(0, tk.END)
        self.purchase_date_entry.insert(0, purchase_ddmmyyyy if purchase_ddmmyyyy else "")

    # ---------------- CRUD actions ---------------- #
    def on_add_clicked(self):
        type_id = self._get_selected_type_id()
        status = self.status_combo.get().strip()
        purchase_input = self.purchase_date_entry.get().strip()

        if type_id is None:
            showerror("Input Error", "Please select an Equipment Type.")
            return
        if not purchase_input:
            showerror("Input Error", "Purchase Date is required (DD-MM-YYYY).")
            return

        try:
            purchase_iso = self._parse_ddmmyyyy_to_iso(purchase_input)
        except ValueError as ve:
            if str(ve) == "future_date":
                showerror("Input Error", "Purchase Date cannot be in the future.")
            else:
                showerror("Input Error", "Purchase Date must be a valid date in DD-MM-YYYY format.")
            return

        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO Equipment (EquipmentTypeID, EquipmentStatus, PurchaseDate)
                VALUES (?, ?, ?)
                """,
                (int(type_id), status, purchase_iso),
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

        type_id = self._get_selected_type_id()
        status = self.status_combo.get().strip()
        purchase_input = self.purchase_date_entry.get().strip()

        if type_id is None:
            showerror("Input Error", "Please select an Equipment Type.")
            return
        if not purchase_input:
            showerror("Input Error", "Purchase Date is required (DD-MM-YYYY).")
            return

        try:
            purchase_iso = self._parse_ddmmyyyy_to_iso(purchase_input)
        except ValueError as ve:
            if str(ve) == "future_date":
                showerror("Input Error", "Purchase Date cannot be in the future.")
            else:
                showerror("Input Error", "Purchase Date must be a valid date in DD-MM-YYYY format.")
            return

        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute(
                """
                UPDATE Equipment
                SET EquipmentTypeID = ?, EquipmentStatus = ?, PurchaseDate = ?
                WHERE EquipmentID = ?
                """,
                (int(type_id), status, purchase_iso, int(equipment_id)),
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
            cur.execute("DELETE FROM Equipment WHERE EquipmentID = ?", (int(equipment_id),))
            conn.commit()
            conn.close()

            self.load_equipment_from_db()
            self.clear_form()
            showinfo("Deleted", "Equipment deleted successfully.")

        except sqlite3.Error as ex:
            showerror("Database Error", f"Failed to delete equipment.\n\n{ex}")
