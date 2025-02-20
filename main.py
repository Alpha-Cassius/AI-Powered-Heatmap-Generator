import os
import customtkinter as ctk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import google.generativeai as genai

# Initialize GUI
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class HeatmapApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Heatmap Generator")
        self.geometry("1500x800+0+0")  # Fullscreen

        # Configure Gemini API
        os.environ['GOOGLE_API_KEY'] = "YOUR_API"  # Replace with your actual API key
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

        # Main Layout
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Left Panel for Inputs
        self.left_panel = ctk.CTkFrame(self.main_frame, width=400)
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)

        # Right Panel for Heatmap
        self.right_panel = ctk.CTkFrame(self.main_frame, width=1200)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Title Label
        self.label_title = ctk.CTkLabel(self.left_panel, text="Select Data Source", font=("Arial", 16))
        self.label_title.pack(pady=10)

        # Data Source Selection
        self.data_source = ctk.StringVar(value="MySQL")  # Set default value to MySQL
        self.combo_source = ctk.CTkComboBox(self.left_panel, values=["CSV", "Excel", "MySQL"], 
                                            variable=self.data_source, 
                                            command=self.update_input_fields)
        self.combo_source.pack(pady=5)

        # Dynamic Input Fields
        self.input_frame = ctk.CTkFrame(self.left_panel)
        self.input_frame.pack(pady=10)

        self.entry_input = ctk.CTkEntry(self.input_frame, width=250)
        self.entry_input.pack(side="left", padx=5)

        self.btn_browse = ctk.CTkButton(self.input_frame, text="Browse", command=self.browse_file)
        self.btn_browse.pack(side="right")

        # MySQL Inputs
        self.mysql_host = ctk.CTkEntry(self.left_panel, placeholder_text="Host (e.g., localhost)")
        self.mysql_user = ctk.CTkEntry(self.left_panel, placeholder_text="Username")
        self.mysql_pass = ctk.CTkEntry(self.left_panel, placeholder_text="Password", show="*")
        self.mysql_db = ctk.CTkEntry(self.left_panel, placeholder_text="Database Name")
        self.mysql_query = ctk.CTkEntry(self.left_panel, placeholder_text="SQL Query")

        # Generate Heatmap Button
        self.btn_generate = ctk.CTkButton(self.left_panel, text="Generate Heatmap", command=self.generate_heatmap)
        self.btn_generate.pack(pady=5)

        # Suggested Heatmap Name
        self.label_suggested_name = ctk.CTkLabel(self.left_panel, text="Suggested Heatmap Name:")
        self.label_suggested_name.pack(pady=5)

        self.entry_suggested_name = ctk.CTkEntry(self.left_panel, width=250)
        self.entry_suggested_name.pack(pady=5)

        # Save Heatmap Button
        self.btn_save = ctk.CTkButton(self.left_panel, text="Save Heatmap", command=self.save_heatmap)
        self.btn_save.pack(pady=5)

        # Analysis Text Box
        self.analysis_text = ctk.CTkTextbox(self.left_panel, width=300, height=250, wrap='word')
        self.analysis_text.pack(pady=10)
        self.analysis_text.insert('1.0', "Enter your analysis or observations here...")

        # Heatmap Frame
        self.heatmap_frame = ctk.CTkFrame(self.right_panel)
        self.heatmap_frame.pack(fill="both", expand=True)

        self.figure = None
        self.canvas = None

        self.update_input_fields()  # Initialize UI elements based on selection

    def update_input_fields(self, event=None):
        """Updates the input fields based on selected data source"""
        for widget in self.input_frame.winfo_children():
            widget.pack_forget()
        self.mysql_host.pack_forget()
        self.mysql_user.pack_forget()
        self.mysql_pass.pack_forget()
        self.mysql_db.pack_forget()
        self.mysql_query.pack_forget()

        source = self.data_source.get()

        if source in ["CSV", "Excel"]:
            self.entry_input.pack(side="left", padx=5)
            self.btn_browse.pack(side="right")
        elif source == "MySQL":
            self.mysql_host.pack(pady=2)
            self.mysql_user.pack(pady=2)
            self.mysql_pass.pack(pady=2)
            self.mysql_db.pack(pady=2)
            self.mysql_query.pack(pady=2)

    def browse_file(self):
        """Opens file dialog to select a file"""
        filetypes = [("CSV files", "*.csv"), ("Excel files", "*.xlsx;*.xls")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        self.entry_input.delete(0, "end")
        self.entry_input.insert(0, file_path)

    def generate_heatmap(self):
        """Loads data and plots heatmap"""
        source = self.data_source.get()

        try:
            if source in ["CSV", "Excel"]:
                file_path = self.entry_input.get()
                if not file_path:
                    messagebox.showerror("Error", "Please select a file")
                    return
                
                if source == "CSV":
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
            
            elif source == "MySQL":
                config = {
                    'host': self.mysql_host.get(),
                    'user': self.mysql_user.get(),
                    'password': self.mysql_pass.get(),
                    'database': self.mysql_db.get()
                }
                query = self.mysql_query.get()
                if not all(config.values()) or not query:
                    messagebox.showerror("Error", "Please fill in all MySQL fields")
                    return
                
                conn = mysql.connector.connect(**config)
                df = pd.read_sql(query, conn)
                conn.close()

            # Keep only numeric columns for heatmap
            df = df.select_dtypes(include=['number'])
            if df.empty:
                messagebox.showerror("Error", "No numerical data available for heatmap")
                return

            # Plot Heatmap
            self.figure, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
            ax.set_title("Heatmap of Correlation Matrix")

            # Generate a name for the heatmap using Gemini API
            self.suggest_heatmap_name(df)

            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(self.figure, master=self.heatmap_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill='both', expand=True)

            # Analyze the heatmap using Gemini API
            self.analyze_heatmap(df)

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"Error: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process data: {e}")

    def suggest_heatmap_name(self, df):
        """Suggests a name for the heatmap using Gemini API"""
        try:
            prompt = f"Suggest a name for a heatmap based on the following correlation matrix:\n{df.corr().to_string()}"
            response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
            suggested_name = response.text.strip()

            # Set the suggested name in the entry
            self.entry_suggested_name.delete(0, "end")
            self.entry_suggested_name.insert(0, suggested_name)

        except Exception as e:
            messagebox.showerror("Name Suggestion Error", f"Failed to suggest heatmap name: {e}")

    def analyze_heatmap(self, df):
        """Analyze the heatmap data using Gemini API and display the response"""
        try:
            # Prepare the data for analysis
            analysis_prompt = f"Analyze the following correlation matrix:\n{df.corr().to_string()}"
            response = genai.GenerativeModel('gemini-pro').generate_content(analysis_prompt)
            analysis_result = response.text

            # Display the analysis result in the analysis_text box
            self.analysis_text.delete('1.0', 'end')  # Clear previous text
            self.analysis_text.insert('1.0', analysis_result)

        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to analyze heatmap: {e}")

    def save_heatmap(self):
        """Saves the heatmap as an image"""
        if self.figure:
            # Open a file dialog to choose the save location and file name
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",  # Default file extension
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                title="Save Heatmap As"
            )
            
            if not file_path:  # If the user cancels the dialog
                return

            self.figure.savefig(file_path)
            messagebox.showinfo("Success", "Heatmap saved successfully!")

if __name__ == "__main__":
    app = HeatmapApp()
    app.mainloop()
