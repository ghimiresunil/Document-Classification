import os
import re
import string
import timeit
import docx2txt
import fitz
import config as cfg
from subprocess import PIPE, Popen


def clean_text(text, dolower):
    """Accepts the plain text and makes use of regex for cleaning the noise.

    Args:
        text (_type_): str
                    plain text
        dolower (_type_): Boolean
                    Boolean value for text uppercase or lowercase
    Returns: cleaned text
        _type_: str
    """
    if dolower == True:
        text = text.lower()

    text = [i.strip() for i in text.splitlines()]
    text = "\n".join(text)

    for old, new in cfg.cleantext_replacements:
        text = re.sub(old, new, text)

    text = text.encode("ascii", errors="ignore").decode("utf-8")
    exclude = set(string.punctuation)
    regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
    text = "".join(ch for ch in text if ch not in exclude)
    text = " ".join(text.split())  # removing the white spaces
    text = re.sub(regex, " ", text)
    
    return text


def doc_to_text(filepath, dolower):
    """Extract the clean text from the doc file path.

    Args:
        filepath (_type_): str
                    filepath with .txt extension
        dolower (_type_): Boolean
                    boolean value for text uppercase of lowercase
    Returns: cleaned text
        _type_: str
    """
    try:
        text = ""
        cmd = ["antiword", filepath]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        text += stdout.decode("utf-8", "ignore")
        text = clean_text(text, dolower)
        return text
    except:
        text = ""


def docx_to_text(file_path, dolower):
    """Takes docx files and extracts plain text from the docx files.

    Args:
        file_path (_type_): str
                    filepath with .docx extension
        dolower (_type_): Boolean
                    Boolean value for text uppercase or lowercase
    Returns: cleaned text
        _type_: str
    """
    text = ""
    text += docx2txt.process(file_path)
    text = clean_text(text, dolower)
    return text


def pdf_to_text(file_path, dolower):
    """Takes filepath and extracts the plain text from pdf
    Args:
        file_path (_type_): str
                        filepath with .pdf extension
        dolower (_type_): boolean
                        boolean value for text uppercase or lowercase
    Returns: cleaned text
        _type_: str
    """
    doc = fitz.open(file_path)
    number_of_pages = doc.page_count
    text = ""
    for i in range(0, number_of_pages):
        page = doc.load_page(i)
        pagetext = page.get_text("text", sort=True, flags=16)
        text += pagetext
    text = clean_text(text, dolower)
    return text


def txt_to_text(file_path, dolower):
    """Extract the plain text from text files.

    Args:
        file_path (_type_): str
                filepath with .txt extension
        dolower (_type_): Boolean
                Boolean value for text uppercase or lowercase
    Returns: cleaned text
        _type_: str
    """
    text = ""
    with open(
        file_path, encoding="unicode_escape", errors="strict", buffering=1
    ) as file:
        data = file.read()
    text += data
    text = clean_text(text, dolower)
    return text


def prepare_text(file, dolower):
    """Take the resume of different extension .pdf, .docx, .doc, and .txt
    and use the suitable method to extract text
    Args:
        file (_type_): str
                   valid filepath with different .pdf, .docx, doc, and .txt entension
        dolower (_type_): boolean
                    boolean value for text upper case and lowercase
    Returns: cleaned text
        _type_: str
    Raises:
        KeyError: Raises an exception.
    """
    reader_choice = {
        ".pdf": pdf_to_text,
        ".docx": docx_to_text,
        ".doc": doc_to_text,
        ".txt": txt_to_text,
    }

    if os.path.isfile(file):
        _, ext = os.path.splitext(file)
        try:
            file_content = reader_choice[ext](file, dolower=dolower)

        except KeyError as e:
            return "Could not process files with this extension"
        return file_content
    else:
        return "Make sure uploaded file exist"

""" <----------------- Testing ---------------------->"""
if __name__ == "__main__":
    start_time = timeit.default_timer()
    cleaned_text = prepare_text(
        "data/resume_job_other_data/resume/Anish Thapaliya.pdf", dolower=True
    )
    print(cleaned_text)
    print("-" * 50)
    print(
        "Total Time Taken for parsing is %s seconds "
        % (timeit.default_timer() - start_time)
    )
    print("-" * 50)
