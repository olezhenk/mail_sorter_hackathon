#команда для запуска теста(в терминал)
#python3 -m pytest tests/test1.py -v -s
import sys                    
from pathlib import Path     
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))  
import pytest
from parser import LetterExtractor

extractor = LetterExtractor()
test_files = ["test_letter1", "test_letter2",  "test_letter3", "test_letter4", "test_letter5","test_letter6","test_letter7.txt","test_letter8.txt",
    "test_letter9.txt","test_letter10.txt","test_letter11", "test_letter12", "test_letter13", "test_letter14", "test_letter15",
    "test_letter16", "test_letter17", "test_letter18", "test_letter19", "test_letter20"]
test_dir = Path(__file__).parent

@pytest.fixture
def existing_files():
    existing = []
    for name in test_files:
        full_path = test_dir / name
        if full_path.exists():
            existing.append(name)
    return existing

@pytest.mark.parametrize("filename", test_files)
def successful_extraction(filename):
    full_path = test_dir / filename
    
    if not full_path.exists():
        pytest.skip(f"Файл {filename} отсутствует")
    
    try:
        letter = extractor.extract(str(full_path))
        print(f"успешно")
        assert letter is not None
        assert hasattr(letter, 'from_email')
        assert hasattr(letter, 'subject')
        assert hasattr(letter, 'text')
        
    except Exception as e:
        pytest.fail(f"Ошибка на {filename}: {e}")

@pytest.mark.parametrize("filename", test_files)
def letter_content(filename):
    full_path = test_dir / filename
    if not full_path.exists():
        pytest.skip(f"Файл {filename} отсутствует")
    
    letter = extractor.extract(str(full_path))
    if letter.from_email or letter.to or letter.subject or letter.text:
        print("Письмо содержит данные")
    else:
        print("Письмо пустое")
    
def types(existing_files):   
    first_file = test_dir / existing_files[0]
    letter = extractor.extract(str(first_file))
    
    assert isinstance(letter.from_email, str)
    assert isinstance(letter.to, str)
    assert isinstance(letter.subject, str)
    assert isinstance(letter.text, (str, type(None)))
    assert isinstance(letter.files, str)
    
    if letter.date is not None:
        assert hasattr(letter.date, 'year')
        assert hasattr(letter.date, 'month')
    
    print(f"типы корректны")

def nonexistent_file():
    fake_path = str(test_dir / "nonexistent.txt")
    with pytest.raises(FileNotFoundError):
        extractor.extract(fake_path)
    print("Несуществующий файл обработан корректно")