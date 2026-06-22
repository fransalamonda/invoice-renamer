import os
import sys
import subprocess


def test_tesseract():
    """Test Tesseract installation"""
    print("\n🔍 Testing Tesseract OCR...")

    # Cek PATH dulu
    try:
        result = subprocess.run(['tesseract', '--version'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract found in PATH")
            version = result.stdout.split('\n')[0] if result.stdout else "Unknown"
            print(f"   Version: {version}")
            return True
    except FileNotFoundError:
        pass

    # Cek di path umum Windows
    tesseract_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    ]

    for path in tesseract_paths:
        if os.path.exists(path):
            print(f"✅ Tesseract found at: {path}")
            return True

    print("❌ Tesseract not found!")
    print("Please install Tesseract from:")
    print("https://github.com/UB-Mannheim/tesseract/wiki")
    return False


def test_poppler():
    """Test Poppler installation"""
    print("\n🔍 Testing Poppler...")
    try:
        result = subprocess.run(['pdfinfo', '-v'],
                                capture_output=True, text=True)
        if result.returncode == 0 or "pdfinfo" in result.stderr:
            print("✅ Poppler found")
            return True
    except FileNotFoundError:
        pass

    # Cek di path umum Windows
    poppler_paths = [
        r'C:\poppler\bin\pdfinfo.exe',
        r'C:\Program Files\poppler\bin\pdfinfo.exe'
    ]

    for path in poppler_paths:
        if os.path.exists(path):
            print(f"✅ Poppler found at: {path}")
            return True

    print("⚠️  Poppler not found! pdf2image might fail.")
    print("Download from: https://github.com/oschwartz10612/poppler-windows/releases/")
    return False


def test_imports():
    """Test all imports"""
    print("\n🔍 Testing imports...")
    success = True

    try:
        import fitz
        print("✅ PyMuPDF (fitz)")
    except Exception as e:
        print(f"❌ PyMuPDF: {e}")
        success = False

    try:
        import pytesseract
        print("✅ PyTesseract")
    except Exception as e:
        print(f"❌ PyTesseract: {e}")
        success = False

    try:
        from pdf2image import convert_from_path
        print("✅ pdf2image")
    except Exception as e:
        print(f"❌ pdf2image: {e}")
        success = False

    try:
        from rapidfuzz import fuzz
        print("✅ RapidFuzz")
    except Exception as e:
        print(f"❌ RapidFuzz: {e}")
        success = False

    return success


def test_folders():
    """Test folder structure"""
    print("\n🔍 Testing folders...")
    folders = ['input', 'output', 'failed', 'logs']

    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"✅ {folder}/")
        except Exception as e:
            print(f"❌ {folder}/: {e}")
            return False

    return True


def main():
    print("=" * 60)
    print("📄 INVOICE RENAMER - SETUP TEST")
    print("=" * 60)

    all_passed = True

    if not test_imports():
        all_passed = False

    if not test_tesseract():
        all_passed = False

    if not test_poppler():
        print("\n⚠️  Poppler not found. OCR will fail for scanned PDFs!")
        print("   Please install Poppler for Windows")
        all_passed = False

    if not test_folders():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nYou can now run: python main.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("\nPlease fix the issues above.")
        print("\nQuick fixes:")
        print("  - Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  - Install Poppler: https://github.com/oschwartz10612/poppler-windows/releases/")
    print("=" * 60)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()