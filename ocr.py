import os
from PIL import Image
import pytesseract
import natsort
import re
from gtts import gTTS

# Configuração do Tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Ajuste conforme necessário
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/'

def add_natural_pauses(text):
    text = re.sub(r'([.!?])', r'\1. ', text)
    text = re.sub(r'(,)', r'\1 ', text)
    return text

def synthesize_text(text, output_path):
    try:
        tts = gTTS(text=text, lang='pt', slow=False)
        tts.save(output_path)
    except Exception as e:
        print(f"Erro ao gerar áudio: {str(e)}")

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='por')
        return text.strip() if text else None
    except Exception as e:
        print(f"Erro ao processar {image_path}: {str(e)}")
        return None

input_dir = 'data'
output_dir = 'output'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
image_files = natsort.natsorted(image_files)

for image_file in image_files:
    image_path = os.path.join(input_dir, image_file)
    
    text = extract_text_from_image(image_path)
    
    if text:
        text_with_pauses = add_natural_pauses(text)
        
        output_filename_audio = os.path.splitext(image_file)[0] + '.mp3'
        output_path_audio = os.path.join(output_dir, output_filename_audio)
        
        output_filename_text = os.path.splitext(image_file)[0] + '.txt'
        output_path_text = os.path.join(output_dir, output_filename_text)
        
        with open(output_path_text, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        
        synthesize_text(text_with_pauses, output_path_audio)
        
        print(f'Processado com sucesso: {image_file} -> {output_filename_audio} e {output_filename_text}')
    else:
        print(f'Nenhum texto encontrado em {image_file}')

print("Processamento concluído!")