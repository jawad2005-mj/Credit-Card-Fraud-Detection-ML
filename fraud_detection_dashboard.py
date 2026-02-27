import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import os

# --- THEME SETTINGS ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FraudGuardUltimate(ctk.CTk):
    def __init__(self):
        super().__init__()

        # WINDOW SETUP
        self.title("🛡️ FraudGuard AI | Enterprise Suite")
        self.geometry("1400x900")
        
        # Load Model
        self.model = self.load_model()
        self.analyzed_df = None 

        # LAYOUT
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="FRAUD GUARD\nPRO SUITE", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=40)

        self.btn_dash = ctk.CTkButton(self.sidebar, text="📊 Dashboard", height=40, fg_color="transparent", border_width=1, command=lambda: self.show_frame("dashboard"))
        self.btn_dash.pack(pady=5, padx=20, fill="x")

        self.btn_manual = ctk.CTkButton(self.sidebar, text="📝 Manual Check", height=40, fg_color="transparent", border_width=1, command=lambda: self.show_frame("manual"))
        self.btn_manual.pack(pady=5, padx=20, fill="x")

        self.btn_batch = ctk.CTkButton(self.sidebar, text="📂 Batch Scan (Table)", height=40, fg_color="#ea580c", hover_color="#c2410c", command=lambda: self.show_frame("batch"))
        self.btn_batch.pack(pady=20, padx=20, fill="x")

        # --- FRAMES ---
        self.frames = {}
        self.create_dashboard_ui()
        self.create_manual_ui()
        self.create_batch_ui()

        self.show_frame("dashboard")

    def load_model(self):
        files = ['fraud_pipeline.pkl', 'logistic_model_advanced.pkl', 'model.pkl']
        for f in files:
            if os.path.exists(f): return joblib.load(f)
        return None

    def show_frame(self, name):
        for f in self.frames.values(): f.grid_forget()
        self.frames[name].grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    # =====================================================
    # 1. DASHBOARD FRAME
    # =====================================================
    def create_dashboard_ui(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frames["dashboard"] = frame
        
        ctk.CTkLabel(frame, text="Live Analytics Overview", font=("Arial", 26, "bold")).pack(anchor="w", pady=(0, 20))

        # KPI Cards
        kpi_frame = ctk.CTkFrame(frame, fg_color="transparent")
        kpi_frame.pack(fill="x", pady=10)

        self.kpi_total = self.create_card(kpi_frame, "Total Scanned", "0", "#334155")
        self.kpi_fraud = self.create_card(kpi_frame, "THREATS FOUND", "0", "#7f1d1d")
        self.kpi_safe = self.create_card(kpi_frame, "Safe Transactions", "0", "#14532d")

        # Chart Area
        self.graph_container = ctk.CTkFrame(frame, fg_color="#1e1e1e", corner_radius=15)
        self.graph_container.pack(fill="both", expand=True, pady=20)
        
        self.lbl_placeholder = ctk.CTkLabel(self.graph_container, text="Run a Check to see Visuals", text_color="gray")
        self.lbl_placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def create_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=color, height=120)
        card.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(card, text=title, font=("Arial", 14)).pack(pady=(20, 5))
        lbl_val = ctk.CTkLabel(card, text=value, font=("Arial", 32, "bold"))
        lbl_val.pack(pady=(0, 20))
        return lbl_val

    # =====================================================
    # 2. MANUAL CHECK FRAME (UPDATED LOGIC)
    # =====================================================
    def create_manual_ui(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frames["manual"] = frame

        head = ctk.CTkFrame(frame, fg_color="transparent")
        head.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(head, text="Manual Audit", font=("Arial", 24, "bold")).pack(side="left")
        
        # Buttons
        ctk.CTkButton(head, text="✨ Auto-Fill", fg_color="#6366f1", command=self.auto_fill_manual).pack(side="right", padx=5)
        ctk.CTkButton(head, text="🔍 Analyze & Graph", fg_color="#ea580c", command=self.run_manual_prediction).pack(side="right", padx=5)

        scroll = ctk.CTkScrollableFrame(frame, label_text="Features")
        scroll.pack(fill="both", expand=True)

        self.manual_entries = {}
        cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        for col in cols:
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=col, width=60, anchor="w").pack(side="left", padx=10)
            ent = ctk.CTkEntry(row)
            ent.pack(side="right", fill="x", expand=True)
            self.manual_entries[col] = ent

    def auto_fill_manual(self):
        for col, ent in self.manual_entries.items():
            ent.delete(0, 'end')
            if col == 'Time': val = random.randint(0, 150000)
            elif col == 'Amount': val = round(random.uniform(0, 5000), 2)
            else: val = round(random.uniform(-3, 3), 4)
            ent.insert(0, str(val))

    def run_manual_prediction(self):
        # YEH FUNCTION AB DASHBOARD UPDATE KAREGA
        if not self.model: return
        try:
            row_data = []
            for col, ent in self.manual_entries.items():
                val = ent.get()
                if not val: raise ValueError
                row_data.append(float(val))
            
            # 1. Predict
            df = pd.DataFrame([row_data], columns=list(self.manual_entries.keys()))
            pred = self.model.predict(df)[0]
            
            # 2. Calculate Dashboard Stats for this single entry
            if pred == 1:
                fraud_count = 1
                safe_count = 0
                msg = "🚨 FRAUD DETECTED!"
            else:
                fraud_count = 0
                safe_count = 1
                msg = "✅ Transaction Safe"

            # 3. Update Dashboard Cards
            self.kpi_total.configure(text="1")
            self.kpi_fraud.configure(text=str(fraud_count))
            self.kpi_safe.configure(text=str(safe_count))

            # 4. Update Dashboard Graph
            self.render_chart(safe_count, fraud_count)

            # 5. Show Alert and Switch
            messagebox.showinfo("Analysis Complete", f"{msg}\nVisualizing on Dashboard...")
            self.show_frame("dashboard")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    # =====================================================
    # 3. BATCH SCAN (TABLE VIEW)
    # =====================================================
    def create_batch_ui(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.frames["batch"] = frame

        # Header
        head = ctk.CTkFrame(frame, fg_color="transparent")
        head.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(head, text="Batch File Analysis", font=("Arial", 24, "bold")).pack(side="left")
        
        ctk.CTkButton(head, text="📂 Upload CSV", command=self.process_batch).pack(side="right", padx=10)
        ctk.CTkButton(head, text="💾 Export Results", fg_color="#059669", command=self.export_results).pack(side="right", padx=10)

        # TABLE
        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=25)
        style.map("Treeview", background=[("selected", "#4f46e5")])

        columns = ("ID", "Time", "Amount", "STATUS", "Risk Level")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.tag_configure("fraud", background="#7f1d1d", foreground="white")
        self.tree.tag_configure("safe", background="#14532d", foreground="white")

    def process_batch(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path: return

        try:
            df = pd.read_csv(path)
            req_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
            if 'Class' in df.columns: df = df.drop(columns=['Class'])
            
            if len(df.columns) == 30: df.columns = req_cols
            elif 'scaled_time' in df.columns:
                 df.rename(columns={'scaled_time': 'Time', 'scaled_amount': 'Amount'}, inplace=True)
                 df = df[req_cols]

            preds = self.model.predict(df)
            df['Prediction'] = preds
            self.analyzed_df = df

            frauds = sum(preds)
            total = len(preds)
            safe = total - frauds

            # Update Dashboard
            self.kpi_total.configure(text=f"{total:,}")
            self.kpi_fraud.configure(text=f"{frauds:,}")
            self.kpi_safe.configure(text=f"{safe:,}")
            self.render_chart(safe, frauds)

            # Populate Table
            for item in self.tree.get_children(): self.tree.delete(item)
            for index, row in df.head(500).iterrows():
                status = "FRAUD" if row['Prediction'] == 1 else "Safe"
                tag = "fraud" if row['Prediction'] == 1 else "safe"
                risk = "CRITICAL" if row['Prediction'] == 1 else "Low"
                self.tree.insert("", "end", values=(index, row['Time'], row['Amount'], status, risk), tags=(tag,))

            messagebox.showinfo("Analysis Complete", f"Found {frauds} Threats!\nCheck Dashboard for Graph.")
            self.show_frame("dashboard")

        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

    def export_results(self):
        if self.analyzed_df is None: return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path: self.analyzed_df.to_csv(path, index=False)

    # =====================================================
    # CHART RENDERER (Common for both Manual & Batch)
    # =====================================================
    def render_chart(self, safe, fraud):
        # Clear old chart
        for widget in self.graph_container.winfo_children(): widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor('#1e1e1e')
        ax.set_facecolor('#1e1e1e')

        labels = ['Safe', 'Fraud']
        sizes = [safe, fraud]
        colors = ['#22c55e', '#ef4444']

        # Logic to handle 100% single color (Manual Check case)
        if safe == 0 and fraud > 0: explode = (0, 0) # Full Red
        elif fraud == 0 and safe > 0: explode = (0, 0) # Full Green
        else: explode = (0, 0.1)

        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                          startangle=90, colors=colors, pctdistance=0.85,
                                          textprops=dict(color="white", weight="bold"))
        
        centre_circle = plt.Circle((0,0),0.70,fc='#1e1e1e')
        fig.gca().add_artist(centre_circle)
        
        title_text = "Single Transaction Analysis" if (safe+fraud)==1 else "Batch Distribution Analysis"
        ax.set_title(title_text, color="white", fontsize=14, pad=20)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both", padx=20, pady=20)

if __name__ == "__main__":
    app = FraudGuardUltimate()
    app.mainloop()