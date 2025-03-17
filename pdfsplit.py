import os 
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf, output_folder): 
    if not os.path.exists(output_folder): os.makedirs(output_folder)

    reader = PdfReader(input_pdf)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        
        output_path = os.path.join(output_folder, f"page_{i + 1}.pdf")
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)
        
        print(f"Saved: {output_path}")

#Example usage

input_pdf = "C:/Users/CJ/OneDrive/Desktop/ERC/MAY 2019 OBR_0001.pdf" # Replace with your PDF file 
output_folder = "C:/Users/CJ/OneDrive/Desktop/ERC/MAY 2019 OBR"  # Replace with your desired output folder 
split_pdf(input_pdf, output_folder)