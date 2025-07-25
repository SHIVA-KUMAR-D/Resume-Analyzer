# 🧠 AI Resume Analyzer & Job Matcher

A powerful AI-based Resume Analyzer and Job Matcher built using **Streamlit**. Upload your resume, extract key information, and get matched with relevant jobs instantly via email.

---

## 🚀 Features

- 📄 Resume Parsing (Name, Email, Phone, Skills, Education)
- 🤖 Smart Skill Matching with Job Descriptions
- 📬 Job Match Results via Email
- 🧾 PDF Report Generation
- 🌐 Simple Web Interface with Streamlit

---

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Libraries:** spaCy, PyMuPDF, ReportLab, dotenv, smtplib

---

## 📁 Project Structure

```

resume-analyzer/
├── app.py                      # Main Streamlit application
├── .env                        # Stores EMAIL\_USER and EMAIL\_PASS
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── utils/
│   ├── resume\_parser.py        # Resume parsing logic
│   ├── email\_sender.py         # Email sending logic
│   └── email\_utils.py          # Job matching and formatting
└── images/
├── demo\_home.png           # Screenshot - Home page
├── demo\_output.png         # Screenshot - Output page

````

---

## 🧑‍💻 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
````

### 2. Install Requirements

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configure Environment

Create a `.env` file in the root directory:

```
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
```

> ⚠️ Use [Gmail App Password](https://support.google.com/accounts/answer/185833) instead of your actual password.

### 4. Run Application

```bash
streamlit run app.py
```

---



## 📸 Screenshots

**Home Page**

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ea72fc3d-53bc-4548-9202-196e06a333d4" />


**Resume Analysis Output**

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b83a9a0c-9d91-49d6-8d22-af86230904cf" />


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ce126855-c9ae-45fa-a912-28c6449d95f7" />
---

## 🔐 Security

* Sensitive credentials stored in `.env` file
* Ensure `.gitignore` includes `.env`

---

## 🤝 Contributions

Contributions are welcome! Please open an issue or pull request for improvements.

---

## 📧 Contact

**Creator:** Shiva Kumar D
📬 Email: [shivayadav0539@example.com](mailto:shivayadav0539@example.com)
