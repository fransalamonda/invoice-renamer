from dotenv import load_dotenv
import os

load_dotenv()

# Folder paths
INPUT_FOLDER = os.getenv("INPUT_FOLDER", "input")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "output")
FAILED_FOLDER = os.getenv("FAILED_FOLDER", "failed")
LOG_FOLDER = os.getenv("LOG_FOLDER", "logs")

# OCR settings
OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng+ind")
MIN_TEXT_LENGTH = int(os.getenv("MIN_TEXT_LENGTH", 50))
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 2))

# Create folders if not exists
for folder in [INPUT_FOLDER, OUTPUT_FOLDER, FAILED_FOLDER, LOG_FOLDER]:
    os.makedirs(folder, exist_ok=True)