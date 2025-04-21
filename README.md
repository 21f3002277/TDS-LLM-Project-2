<img src="https://github.com/user-attachments/assets/a9f996f7-6cbb-468d-8796-409aff63a82e" alt="alt text" width="500" height="300">



# TDS Course Project 2 (Jan 2025)  

## Submitted by :-

- **VIKASH PRASAD**  
- **Roll Number** - 21f3002277

## Project Title : 📘 TDS Solver – IITM Data Science Assignment Assistant
This project is part of the **Tools in Data Science** course in the **IIT Madras B.S. in Data Science** program. The goal is to build an LLM-powered API that can automatically solve questions from any of the 5 graded assignments.

## 🚀 Project Overview

The TDS Solver is a web API that takes in a question (and optionally, a file), and returns the correct answer in a simple JSON format.

It is designed to:
- Automatically answer questions from **Graded Assignments 1 to 5**
- Support file uploads (e.g., CSV or ZIP files with CSVs inside)
- Return a valid answer that can be directly used in assignments

---

## 📌 API Endpoint

### `POST /api/`

### ✅ Request Format

Send a `multipart/form-data` request with:
- `question`: The question text
- `file` (optional): File(s) needed to answer the question

### 🧪 Example (Using curl)

```bash
curl -X POST "https://your-app.vercel.app/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the \"answer\" column of the CSV file?" \
  -F "file=@abcd.zip"

### 🔁 Response Format

```json
{
  "answer": "1234567890"
}
```
