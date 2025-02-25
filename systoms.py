import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from datetime import datetime
import math


class DiagnosisAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Symptom Diagnosis Assistant")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Load medical data
        self.medical_data = self.load_medical_data()
        self.all_symptoms = self.get_all_symptoms()
        self.symptom_categories = self.categorize_symptoms()

        # Tracking user interactions for better diagnosis
        self.user_history = []

        self.create_ui()

    def load_medical_data(self):
        # This is sample data - in a real application, you'd use a comprehensive medical database
        return {
            "Common Cold": {
                "symptoms": {
                    "runny nose": {"weight": 0.8, "key": True},
                    "sneezing": {"weight": 0.7, "key": False},
                    "cough": {"weight": 0.6, "key": False},
                    "sore throat": {"weight": 0.6, "key": False},
                    "mild fever": {"weight": 0.4, "key": False},
                    "nasal congestion": {"weight": 0.8, "key": True}
                },
                "description": "A viral infection of the upper respiratory tract.",
                "recommendations": "Rest, stay hydrated, and take over-the-counter cold medications if needed.",
                "incubation_period": "1-3 days",
                "typical_duration": "7-10 days",
                "risk_factors": ["weakened immune system", "seasonal changes", "exposure to infected individuals"],
                "differential_diagnosis": ["Influenza", "Allergic Rhinitis", "Sinusitis"]
            },
            "Influenza": {
                "symptoms": {
                    "high fever": {"weight": 0.9, "key": True},
                    "body aches": {"weight": 0.8, "key": True},
                    "fatigue": {"weight": 0.7, "key": True},
                    "headache": {"weight": 0.6, "key": False},
                    "dry cough": {"weight": 0.7, "key": False},
                    "sore throat": {"weight": 0.5, "key": False},
                    "runny nose": {"weight": 0.3, "key": False},
                    "sudden onset": {"weight": 0.8, "key": True}
                },
                "description": "A viral infection that attacks your respiratory system.",
                "recommendations": "Rest, stay hydrated, take antiviral medications if prescribed, and consult a doctor if symptoms are severe.",
                "incubation_period": "1-4 days",
                "typical_duration": "1-2 weeks",
                "risk_factors": ["age (very young or elderly)", "weakened immune system", "chronic conditions",
                                 "pregnancy"],
                "differential_diagnosis": ["Common Cold", "Pneumonia", "COVID-19"]
            },
            "Migraine": {
                "symptoms": {
                    "severe headache": {"weight": 0.9, "key": True},
                    "sensitivity to light": {"weight": 0.8, "key": True},
                    "sensitivity to sound": {"weight": 0.7, "key": False},
                    "nausea": {"weight": 0.7, "key": False},
                    "vomiting": {"weight": 0.6, "key": False},
                    "visual aura": {"weight": 0.8, "key": False},
                    "throbbing pain": {"weight": 0.8, "key": True},
                    "pain on one side of head": {"weight": 0.7, "key": False}
                },
                "description": "A headache of varying intensity, often accompanied by nausea and sensitivity to light and sound.",
                "recommendations": "Rest in a dark, quiet room, take prescribed migraine medication, apply cold compresses.",
                "incubation_period": "Hours (with aura)",
                "typical_duration": "4-72 hours",
                "risk_factors": ["family history", "hormonal changes", "stress", "certain foods", "sleep changes"],
                "differential_diagnosis": ["Tension Headache", "Cluster Headache", "Sinus Headache"]
            },
            "Food Poisoning": {
                "symptoms": {
                    "nausea": {"weight": 0.8, "key": True},
                    "vomiting": {"weight": 0.8, "key": True},
                    "diarrhea": {"weight": 0.9, "key": True},
                    "abdominal pain": {"weight": 0.7, "key": False},
                    "fever": {"weight": 0.5, "key": False},
                    "sudden onset": {"weight": 0.8, "key": True},
                    "dehydration": {"weight": 0.6, "key": False}
                },
                "description": "Illness caused by eating contaminated food.",
                "recommendations": "Stay hydrated, rest, eat bland foods when possible, and seek medical attention if symptoms persist or are severe.",
                "incubation_period": "30 minutes to 8 hours (typical)",
                "typical_duration": "1-10 days depending on cause",
                "risk_factors": ["eating undercooked foods", "poor food handling", "cross-contamination"],
                "differential_diagnosis": ["Gastroenteritis", "Irritable Bowel Syndrome", "Appendicitis"]
            },
            "Allergic Reaction": {
                "symptoms": {
                    "itching": {"weight": 0.8, "key": True},
                    "rash": {"weight": 0.8, "key": True},
                    "swelling": {"weight": 0.7, "key": False},
                    "sneezing": {"weight": 0.5, "key": False},
                    "runny nose": {"weight": 0.5, "key": False},
                    "watery eyes": {"weight": 0.6, "key": False},
                    "difficulty breathing": {"weight": 0.9, "key": False},
                    "rapid onset": {"weight": 0.7, "key": True}
                },
                "description": "An immune system response to a substance that the body mistakenly identifies as harmful.",
                "recommendations": "Avoid allergens, take antihistamines, and seek emergency help for severe reactions or difficulty breathing.",
                "incubation_period": "Minutes to hours",
                "typical_duration": "Hours to days",
                "risk_factors": ["previous allergies", "family history", "certain medical conditions"],
                "differential_diagnosis": ["Eczema", "Contact Dermatitis", "Asthma"]
            },
            "Gastroenteritis": {
                "symptoms": {
                    "diarrhea": {"weight": 0.9, "key": True},
                    "nausea": {"weight": 0.7, "key": False},
                    "vomiting": {"weight": 0.8, "key": True},
                    "abdominal cramps": {"weight": 0.8, "key": True},
                    "low-grade fever": {"weight": 0.5, "key": False},
                    "muscle aches": {"weight": 0.4, "key": False},
                    "headache": {"weight": 0.3, "key": False}
                },
                "description": "Inflammation of the lining of the stomach and intestines.",
                "recommendations": "Stay hydrated, rest, follow the BRAT diet (bananas, rice, applesauce, toast), and seek medical care if symptoms are severe or persistent.",
                "incubation_period": "1-3 days",
                "typical_duration": "1-10 days",
                "risk_factors": ["contaminated food or water", "contact with infected individuals", "poor hygiene"],
                "differential_diagnosis": ["Food Poisoning", "Irritable Bowel Syndrome", "Inflammatory Bowel Disease"]
            },
            "Tension Headache": {
                "symptoms": {
                    "dull headache": {"weight": 0.9, "key": True},
                    "pressure around head": {"weight": 0.8, "key": True},
                    "tender scalp": {"weight": 0.6, "key": False},
                    "neck pain": {"weight": 0.7, "key": False},
                    "shoulder pain": {"weight": 0.5, "key": False},
                    "stress": {"weight": 0.7, "key": True}
                },
                "description": "The most common type of headache, often described as a feeling of pressure or tightness.",
                "recommendations": "Rest, over-the-counter pain relievers, stress management techniques, massage, adequate sleep, and staying hydrated.",
                "incubation_period": "Gradual onset",
                "typical_duration": "30 minutes to 7 days",
                "risk_factors": ["stress", "poor posture", "eye strain", "fatigue", "dehydration"],
                "differential_diagnosis": ["Migraine", "Sinus Headache", "Cervicogenic Headache"]
            },
            "Bronchitis": {
                "symptoms": {
                    "cough with mucus": {"weight": 0.9, "key": True},
                    "chest discomfort": {"weight": 0.7, "key": True},
                    "fatigue": {"weight": 0.5, "key": False},
                    "mild fever": {"weight": 0.4, "key": False},
                    "shortness of breath": {"weight": 0.6, "key": False},
                    "wheezing": {"weight": 0.7, "key": False},
                    "sore throat": {"weight": 0.3, "key": False}
                },
                "description": "Inflammation of the lining of the bronchial tubes.",
                "recommendations": "Rest, increased fluid intake, humidifier use, and possibly antibiotics if bacterial in origin.",
                "incubation_period": "4-6 days (for infectious types)",
                "typical_duration": "Acute: 1-3 weeks, Chronic: ongoing",
                "risk_factors": ["smoking", "respiratory infections", "exposure to irritants",
                                 "weakened immune system"],
                "differential_diagnosis": ["Pneumonia", "Asthma", "COPD"]
            },
            "Sinusitis": {
                "symptoms": {
                    "facial pain": {"weight": 0.9, "key": True},
                    "nasal congestion": {"weight": 0.8, "key": True},
                    "thick nasal discharge": {"weight": 0.8, "key": True},
                    "reduced sense of smell": {"weight": 0.6, "key": False},
                    "cough": {"weight": 0.4, "key": False},
                    "fatigue": {"weight": 0.4, "key": False},
                    "ear pressure": {"weight": 0.5, "key": False},
                    "headache": {"weight": 0.7, "key": False}
                },
                "description": "Inflammation of the sinuses, typically due to infection or allergies.",
                "recommendations": "Nasal saline rinses, decongestants, pain relievers, antibiotics if bacterial, and staying hydrated.",
                "incubation_period": "Variable",
                "typical_duration": "Acute: 2-4 weeks, Chronic: 12+ weeks",
                "risk_factors": ["prior respiratory infections", "nasal polyps", "deviated septum", "allergies",
                                 "smoking"],
                "differential_diagnosis": ["Common Cold", "Allergic Rhinitis", "Dental Problems"]
            },
            "COVID-19": {
                "symptoms": {
                    "fever": {"weight": 0.8, "key": True},
                    "dry cough": {"weight": 0.8, "key": True},
                    "fatigue": {"weight": 0.7, "key": False},
                    "shortness of breath": {"weight": 0.8, "key": True},
                    "loss of taste or smell": {"weight": 0.9, "key": True},
                    "sore throat": {"weight": 0.5, "key": False},
                    "headache": {"weight": 0.5, "key": False},
                    "body aches": {"weight": 0.6, "key": False},
                    "diarrhea": {"weight": 0.4, "key": False}
                },
                "description": "A respiratory illness caused by the SARS-CoV-2 virus.",
                "recommendations": "Isolate, rest, stay hydrated, monitor symptoms, and seek medical attention if symptoms worsen. Follow current public health guidelines.",
                "incubation_period": "2-14 days",
                "typical_duration": "2-6 weeks for mild to moderate cases",
                "risk_factors": ["close contact with infected individuals", "crowded settings", "age",
                                 "underlying medical conditions"],
                "differential_diagnosis": ["Influenza", "Common Cold", "Allergies", "Pneumonia"]
            },
            "Appendicitis": {
                "symptoms": {
                    "abdominal pain starting near navel": {"weight": 0.8, "key": True},
                    "pain moving to lower right abdomen": {"weight": 0.9, "key": True},
                    "nausea": {"weight": 0.6, "key": False},
                    "vomiting": {"weight": 0.6, "key": False},
                    "loss of appetite": {"weight": 0.5, "key": False},
                    "low-grade fever": {"weight": 0.4, "key": False},
                    "abdominal swelling": {"weight": 0.7, "key": False}
                },
                "description": "Inflammation of the appendix that can cause severe pain.",
                "recommendations": "Seek immediate medical attention. Surgery (appendectomy) is typically required.",
                "incubation_period": "Rapid onset",
                "typical_duration": "Requires medical intervention",
                "risk_factors": ["age (teens and 20s)", "family history"],
                "differential_diagnosis": ["Gastroenteritis", "Urinary Tract Infection", "Inflammatory Bowel Disease"]
            }
        }

    def get_all_symptoms(self):
        all_symptoms = set()
        for condition in self.medical_data.values():
            for symptom in condition["symptoms"].keys():
                all_symptoms.add(symptom)
        return sorted(list(all_symptoms))

    def categorize_symptoms(self):
        categories = {
            "Respiratory": ["cough", "runny nose", "sneezing", "shortness of breath", "sore throat", "nasal congestion",
                            "dry cough", "cough with mucus", "wheezing", "thick nasal discharge"],
            "Digestive": ["nausea", "vomiting", "diarrhea", "abdominal pain", "loss of appetite", "abdominal cramps"],
            "Head/Neurological": ["headache", "severe headache", "dull headache", "pressure around head",
                                  "sensitivity to light", "sensitivity to sound", "visual aura",
                                  "pain on one side of head", "reduced sense of smell", "loss of taste or smell"],
            "Skin": ["rash", "itching", "swelling"],
            "General": ["fever", "high fever", "mild fever", "low-grade fever", "fatigue", "body aches", "sudden onset",
                        "rapid onset"]
        }

        # Create a lookup dictionary for faster symptom categorization
        symptom_categories = {}
        for category, symptoms in categories.items():
            for symptom in symptoms:
                symptom_categories[symptom] = category

        return symptom_categories

    def create_ui(self):

        style = ttk.Style()
        style.theme_use('clam')


        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', background='#4a7abc', font=('Arial', 10, 'bold'))
        style.configure('Accent.TButton', background='#2a5a8c', foreground='white')
        style.configure('TLabelframe', background='#f0f0f0')
        style.configure('TLabelframe.Label', background='#f0f0f0', font=('Arial', 10, 'bold'))

        # Create a main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Advanced Medical Symptom Diagnosis Assistant",
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Disclaimer
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Symptoms tab
        symptoms_tab = ttk.Frame(notebook, padding=10)
        notebook.add(symptoms_tab, text="Symptoms")

        # Results tab
        results_tab = ttk.Frame(notebook, padding=10)
        notebook.add(results_tab, text="Diagnosis Results")

        # Patient info tab
        info_tab = ttk.Frame(notebook, padding=10)
        notebook.add(info_tab, text="Patient Information")

        # Help tab
        help_tab = ttk.Frame(notebook, padding=10)
        notebook.add(help_tab, text="Help & Info")

        # ---- Symptoms Tab ----
        # Info section
        info_frame = ttk.LabelFrame(symptoms_tab, text="Instructions", padding="10")
        info_frame.pack(fill=tk.X, pady=10)

        info_text = "Enter your symptoms below, rate their severity, and provide onset information for a more accurate diagnosis."
        ttk.Label(info_frame, text=info_text, wraplength=800).pack()

        # Create left and right panels for symptoms tab
        symptoms_panel = ttk.PanedWindow(symptoms_tab, orient=tk.HORIZONTAL)
        symptoms_panel.pack(fill=tk.BOTH, expand=True, pady=10)

        left_frame = ttk.Frame(symptoms_panel, padding=5)
        right_frame = ttk.Frame(symptoms_panel, padding=5)

        symptoms_panel.add(left_frame, weight=1)
        symptoms_panel.add(right_frame, weight=1)

        # Symptom selection (left frame)
        symptom_select_frame = ttk.LabelFrame(left_frame, text="Symptom Selection", padding="10")
        symptom_select_frame.pack(fill=tk.BOTH, expand=True)

        # Symptom entry with autocomplete
        symptom_frame = ttk.Frame(symptom_select_frame)
        symptom_frame.pack(fill=tk.X, pady=5)

        ttk.Label(symptom_frame, text="Enter symptom:").pack(side=tk.LEFT, padx=5)

        self.symptom_var = tk.StringVar()
        self.symptom_entry = ttk.Combobox(symptom_frame, textvariable=self.symptom_var, values=self.all_symptoms)
        self.symptom_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Severity selection
        severity_frame = ttk.Frame(symptom_select_frame)
        severity_frame.pack(fill=tk.X, pady=5)

        ttk.Label(severity_frame, text="Severity:").pack(side=tk.LEFT, padx=5)

        self.severity_var = tk.StringVar(value="Moderate")
        severity_combo = ttk.Combobox(severity_frame, textvariable=self.severity_var,
                                      values=["Mild", "Moderate", "Severe"], width=10)
        severity_combo.pack(side=tk.LEFT, padx=5)

        # Duration selection
        duration_frame = ttk.Frame(symptom_select_frame)
        duration_frame.pack(fill=tk.X, pady=5)

        ttk.Label(duration_frame, text="Duration:").pack(side=tk.LEFT, padx=5)

        self.duration_var = tk.StringVar(value="Days")
        duration_combo = ttk.Combobox(duration_frame, textvariable=self.duration_var,
                                      values=["Hours", "Days", "Weeks", "Months"], width=10)
        duration_combo.pack(side=tk.LEFT, padx=5)

        # Add button
        add_button = ttk.Button(symptom_select_frame, text="Add Symptom", command=self.add_symptom)
        add_button.pack(pady=10)

        # Filter by category
        filter_frame = ttk.Frame(symptom_select_frame)
        filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filter_frame, text="Filter by category:").pack(side=tk.LEFT, padx=5)

        self.category_var = tk.StringVar(value="All")
        categories = ["All"] + sorted(set(self.symptom_categories.values()))
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var,
                                      values=categories, width=15)
        category_combo.pack(side=tk.LEFT, padx=5)

        # Bind category selection to update symptom list
        category_combo.bind("<<ComboboxSelected>>", self.filter_symptoms_by_category)

        # Common symptoms suggestions
        common_frame = ttk.LabelFrame(symptom_select_frame, text="Common Symptoms", padding="5")
        common_frame.pack(fill=tk.X, pady=10)

        common_symptoms = ["fever", "cough", "headache", "fatigue", "nausea", "sore throat"]
        common_buttons_frame = ttk.Frame(common_frame)
        common_buttons_frame.pack(fill=tk.X)

        for i, symptom in enumerate(common_symptoms):
            btn = ttk.Button(common_buttons_frame, text=symptom.capitalize(),
                             command=lambda s=symptom: self.quick_add_symptom(s))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")

        for i in range(3):
            common_buttons_frame.columnconfigure(i, weight=1)

        # Selected symptoms display (right frame)
        selected_frame = ttk.LabelFrame(right_frame, text="Selected Symptoms", padding="10")
        selected_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollable frame for selected symptoms
        self.selected_canvas = tk.Canvas(selected_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(selected_frame, orient="vertical", command=self.selected_canvas.yview)
        self.selected_symptoms_frame = ttk.Frame(self.selected_canvas)

        self.selected_symptoms_frame.bind(
            "<Configure>",
            lambda e: self.selected_canvas.configure(scrollregion=self.selected_canvas.bbox("all"))
        )

        self.selected_canvas.create_window((0, 0), window=self.selected_symptoms_frame, anchor="nw")
        self.selected_canvas.configure(yscrollcommand=scrollbar.set)

        self.selected_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.selected_symptoms = []
        self.update_selected_symptoms_display()

        # Diagnosis button
        diagnose_button = ttk.Button(symptoms_tab, text="Get Diagnosis",
                                     command=lambda: [self.diagnose(), notebook.select(results_tab)])
        diagnose_button.pack(pady=10)

        # ---- Results Tab ----
        self.results_frame = ttk.Frame(results_tab)
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        # Results area
        self.results_text = scrolledtext.ScrolledText(self.results_frame, wrap=tk.WORD, height=20)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.results_text.config(state=tk.DISABLED)

        # Action buttons
        action_frame = ttk.Frame(self.results_frame)
        action_frame.pack(fill=tk.X, pady=10)

        save_button = ttk.Button(action_frame, text="Save Results", command=self.save_results)
        save_button.pack(side=tk.LEFT, padx=5)

        clear_button = ttk.Button(action_frame, text="Clear All", command=self.clear_all)
        clear_button.pack(side=tk.LEFT, padx=5)

        # ---- Patient Information Tab ----
        patient_frame = ttk.LabelFrame(info_tab, text="Patient Details", padding="10")
        patient_frame.pack(fill=tk.X, pady=10)

        # Age
        age_frame = ttk.Frame(patient_frame)
        age_frame.pack(fill=tk.X, pady=5)

        ttk.Label(age_frame, text="Age:").pack(side=tk.LEFT, padx=5)
        self.age_var = tk.StringVar()
        age_entry = ttk.Entry(age_frame, textvariable=self.age_var, width=10)
        age_entry.pack(side=tk.LEFT, padx=5)

        # Gender
        gender_frame = ttk.Frame(patient_frame)
        gender_frame.pack(fill=tk.X, pady=5)

        ttk.Label(gender_frame, text="Gender:").pack(side=tk.LEFT, padx=5)
        self.gender_var = tk.StringVar()
        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side=tk.LEFT,
                                                                                                    padx=5)
        ttk.Radiobutton(gender_frame, text="Other", variable=self.gender_var, value="Other").pack(side=tk.LEFT, padx=5)

        # Medical History
        history_frame = ttk.LabelFrame(info_tab, text="Medical History", padding="10")
        history_frame.pack(fill=tk.X, pady=10)

        # Existing conditions
        ttk.Label(history_frame, text="Existing medical conditions:").pack(anchor=tk.W, pady=5)
        self.conditions_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, height=3)
        self.conditions_text.pack(fill=tk.X, pady=5)

        # Medications
        ttk.Label(history_frame, text="Current medications:").pack(anchor=tk.W, pady=5)
        self.medications_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, height=3)
        self.medications_text.pack(fill=tk.X, pady=5)

        # Allergies
        ttk.Label(history_frame, text="Allergies:").pack(anchor=tk.W, pady=5)
        self.allergies_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, height=2)
        self.allergies_text.pack(fill=tk.X, pady=5)

        # Save patient info button
        save_info_button = ttk.Button(info_tab, text="Save Patient Information",
                                      command=self.save_patient_info)
        save_info_button.pack(pady=10)

        # ---- Help Tab ----
        help_text = """
        HOW TO USE THIS APPLICATION:

        1. Enter your symptoms one by one in the "Symptoms" tab.
        2. For each symptom, select severity and duration.
        3. Click "Add Symptom" to add each symptom to your list.
        4. Remove symptoms by clicking the "✕" button next to them.
        5. (Optional) Fill in patient information in the "Patient Information" tab.
        6. Click "Get Diagnosis" to see possible conditions matching your symptoms.

        TIPS FOR ACCURATE DIAGNOSIS:

        - Be as specific as possible with your symptoms
        - Include all symptoms, even minor ones
        - Rate severity accurately
        - Provide accurate duration information
        - Include relevant medical history in the Patient Information tab

        IMPORTANT MEDICAL DISCLAIMER:

        This tool provides information only and should not replace professional medical advice.
        Always consult a healthcare provider for medical concerns.
        In case of emergency, call your local emergency number (e.g., 911 in the US).
        """

        help_scroll = scrolledtext.ScrolledText(help_tab, wrap=tk.WORD, height=20)
        help_scroll.pack(fill=tk.BOTH, expand=True, pady=10)
        help_scroll.insert(tk.END, help_text)
        help_scroll.config(state=tk.DISABLED)

    def filter_symptoms_by_category(self, event=None):
        category = self.category_var.get()
        if category == "All":
            self.symptom_entry.config(values=self.all_symptoms)
        else:
            filtered_symptoms = [symptom for symptom, cat in self.symptom_categories.items()
                                 if cat == category]
            self.symptom_entry.config(values=sorted(filtered_symptoms))

    def quick_add_symptom(self, symptom):
        self.symptom_var.set(symptom)
        self.add_symptom()

    def add_symptom(self):
        symptom = self.symptom_var.get().strip().lower()
        severity = self.severity_var.get()
        duration = self.duration_var.get()

        if not symptom:
            messagebox.showinfo("Information", "Please enter a symptom.")
            return

        # Check if symptom already exists
        for s in self.selected_symptoms:
            if s["name"] == symptom:
                messagebox.showinfo("Information", f"Symptom '{symptom}' already added.")
                return

        # Add symptom with metadata
        self.selected_symptoms.append({
            "name": symptom,"name": symptom,
            "severity": severity,
            "duration": duration,
            "added_time": datetime.now()
        })

        self.update_selected_symptoms_display()
        self.symptom_var.set("")

    def update_selected_symptoms_display(self):
        # Clear the frame
        for widget in self.selected_symptoms_frame.winfo_children():
            widget.destroy()

        # Display selected symptoms as buttons that can be removed
        if not self.selected_symptoms:
            ttk.Label(self.selected_symptoms_frame, text="No symptoms selected").pack(anchor=tk.W)
        else:
            for i, symptom_data in enumerate(self.selected_symptoms):
                symptom = symptom_data["name"]
                severity = symptom_data["severity"]
                duration = symptom_data["duration"]

                symptom_frame = ttk.Frame(self.selected_symptoms_frame)
                symptom_frame.pack(fill=tk.X, pady=2)

                # Set background color based on severity
                severity_color = "#FFE0E0" if severity == "Severe" else "#FFFFD0" if severity == "Moderate" else "#E0FFE0"

                # Create a label with colored background
                symptom_label = tk.Label(symptom_frame,
                                        text=f"• {symptom.capitalize()} ({severity}, {duration})",
                                        anchor="w", bg=severity_color, padx=5, pady=2)
                symptom_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

                remove_button = ttk.Button(symptom_frame, text="✕", width=2,
                                         command=lambda s=symptom: self.remove_symptom(s))
                remove_button.pack(side=tk.RIGHT, padx=5)

    def remove_symptom(self, symptom_name):
        self.selected_symptoms = [s for s in self.selected_symptoms if s["name"] != symptom_name]
        self.update_selected_symptoms_display()

    def diagnose(self):
        if not self.selected_symptoms:
            messagebox.showinfo("Information", "Please select at least one symptom.")
            return

        # Get patient info for contextual diagnosis
        age = self.age_var.get().strip()
        gender = self.gender_var.get()

        # Extract symptom names for matching
        symptom_names = [s["name"] for s in self.selected_symptoms]
        symptom_data = {s["name"]: {"severity": s["severity"], "duration": s["duration"]}
                      for s in self.selected_symptoms}

        # Calculate match scores for each condition using enhanced algorithm
        results = {}
        for condition, data in self.medical_data.items():
            condition_symptoms = data["symptoms"]

            # 1. Check if key symptoms are present
            key_symptoms = [s for s, props in condition_symptoms.items() if props["key"]]
            matched_key_symptoms = [s for s in key_symptoms if s in symptom_names]
            key_symptom_ratio = len(matched_key_symptoms) / len(key_symptoms) if key_symptoms else 0

            # 2. Calculate weighted match score for all symptoms
            total_possible_weight = sum(props["weight"] for props in condition_symptoms.values())
            matched_weight = sum(condition_symptoms[s]["weight"] for s in symptom_names if s in condition_symptoms)

            # 3. Calculate how many symptoms the user has that match this condition
            matched_symptoms = [s for s in symptom_names if s in condition_symptoms]
            symptom_match_ratio = len(matched_symptoms) / len(symptom_names) if symptom_names else 0

            # 4. Adjust score based on user-reported severity for key symptoms
            severity_modifier = 1.0
            for symptom in matched_key_symptoms:
                if symptom in symptom_data:
                    if symptom_data[symptom]["severity"] == "Severe":
                        severity_modifier *= 1.2
                    elif symptom_data[symptom]["severity"] == "Mild":
                        severity_modifier *= 0.8

            # Calculate final weighted score
            # Higher importance to key symptoms and matched weight
            if not matched_key_symptoms and key_symptoms:
                base_score = 0.1  # Very low score if no key symptoms matched
            else:
                # Base formula - weightings can be adjusted
                base_score = (
                    (key_symptom_ratio * 0.5) +  # 50% weight to key symptoms
                    (matched_weight / total_possible_weight * 0.3) +  # 30% weight to weighted symptom match
                    (symptom_match_ratio * 0.2)  # 20% weight to overall symptom coverage
                )

            # Apply severity modifier
            final_score = base_score * severity_modifier

            # Only include in results if score is above threshold
            if final_score > 0.15:
                results[condition] = {
                    "score": final_score,
                    "matched_symptoms": matched_symptoms,
                    "matched_key_symptoms": matched_key_symptoms,
                    "description": data["description"],
                    "recommendations": data["recommendations"],
                    "incubation_period": data.get("incubation_period", "Unknown"),
                    "typical_duration": data.get("typical_duration", "Variable"),
                    "risk_factors": data.get("risk_factors", []),
                    "differential_diagnosis": data.get("differential_diagnosis", [])
                }

        # Add this diagnosis to history
        self.user_history.append({
            "timestamp": datetime.now(),
            "symptoms": self.selected_symptoms.copy(),
            "results": results
        })

        self.display_results(results)

    def display_results(self, results):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        # Get patient age and gender for contextualized results
        age = self.age_var.get().strip()
        gender = self.gender_var.get()

        # Add header with timestamp and patient info if available
        header = f"DIAGNOSIS RESULTS - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        if age and gender:
            header += f"Patient: {age} year old {gender}\n"

        # Add symptom summary
        header += f"\nSymptoms analyzed ({len(self.selected_symptoms)}):\n"
        for symptom in self.selected_symptoms:
            header += f"• {symptom['name'].capitalize()} ({symptom['severity']}, {symptom['duration']})\n"

        self.results_text.insert(tk.END, header + "\n", "header")

        if not results:
            self.results_text.insert(tk.END, "No matching conditions found for the selected symptoms.\n\n", "warning")
            self.results_text.insert(tk.END, "Please consider:\n")
            self.results_text.insert(tk.END, "• Adding more specific symptoms\n")
            self.results_text.insert(tk.END, "• Checking symptom severity and duration\n")
            self.results_text.insert(tk.END, "• Consulting a healthcare professional\n\n")
        else:
            # Sort conditions by score
            sorted_results = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)

            self.results_text.insert(tk.END, "POSSIBLE CONDITIONS (by relevance):\n\n", "section")

            # Group results by confidence level
            high_confidence = []
            medium_confidence = []
            low_confidence = []

            for condition, data in sorted_results:
                match_percentage = int(data["score"] * 100)
                if match_percentage >= 70:
                    high_confidence.append((condition, data, match_percentage))
                elif match_percentage >= 40:
                    medium_confidence.append((condition, data, match_percentage))
                else:
                    low_confidence.append((condition, data, match_percentage))

            # Display high confidence results
            if high_confidence:
                self.results_text.insert(tk.END, "High probability conditions:\n", "subsection")
                for condition, data, match_percentage in high_confidence:
                    self.display_condition(condition, data, match_percentage)

            # Display medium confidence results
            if medium_confidence:
                self.results_text.insert(tk.END, "\nModerate probability conditions:\n", "subsection")
                for condition, data, match_percentage in medium_confidence:
                    self.display_condition(condition, data, match_percentage)

            # Display low confidence results
            if low_confidence:
                self.results_text.insert(tk.END, "\nLower probability conditions:\n", "subsection")
                for condition, data, match_percentage in low_confidence:
                    self.display_condition(condition, data, match_percentage)

            # Add next steps
            self.results_text.insert(tk.END, "\nRECOMMENDED NEXT STEPS:\n", "section")
            if high_confidence:
                next_steps = "Based on your symptoms, consider the recommendations for "
                next_steps += f"{high_confidence[0][0]}. "
                self.results_text.insert(tk.END, next_steps)

            self.results_text.insert(tk.END, "\n• Record any changes in symptoms\n")
            self.results_text.insert(tk.END, "• Consider consultation with a healthcare provider\n")

            # Check for any severe symptoms that might require urgent care
            severe_symptoms = [s for s in self.selected_symptoms if s["severity"] == "Severe"]
            if severe_symptoms:
                urgent_text = "\nUrgent symptoms detected. Consider seeking prompt medical attention.\n"
                self.results_text.insert(tk.END, urgent_text, "warning")

        # Add disclaimer
        disclaimer = ("\n\nIMPORTANT: This is not a professional medical diagnosis. "
                     "The results are based on symptom matching only and do not account for all medical factors. "
                     "Please consult with a healthcare provider for proper medical advice.")
        self.results_text.insert(tk.END, disclaimer, "disclaimer")

        self.results_text.config(state=tk.DISABLED)

        # Configure text tags for styling
        self.results_text.tag_configure("header", font=("Arial", 11, "bold"), background="#E6E6E6")
        self.results_text.tag_configure("section", font=("Arial", 11, "bold"), foreground="#2A5A8C")
        self.results_text.tag_configure("subsection", font=("Arial", 10, "bold"), foreground="#2A5A8C")
        self.results_text.tag_configure("condition", font=("Arial", 10, "bold"))
        self.results_text.tag_configure("warning", foreground="red", font=("Arial", 10, "bold"))
        self.results_text.tag_configure("key_symptom", foreground="#006600")
        self.results_text.tag_configure("matched_symptom", foreground="#000066")
        self.results_text.tag_configure("disclaimer", foreground="#888888", font=("Arial", 9, "italic"))

    def display_condition(self, condition, data, match_percentage):
        # Confidence indicator
        confidence = "★★★" if match_percentage >= 70 else "★★" if match_percentage >= 40 else "★"

        # Insert condition name with match percentage
        self.results_text.insert(tk.END, f"{condition} ", "condition")
        self.results_text.insert(tk.END, f"({match_percentage}% match) {confidence}\n")

        # Key matched symptoms
        if data["matched_key_symptoms"]:
            self.results_text.insert(tk.END, "Key matched symptoms: ")
            self.results_text.insert(tk.END, ", ".join(s.capitalize() for s in data["matched_key_symptoms"]) + "\n", "key_symptom")

        # Other matched symptoms
        other_symptoms = [s for s in data["matched_symptoms"] if s not in data["matched_key_symptoms"]]
        if other_symptoms:
            self.results_text.insert(tk.END, "Other matched symptoms: ")
            self.results_text.insert(tk.END, ", ".join(s.capitalize() for s in other_symptoms) + "\n", "matched_symptom")

        # Description and recommendations
        self.results_text.insert(tk.END, f"Description: {data['description']}\n")
        self.results_text.insert(tk.END, f"Recommendations: {data['recommendations']}\n")

        # Additional information
        self.results_text.insert(tk.END, f"Typical duration: {data['typical_duration']}\n")

        # Risk factors if present
        if data["risk_factors"]:
            self.results_text.insert(tk.END, "Risk factors: " + ", ".join(data["risk_factors"]) + "\n")

        self.results_text.insert(tk.END, "\n")

    def save_results(self):
        if not hasattr(self, 'user_history') or not self.user_history:
            messagebox.showinfo("Information", "No diagnosis results to save.")
            return

        # Get the latest diagnosis
        latest = self.user_history[-1]

        # Create a filename with timestamp
        timestamp = latest["timestamp"].strftime("%Y%m%d_%H%M%S")
        filename = f"diagnosis_results_{timestamp}.txt"

        try:
            with open(filename, "w") as f:
                # Write header
                f.write(f"MEDICAL SYMPTOM DIAGNOSIS RESULTS\n")
                f.write(f"Date/Time: {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # Patient info if available
                age = self.age_var.get().strip()
                gender = self.gender_var.get()
                if age and gender:
                    f.write(f"Patient: {age} year old {gender}\n\n")

                # Write symptoms
                f.write(f"REPORTED SYMPTOMS:\n")
                for symptom in latest["symptoms"]:
                    f.write(f"• {symptom['name'].capitalize()} ({symptom['severity']}, {symptom['duration']})\n")
                f.write("\n")

                # Write results
                f.write("POSSIBLE CONDITIONS:\n")
                sorted_results = sorted(latest["results"].items(),
                                      key=lambda x: x[1]["score"], reverse=True)

                for condition, data in sorted_results:
                    match_percentage = int(data["score"] * 100)
                    f.write(f"\n{condition} - {match_percentage}% match\n")

                    # Key matched symptoms
                    if data["matched_key_symptoms"]:
                        f.write("Key matched symptoms: ")
                        f.write(", ".join(s.capitalize() for s in data["matched_key_symptoms"]) + "\n")

                    # Other matched symptoms
                    other_symptoms = [s for s in data["matched_symptoms"]
                                    if s not in data["matched_key_symptoms"]]
                    if other_symptoms:
                        f.write("Other matched symptoms: ")
                        f.write(", ".join(s.capitalize() for s in other_symptoms) + "\n")

                    f.write(f"Description: {data['description']}\n")
                    f.write(f"Recommendations: {data['recommendations']}\n")
                    f.write(f"Typical duration: {data['typical_duration']}\n")

                # Write disclaimer
                f.write("\n\nDISCLAIMER: This is not a professional medical diagnosis. ")
                f.write("The results are based on symptom matching only and do not account for all medical factors. ")
                f.write("Please consult with a healthcare provider for proper medical advice.")

            messagebox.showinfo("Success", f"Diagnosis results saved to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")

    def save_patient_info(self):
        age = self.age_var.get().strip()
        gender = self.gender_var.get()
        conditions = self.conditions_text.get("1.0", tk.END).strip()
        medications = self.medications_text.get("1.0", tk.END).strip()
        allergies = self.allergies_text.get("1.0", tk.END).strip()

        if not (age or gender or conditions or medications or allergies):
            messagebox.showinfo("Information", "No patient information to save.")
            return

        # Create a filename
        filename = "patient_info.json"

        try:
            patient_info = {
                "age": age,
                "gender": gender,
                "medical_conditions": conditions,
                "medications": medications,
                "allergies": allergies,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            with open(filename, "w") as f:
                json.dump(patient_info, f, indent=4)

            messagebox.showinfo("Success", f"Patient information saved to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save patient information: {str(e)}")

    def clear_all(self):
        # Clear symptoms
        self.selected_symptoms = []
        self.update_selected_symptoms_display()

        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)

        # Reset diagnosis history
        self.user_history = []

        messagebox.showinfo("Information", "All data has been cleared.")

    def show_help(self):
        help_text = """
        HOW TO USE THIS APPLICATION:
        
        1. Enter your symptoms one by one in the symptom entry field.
        2. For each symptom, select severity and duration.
        3. Click "Add Symptom" to add each symptom to your list.
        4. Remove symptoms by clicking the "✕" button next to them.
        5. Click "Get Diagnosis" to see possible conditions matching your symptoms.
        
        TIPS FOR BETTER RESULTS:
        
        - Be as specific as possible with your symptoms
        - Include all symptoms, even minor ones
        - Rate the severity accurately
        - Fill in the Patient Information tab if possible
        
        IMPORTANT NOTES:
        
        - This tool provides information only and should not replace professional medical advice.
        - Always consult a healthcare provider for medical concerns.
        - In case of emergency, call your local emergency number (e.g., 911 in the US).
        """
        messagebox.showinfo("Help", help_text)

def save_medical_data_to_file(data, filename="medical_data.json"):
    """Utility function to save the medical data to a file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_medical_data_from_file(filename="medical_data.json"):
    """Utility function to load medical data from a file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def main():
    root = tk.Tk()
    app = DiagnosisAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()