import os
import exifread
import PyPDF2
import docx
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image
from PIL.ExifTags import TAGS

def extract_image_metadata(image_path):
    """ Extract metadata from an image file """
    metadata = "\n🔍 Image Metadata:\n"
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                metadata += f"{tag_name}: {value}\n"
        else:
            metadata += "No EXIF metadata found.\n"
    except Exception as e:
        metadata += f"Error reading image metadata: {e}\n"
    return metadata

def extract_pdf_metadata(pdf_path):
    """ Extract metadata from a PDF file """
    metadata = "\n📄 PDF Metadata:\n"
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            meta = reader.metadata
            for key, value in meta.items():
                metadata += f"{key}: {value}\n"
    except Exception as e:
        metadata += f"Error reading PDF metadata: {e}\n"
    return metadata

def extract_doc_metadata(doc_path):
    """ Extract metadata from a Word document """
    metadata = "\n📝 DOCX Metadata:\n"
    try:
        doc = docx.Document(doc_path)
        core_props = doc.core_properties
        metadata += f"Title: {core_props.title}\n"
        metadata += f"Author: {core_props.author}\n"
        metadata += f"Created: {core_props.created}\n"
        metadata += f"Modified: {core_props.modified}\n"
    except Exception as e:
        metadata += f"Error reading DOCX metadata: {e}\n"
    return metadata

def browse_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    file_extension = file_path.lower().split(".")[-1]
    result_text.delete(1.0, tk.END)  # Clear previous output

    if file_extension in ["jpg", "jpeg", "png"]:
        result_text.insert(tk.END, extract_image_metadata(file_path))
    elif file_extension == "pdf":
        result_text.insert(tk.END, extract_pdf_metadata(file_path))
    elif file_extension == "docx":
        result_text.insert(tk.END, extract_doc_metadata(file_path))
    else:
        result_text.insert(tk.END, "⚠ Unsupported file type. Supported: JPG, PNG, PDF, DOCX\n")

# Create GUI Window
root = tk.Tk()
root.title("Metadata Extraction Tool")
root.geometry("600x400")

tk.Label(root, text="Select a file to extract metadata:").pack(pady=10)
tk.Button(root, text="Browse File", command=browse_file).pack()

# Scrollable Text Box for Output
result_text = scrolledtext.ScrolledText(root, width=70, height=15)
result_text.pack(pady=10)

root.mainloop()
