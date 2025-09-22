# src/generate_report.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
from datetime import datetime

def create_pdf(github_url, city="Mumbai"):
    out_path = "report/capstone_report.pdf"
    os.makedirs("report", exist_ok=True)
    c = canvas.Canvas(out_path, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, h-50, "CAPSTONE PROJECT: Weather Data Collection and Forecasting")
    c.setFont("Helvetica", 11)
    c.drawString(30, h-80, f"Author: <Your Name>    Date: {datetime.utcnow().date().isoformat()}")
    c.drawString(30, h-105, "Objectives:")
    objectives = [
        "1) Fetch live weather and historical last 30 days from public API",
        "2) Store readings into PostgreSQL",
        "3) Visualize last 30 days for a selected city",
        "4) Build basic ML models for short-term forecast",
        "5) Provide codebase on GitHub"
    ]
    y = h-130
    for obj in objectives:
        c.drawString(40, y, obj)
        y -= 18
    c.drawString(30, y-10, f"GitHub Repository: {github_url}")
    # embed sample image if available
    img_path = f"report/{city}_temperature_last30.png"
    if os.path.exists(img_path):
        try:
            c.drawImage(img_path, 30, y-320, width=500, height=250, preserveAspectRatio=True)
        except Exception as e:
            print("Could not embed image:", e)
    c.showPage()
    c.save()
    print("PDF created at", out_path)

if __name__ == "__main__":
    # Replace with your repo URL
    create_pdf("https://github.com/yourusername/capstone-weather")
