import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import io
import threading
import pandas as pd
import re
import os
import google.generativeai as genai


API_KEY = 'your api key here'

class PrescriptionProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prescription Processing System")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        # Initialize variables
        self.image_path = None
        self.image_display = None
        self.medicine_data = None
        self.prescribed_meds = []
        self.final_meds = []
        self.api_key = API_KEY
        # Load medicine database
        self.load_database()

        # Configure API
        self.configure_api()

        # Create UI elements
        self.create_ui()

    def load_database(self):
        try:
            self.medicine_data = pd.read_csv('medicine_database.csv')
            self.medicine_names = self.medicine_data['name'].tolist()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load medicine database: {str(e)}")
            self.root.quit()

    def configure_api(self):
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to configure API: {str(e)}")

    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Prescription Processing System", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)  # Store notebook as instance variable
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Upload tab
        upload_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(upload_frame, text="Upload Prescription")

        # Results tab
        results_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(results_frame, text="Results")

        # Setup Upload tab
        self.setup_upload_tab(upload_frame)

        # Setup Results tab
        self.setup_results_tab(results_frame)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to process prescription")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_upload_tab(self, parent):
        # Left side - Controls
        left_frame = ttk.Frame(parent)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Instructions
        instruction_label = ttk.Label(left_frame, text="Upload a prescription image to process",
                                      font=("Arial", 12))
        instruction_label.pack(pady=20)

        # Upload button
        upload_button = ttk.Button(left_frame, text="Select Image", command=self.select_image)
        upload_button.pack(pady=10)

        self.filename_var = tk.StringVar()
        filename_label = ttk.Label(left_frame, textvariable=self.filename_var)
        filename_label.pack(pady=5)

        # Process button
        self.process_button = ttk.Button(left_frame, text="Process Prescription",
                                         command=self.process_prescription, state=tk.DISABLED)
        self.process_button.pack(pady=20)

        # Progress indicator
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(left_frame, orient=tk.HORIZONTAL,
                                        length=200, mode='indeterminate',
                                        variable=self.progress_var)
        self.progress.pack(pady=10)

        # Right side - Image preview
        right_frame = ttk.LabelFrame(parent, text="Prescription Image")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.image_label = ttk.Label(right_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def setup_results_tab(self, parent):
        # Top frame for detected medications
        top_frame = ttk.LabelFrame(parent, text="Detected Medications")
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create treeview for medications
        self.med_tree = ttk.Treeview(top_frame, columns=("Medicine", "Available", "Suggested Alternative"),
                                     show="headings")
        self.med_tree.heading("Medicine", text="Medicine")
        self.med_tree.heading("Available", text="Available")
        self.med_tree.heading("Suggested Alternative", text="Suggested Alternative")
        self.med_tree.column("Medicine", width=150)
        self.med_tree.column("Available", width=100)
        self.med_tree.column("Suggested Alternative", width=200)
        self.med_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(top_frame, orient=tk.VERTICAL, command=self.med_tree.yview)
        self.med_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom frame for final order details
        bottom_frame = ttk.LabelFrame(parent, text="Final Order")
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create treeview for final order
        self.order_tree = ttk.Treeview(bottom_frame,
                                       columns=("Medicine", "Price", "Frequency", "Special Instructions"),
                                       show="headings")
        self.order_tree.heading("Medicine", text="Medicine")
        self.order_tree.heading("Price", text="Price")
        self.order_tree.heading("Frequency", text="Frequency")
        self.order_tree.heading("Special Instructions", text="Special Instructions")
        self.order_tree.column("Medicine", width=150)
        self.order_tree.column("Price", width=70)
        self.order_tree.column("Frequency", width=150)
        self.order_tree.column("Special Instructions", width=200)
        self.order_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add scrollbar
        order_scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=self.order_tree.yview)
        self.order_tree.configure(yscroll=order_scrollbar.set)
        order_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=10)

        # Total price label
        self.total_price_var = tk.StringVar()
        self.total_price_var.set("Total Price: ₹0")
        total_price_label = ttk.Label(buttons_frame, textvariable=self.total_price_var, font=("Arial", 12, "bold"))
        total_price_label.pack(side=tk.LEFT, padx=10)

        # Show Total button
        show_total_button = ttk.Button(buttons_frame, text="Show Total", command=self.show_total_popup)
        show_total_button.pack(side=tk.LEFT, padx=10)

        # Save order button
        save_button = ttk.Button(buttons_frame, text="Save Order", command=self.save_order)
        save_button.pack(side=tk.RIGHT, padx=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )

        if self.image_path:
            self.filename_var.set(os.path.basename(self.image_path))
            self.process_button.config(state=tk.NORMAL)
            self.display_image()
        else:
            self.filename_var.set("")
            self.process_button.config(state=tk.DISABLED)

    def display_image(self):
        try:
            # Load and resize image for display
            image = Image.open(self.image_path)
            image = self.resize_image(image, 400)

            # Convert to PhotoImage
            self.image_display = ImageTk.PhotoImage(image)

            # Update label
            self.image_label.config(image=self.image_display)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image: {str(e)}")

    def resize_image(self, image, max_size):
        # Resize image while maintaining aspect ratio
        width, height = image.size

        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        return image.resize((new_width, new_height), Image.LANCZOS)

    def process_prescription(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first")
            return

        # Clear previous results
        self.prescribed_meds = []
        self.final_meds = []

        for item in self.med_tree.get_children():
            self.med_tree.delete(item)

        for item in self.order_tree.get_children():
            self.order_tree.delete(item)

        # Start progress bar
        self.progress.start()
        self.status_var.set("Processing prescription...")
        self.process_button.config(state=tk.DISABLED)

        # Run processing in a separate thread to avoid UI freezing
        threading.Thread(target=self.process_in_background).start()

    def process_in_background(self):
        try:
            # Read and process prescription
            self.prescribed_meds = self.read_prescription()

            # Check availability and suggest alternates
            self.check_availability()

            # Calculate total price
            total_price = self.calculate_total_price()

            # Update UI in the main thread
            self.root.after(0, self.update_results_ui, total_price)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Processing failed: {str(e)}"))
        finally:
            # Stop progress bar
            self.root.after(0, self.stop_progress)

    def read_prescription(self):
        try:
            # Load image
            image = Image.open(self.image_path)

            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()

            model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

            # Generate response
            response = model.generate_content([
                {
                    "text": "You are an AI-powered Pharmacist Assistant. Your job is to accurately read handwritten prescriptions, verify medicine names, suggest possible corrections for unclear handwriting, and generate structured medicine orders. Always prioritize accuracy and ensure patient safety. If a medicine name is unclear, suggest possible alternatives. Use a structured format for responses: Name of patient, Medicine Name, Dosage, Frequency, and Special Instructions. Be polite and professional, following pharmacy best practices. Be concise. Don't give disclaimers"},
                {"mime_type": "image/png", "data": img_bytes}
            ])

            # Extract medicine names using regex
            medicine_names = re.findall(r"\*\*\s*Medicine Name:\s*\*\*(.*?)\n", response.text)

            # Strip any extra spaces
            medicine_names = [name.strip() for name in medicine_names]

            return medicine_names

        except Exception as e:
            raise Exception(f"Failed to process prescription: {str(e)}")

    def suggest_alternate(self, medicine):
        try:
            model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

            # Generate alternatives
            alternate = model.generate_content([
                {
                    "text": f"Output should be of 3 word Suggest me 3 alternate for {medicine} in this format: alternate1, alterate2, alternate3"}
            ])

            # Split the response
            list_of_alternates = alternate.text.split(", ")
            cleaned_list = [item.replace('"', '') for item in list_of_alternates]

            # Check if alternatives are available in database
            for name in cleaned_list:
                if name in self.medicine_names:
                    return name

            return None

        except Exception as e:
            print(f"Error suggesting alternate: {str(e)}")
            return None

    def check_availability(self):
        for medicine in self.prescribed_meds:
            if medicine in self.medicine_names:
                self.med_tree.insert("", tk.END, values=(medicine, "Yes", ""))
                self.final_meds.append(medicine)
            else:
                alternate = self.suggest_alternate(medicine)
                self.med_tree.insert("", tk.END,
                                     values=(medicine, "No", alternate if alternate else "No alternative found"))
                if alternate:
                    self.final_meds.append(alternate)

    def calculate_total_price(self):
        total = 0

        for medicine in self.final_meds:
            row = self.medicine_data[self.medicine_data["name"] == medicine]
            if not row.empty:
                price = int(row['price'].iloc[0])
                frequency = row['frequency'].iloc[0]
                special_instructions = row['special instructions'].iloc[0]

                # Add to order treeview
                self.order_tree.insert("", tk.END, values=(medicine, f"₹{price}", frequency, special_instructions))

                total += price

        return total

    def update_results_ui(self, total_price):
        # Update total price
        self.total_price_var.set(f"Total Price: ₹{total_price}")
        self.total_price = total_price


        self.notebook.select(1)

        # Show total popup
        self.root.after(500, self.show_total_popup)

    def show_total_popup(self):
        if hasattr(self, 'total_price'):
            # Create custom popup
            popup = tk.Toplevel(self.root)
            popup.title("Order Total")
            popup.geometry("300x200")
            popup.transient(self.root)  # Make it a transient window (always on top of parent)
            popup.grab_set()  # Modal window

            # Add some padding
            frame = ttk.Frame(popup, padding=20)
            frame.pack(fill=tk.BOTH, expand=True)

            # Add icon or image (placeholder)
            icon_label = ttk.Label(frame, text="💊", font=("Arial", 36))
            icon_label.pack(pady=10)

            # Add total amount
            amount_label = ttk.Label(frame, text=f"Total Amount", font=("Arial", 12))
            amount_label.pack()

            total_label = ttk.Label(frame, text=f"₹{self.total_price}", font=("Arial", 18, "bold"))
            total_label.pack(pady=10)

            # Add close button
            close_button = ttk.Button(frame, text="Close", command=popup.destroy)
            close_button.pack(pady=10)

            # Center the popup on the parent window
            popup.update_idletasks()
            width = popup.winfo_width()
            height = popup.winfo_height()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
            popup.geometry(f"+{x}+{y}")
        else:
            messagebox.showinfo("No Data", "Please process a prescription first")

    def stop_progress(self):
        self.progress.stop()
        self.status_var.set("Processing complete")
        self.process_button.config(state=tk.NORMAL)

    def save_order(self):
        if not self.final_meds:
            messagebox.showerror("Error", "No medications to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("PRESCRIPTION ORDER\n")
                    f.write("=================\n\n")

                    for item_id in self.order_tree.get_children():
                        values = self.order_tree.item(item_id)['values']
                        f.write(f"Medicine: {values[0]}\n")
                        f.write(f"Price: {values[1]}\n")
                        f.write(f"Frequency: {values[2]}\n")
                        f.write(f"Special Instructions: {values[3]}\n")
                        f.write("-----------------\n")

                    f.write(f"\n{self.total_price_var.get()}")

                messagebox.showinfo("Success", "Order saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save order: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PrescriptionProcessingApp(root)
    root.mainloop()