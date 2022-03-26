# coding = utf8

import os

os.path.abspath(".")

import fitz
import glob
import pdfplumber


def readPDF(pdf_file="./Mac os极简用法及设置.pdf"):
    with pdfplumber.open(pdf_file) as pdf:
        pdf_pages = pdf.pages
        for i in range(0, len(pdf_pages)):
            cur_page = pdf_pages[i]
            print(cur_page.extract_text())

if __name__ == '__main__':
    pdf_file = "./Mac os极简用法及设置.pdf"
    readPDF(pdf_file)
