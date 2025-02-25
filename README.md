# PharmaMate
# 🏥 A Pharmacist’s assistant, that automatically matches orders against handwritten prescriptions and creates orders for patient also Diagnose based on Symptoms

## **📌 Project Overview**  

1. **Prescription Processing (`main.py`)**  
   - Takes an image of a prescription as input.  
   - Validates the image and extracts medicine names.  
   - Checks the availability of medicines.  
   - Suggests alternative medicines if the required ones are unavailable.  
   - Generates a final order with the total cost.  

2. **Symptom-Based Diagnosis (`symptom.py`)**  
   - Asks the user for symptoms through an interactive interface.  
   - Diagnoses the possible medical condition.   

This system leverages **Google Generative AI** for intelligent recommendations and uses **Tkinter** for an easy-to-use graphical interface.  

---

## **⚙️ Installation & Setup**  


1️⃣ Install Required Dependencies
- When you open in Pycharm or any such IDE click on Install Requirements

- ![Screenshot 2025-02-26 015219](https://github.com/user-attachments/assets/7721f0a9-9408-42d0-bf87-5551dceceb72)

- Or run this in terminal:  pip install -r requirements.txt
  

2️⃣ Set Up Google Generative AI API
- This project requires an API key from Google Generative AI for medicine suggestions.

- Sign up at Google AI.
- Generate an API key.
- Open main.py and replace 'your api key here' with your actual API key.

## **🚀 How to Run the Project** 
**🖼️ Running main.py (Prescription Processing & Medicine Recommendation)**
- Run this in terminal: 
- --python main.py

- Upload an image of your prescription. 
- You can also use the **image1.jpg** given in the repo 

![Screenshot 2025-02-25 193943](https://github.com/user-attachments/assets/69101541-e576-4763-8e38-c48ee78c9f83)

- The system validates and extracts medicine details.
- It checks availability and suggests alternatives if needed.

![Screenshot 2025-02-25 194032](https://github.com/user-attachments/assets/231780d8-58ba-4e22-9c88-e30b8faf7c25)

- A final order with total cost is generated.



**🩺 Running symptom.py (Symptom-Based Diagnosis)**

- -- python symptom.py
- Enter your symptoms when prompted.
- The system diagnoses possible medical conditions.

![Screenshot 2025-02-26 012755](https://github.com/user-attachments/assets/7452e878-7ab3-4099-ab1b-f14d3ba5bcc6)

![Screenshot 2025-02-26 012815](https://github.com/user-attachments/assets/0a7aa994-592e-49c2-9b7b-f93adc81ac55)


**🛠 Technologies Used**
- Python (Core programming language)
- Tkinter (GUI for user interaction)
- Pandas (Data handling for medicines)
- PIL (Pillow) (Image processing)
- Google Generative AI (Medicine recommendations)

**🤝 Contributing**
Feel free to fork this repository, create a new branch, and submit pull requests for improvements!

**🌟 Star this repo if you find it useful! ⭐**
