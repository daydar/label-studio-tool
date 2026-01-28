import os
from pdf2image import convert_from_path
from PIL.Image import DecompressionBombError

PDF_FOLDER = "pdfs"
PAGE_IMAGES_FOLDER = "page_images"


def create_page_images_from_pdf(input_pdf):
    """
    Script for creating images from the pages from a pdf
    """
    if not os.path.exists(PAGE_IMAGES_FOLDER):
        os.makedirs(PAGE_IMAGES_FOLDER)

    pages = []

    try:
        pages = convert_from_path(os.path.join(PDF_FOLDER, input_pdf), dpi=300)
    except DecompressionBombError as e:
        print(f"Error: {e}. Skipping {input_pdf}")

    if not pages:
        print(f"No pages found in {input_pdf}")
        return

    for i, page in enumerate(pages):
        filename, file_extension = os.path.splitext(input_pdf)
        image_path = os.path.join(PAGE_IMAGES_FOLDER, f"{filename}_page_{i + 1}.png")
        page.save(image_path, "PNG")
        print(f"Saved page {i + 1} to {image_path}")


if __name__ == "__main__":
    for pdf in os.listdir(PDF_FOLDER):
        if not pdf.endswith(".pdf"):
            continue
        create_page_images_from_pdf(pdf)
