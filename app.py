import os
import re
import cv2
import pytesseract
import pandas as pd
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
DATASET_PATH = "id_dataset.csv"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(img_path: str) -> str:
    img = cv2.imread(img_path)
    if img is None:
        return ""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return pytesseract.image_to_string(thresh, config="--oem 3 --psm 6")

def extract_fields(text: str) -> dict:
    fields = {"Name": "", "Father's Name": "", "House No.": "", "Age": "", "Sex": ""}

    # Normalize text
    clean_text = text.replace("’", "'").replace("‘", "'")
    clean_text = re.sub(r"\s+", " ", clean_text)

    # Use non-greedy match until next keyword
    name_match = re.search(r"NAME\s*:\s*(.*?)(?=FATHER|HOUSE|AGE|SEX|$)", clean_text, re.I)
    father_match = re.search(r"FATHER'?S NAME\s*:\s*(.*?)(?=HOUSE|AGE|SEX|$)", clean_text, re.I)
    house_match = re.search(r"HOUSE NO\.?\s*:\s*(.*?)(?=AGE|SEX|$)", clean_text, re.I)
    age_match = re.search(r"AGE\s*:\s*(\d+)", clean_text, re.I)
    sex_match = re.search(r"SEX\s*:\s*([A-Z]+)", clean_text, re.I)

    if name_match:
        fields["Name"] = name_match.group(1).strip()
    if father_match:
        fields["Father's Name"] = father_match.group(1).strip()
    if house_match:
        fields["House No."] = house_match.group(1).strip()
    if age_match:
        fields["Age"] = age_match.group(1).strip()
    if sex_match:
        fields["Sex"] = sex_match.group(1).strip()

    return fields


def save_to_dataset(fields: dict):
    df = pd.read_csv(DATASET_PATH)
    df = pd.concat([df, pd.DataFrame([fields])], ignore_index=True)
    df.to_csv(DATASET_PATH, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    fields = None
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return redirect("/")
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(save_path)

        text = extract_text(save_path)
        print("------------------")
        print(text)
        print("------------------")
        fields = extract_fields(text)
        save_to_dataset(fields)

    records = pd.read_csv(DATASET_PATH).to_dict(orient="records")
    return render_template("index.html", fields=fields, records=records)

if __name__ == "__main__":
    app.run(debug=True)
