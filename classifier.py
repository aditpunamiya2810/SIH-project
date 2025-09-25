import fitz  # PyMuPDF
import os

def classify_pdf_content(pdf_path, output_dir):
    """
    Extracts text and images from a PDF and saves them into type-based folders.
    """
    # Create the main output directories if they don't already exist
    for folder in ["text", "images", "tables", "drawings"]:
        os.makedirs(os.path.join(output_dir, folder), exist_ok=True)

    # Get the PDF's base name to use for naming the output files
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return

    print(f"Processing '{base_name}.pdf'...")

    # Loop through each page of the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # 1. Extract and save all text on the page
        text = page.get_text()
        if text.strip():  # Only save if there's actual text
            text_filename = os.path.join(output_dir, "text", f"{base_name}_page_{page_num + 1}.txt")
            with open(text_filename, "w", encoding="utf-8") as text_file:
                text_file.write(text)

        # 2. Extract and save all images on the page
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = os.path.join(output_dir, "images", f"{base_name}_page_{page_num + 1}_img_{img_index}.{image_ext}")
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)

    doc.close()
    print(f"Finished processing '{base_name}.pdf'.\n")


# --- HOW TO USE ---

# 1. Put all your PDF files into one folder
pdf_source_folder = "PDFs"

# 2. Specify where you want the classified files to go
output_destination_folder = "classified_output"

# 3. Run the script
if os.path.exists(pdf_source_folder):
    for filename in os.listdir(pdf_source_folder):
        if filename.lower().endswith(".pdf"):
            pdf_file_path = os.path.join(pdf_source_folder, filename)
            classify_pdf_content(pdf_file_path, output_destination_folder)
else:
    print(f"Error: The source folder '{pdf_source_folder}' does not exist.")