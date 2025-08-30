# 🗳️ Voter ID Card Details Extractor (Physical ➝ Digital)

This project converts **physical voter ID card details** into a **digital dataset**.  
It uses **OCR (Tesseract)** + **Flask web app** to extract voter details (Name, Father's Name, House No., Age, Sex) from uploaded images and stores them in an **Excel file (CSV)**.  

---

## 🚀 Features
- Upload scanned **Voter ID card images (JPG/PNG)**  
- OCR extraction using **Tesseract**  
- Preprocessing with **OpenCV** for better accuracy  
- Extract and digitize fields:
  - Name  
  - Father’s Name  
  - House No.  
  - Age  
  - Sex  
- Save extracted records in **`id_dataset.csv` (Excel-compatible)**  
- View **latest extraction** and **all past records** in a neat web UI  

---

## 🛠️ Tech Stack
- **Python 3**  
- **Flask** – Web app framework  
- **OpenCV** – Image preprocessing  
- **pytesseract** – OCR  
- **Pandas** – Data storage in Excel/CSV  

---

## How to RUN
- Install Tesseract OCR
- then Update path in app.py in **pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"**
- install all required modules by running **pip install -r requirements.txt** in cmd (in Project path)
- Then simply run **python app.py** in cmd in respective folder
- then the website will run locally , just ctrl+click on the local host link


