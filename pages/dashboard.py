import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Configuration Colors & Fonts ---
COLOR_BG_MAIN = "#FFFFFF"
COLOR_CARD_BG = "#FFFFFF"
FONT_SUBHEADER = ("Arial", 12, "bold")
FONT_BODY = ("Arial", 10)
FONT_KPI_NUM = ("Arial", 24, "bold")

class FitLifeDashboard(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        
        self.place(relwidth=1, relheight=1)
        
        self.configure(bg=COLOR_BG_MAIN)
        
        # --- LAYOUT GRID ---
        
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1)    
        self.grid_rowconfigure(2, weight=1)    

        # --- Build Sections ---
        self.build_kpi_row()
        self.build_middle_section()
        self.build_bottom_section()

    def build_kpi_row(self):
        # Row 0: KPI Cards
        
        kpi_container = tk.Frame(self, bg=COLOR_BG_MAIN)
        kpi_container.grid(row=0, column=0, sticky="ew", pady=(10, 5), padx=10)

        kpis = [
            ("1250", "Active Members"),
            ("18", "Today's Classes"),
            ("24", "Upcoming Renewals"),
            ("5", "Overdue Payments")
        ]

        for i, (num, label) in enumerate(kpis):
            card = tk.Frame(kpi_container, bg=COLOR_CARD_BG, highlightbackground="black", highlightthickness=2)
            card.grid(row=0, column=i, padx=5, sticky="ew")
            
            kpi_container.grid_columnconfigure(i, weight=1)

            tk.Label(card, text=num, font=FONT_KPI_NUM, bg=COLOR_CARD_BG).pack(pady=(10, 0))
            tk.Label(card, text=label, font=FONT_BODY, bg=COLOR_CARD_BG).pack(pady=(0, 10))

    def build_middle_section(self):
        # Row 1: Graph and Invoices
       
        middle_container = tk.Frame(self, bg=COLOR_BG_MAIN)
        middle_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # 3 parts graph, 1 part invoices
        middle_container.grid_columnconfigure(0, weight=3) 
        middle_container.grid_columnconfigure(1, weight=1) 
        middle_container.grid_rowconfigure(0, weight=1)

        # --- Graph Section (Left) ---
        graph_frame = tk.Frame(middle_container, bg=COLOR_BG_MAIN)
        graph_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.create_matplotlib_graph(graph_frame)

        # --- Outstanding Invoices (Right) ---
        invoices_frame = tk.Frame(middle_container, bg="#D3D3D3", padx=10, pady=10)
        invoices_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(invoices_frame, text="Outstanding Invoices", font=FONT_SUBHEADER, bg="#D3D3D3").pack(anchor="w", pady=(0, 5))

        for i in range(5):
            item_frame = tk.Frame(invoices_frame, bg="#D3D3D3", pady=3)
            item_frame.pack(fill="x", pady=1)
            inner = tk.Frame(item_frame, bg=COLOR_CARD_BG, highlightthickness=1, highlightbackground="red")
            inner.pack(fill="x", ipady=3) 
            tk.Label(inner, text="Invoice Title", font=("Arial", 9, "bold"), bg=COLOR_CARD_BG).pack(side="left", padx=5)
            tk.Label(inner, text="£00.00", font=("Arial", 9), bg=COLOR_CARD_BG).pack(side="right", padx=5)

    def create_matplotlib_graph(self, parent):
        
        fig = Figure(figsize=(5, 3), dpi=100) 
        ax = fig.add_subplot(111)

        hours = [8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]
        x_labels = ["1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 AM", "10 AM", "11 AM", "12 PM"]
        values = [9, 11, 7, 7, 12, 18, 14, 15, 18, 20, 14, 10]
        
        if len(hours) != len(values): hours = range(len(values))

        ax.plot(hours[:len(values)], values, marker='.', color="#4A90E2", linewidth=2)
        
        ax.set_ylabel("No. of buses passing") 
        ax.set_xticks(hours[:len(values)])
        ax.set_xticklabels(x_labels, fontsize=8) 
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        fig.tight_layout(pad=1)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def build_bottom_section(self):
        # Row 2: Bottom Tables
        
        bottom_container = tk.Frame(self, bg=COLOR_BG_MAIN)
        bottom_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        bottom_container.grid_columnconfigure(0, weight=1)
        bottom_container.grid_columnconfigure(1, weight=1)
        bottom_container.grid_rowconfigure(0, weight=1) # Ensure panels fill height

        self.create_table_panel(bottom_container, 0, "Overdue Payments", 
                                ["Ashley", "Musa", "Ryan", "Tom"], 
                                ["23/04/2026", "02/09/2026", "07/12/2026", "13/01/2026"],
                                ["£45", "£160", "£160", "£45"], "Renew")

        self.create_table_panel(bottom_container, 1, "Pending Refunds",
                                ["Ashley", "Ashley", "Ashley", "Ashley"],
                                ["15/04/2026", "29/07/2026", "31/09/2026", "18/05/2026"],
                                ["£45", "£12", "£12", "£45"], "Approve")

    def create_table_panel(self, parent, col, title, names, dates, amounts, btn_text):
        panel = tk.Frame(parent, bg=COLOR_BG_MAIN, highlightbackground="black", highlightthickness=1)
        panel.grid(row=0, column=col, sticky="nsew", padx=5) 
        
        header_row = tk.Frame(panel, bg=COLOR_BG_MAIN)
        header_row.pack(fill="x", padx=10, pady=5)
        
        tk.Label(header_row, text=title, font=FONT_SUBHEADER, bg=COLOR_BG_MAIN).pack(side="left")
        
        search_frame = tk.Frame(panel, bg=COLOR_BG_MAIN)
        search_frame.pack(fill="x", padx=10, pady=5)
        entry = tk.Entry(search_frame, bg="#F0F0F0")
        entry.pack(side="left", fill="x", expand=True)
        entry.insert(0, " Search...")
        
        tk.Label(search_frame, text="Date/Client ▼", bg="#F0F0F0", relief="solid", bd=1).pack(side="right", padx=5)

        for n, d, a in zip(names, dates, amounts):
            row = tk.Frame(panel, bg="white", highlightbackground="black", highlightthickness=1)
            row.pack(fill="x", padx=10, pady=2)
            
            tk.Label(row, text=n, font=("Arial", 10, "bold"), bg="white", width=10, anchor="w").pack(side="left", padx=5)
            tk.Label(row, text=d, font=("Arial", 9), bg="white").pack(side="left", padx=5)
            
            btn = tk.Button(row, text=btn_text, font=("Arial", 8), bg="#E0E0E0")
            btn.pack(side="right", padx=5, pady=2)
            
            tk.Label(row, text=a, font=("Arial", 10, "bold"), bg="white").pack(side="right", padx=10)