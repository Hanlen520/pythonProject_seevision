# coding = utf8

import os

import pandas as pd

os.path.abspath(".")

import fitz
import glob
import pdfplumber


def readPDF_text(pdf_file="./Mac os极简用法及设置.pdf"):
    page_content = []
    with pdfplumber.open(pdf_file) as pdf:
        pdf_pages = pdf.pages
        for i in range(0, len(pdf_pages)):
            cur_page = pdf_pages[i]
            cur_page_content = cur_page.extract_text().strip()
            print("==========当前页面【{}】的文字内容是：==========\n\n{}\n".format(str(i + 1), cur_page_content))
            page_content.append(cur_page_content)
    if page_content:
        return page_content
    else:
        return 0


def toTxt(result):
    with open("./Result.txt", "a+", encoding="utf-8") as f:
        f.write(result + "\n")


# 从excel中读取数据并返回（element）
def read_excel_for_page_element(form="./page_sheet.xlsx", sheet_name="calendar_page",
                                element_name="guide_got_it"):
    df = pd.read_excel(form, sheet_name=sheet_name, index_col="element_name", engine="openpyxl")
    original_data = df.loc[element_name, "element_data"]
    return original_data


if __name__ == '__main__':
    # pdf_file = "./Mac os极简用法及设置.pdf"
    pdf_file = "./AndroidTool_Guide.pdf"
    # print(readPDF_text(pdf_file))
    pdf_contents = readPDF_text(pdf_file)
    for pdfContent in pdf_contents:
        toTxt(pdfContent)
        # if "office" in pdfContent:
        #     print("PASS")
    print(read_excel_for_page_element())
