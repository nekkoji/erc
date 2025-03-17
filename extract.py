from PIL import Image
import os
import pytesseract
import pdf2image

def sanitize_filename(filename):
    filename = "".join(c if c.isalnum() or c in ("-", "") else "" for c in filename)
    return filename.lstrip("_")

def extract_serial_number_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            images = pdf2image.convert_from_path(pdf_path)
            
            serial_number = None
            for image in images:
                text = pytesseract.image_to_string(image, lang='eng', config='-l eng --psm 6')
                
                lines = text.split('\n')
                for line in lines:
                    if 'Serial No.' in line:
                        serial_number = line.split('Serial No.')[-1].strip()
                        serial_number = sanitize_filename(serial_number)
                        break
                
                if serial_number:
                    break
            
            if serial_number:
                new_filename = f"{serial_number}.pdf"
                new_path = os.path.join(folder_path, new_filename)
                
                if not os.path.exists(new_path):
                    try:
                        os.rename(pdf_path, new_path)
                        print(f"Renamed: {filename} -> {new_filename}")
                    except FileNotFoundError:
                        print(f"Error: File {pdf_path} not found.")
                    except Exception as e:
                        print(f"Error renaming {filename}: {e}")
                else:
                    print(f"Skipped renaming {filename}, {new_filename} already exists.")
            else:
                print(f"Serial number not found in {filename}")

folder_path = "C:/Users/CJ/OneDrive/Desktop/ERC/MAY 2019 OBR"
extract_serial_number_from_folder(folder_path)