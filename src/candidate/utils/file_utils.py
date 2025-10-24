import fitz

def extract_text_from_pdf(paths: str) -> str:
    # paths = path,path,path
    text = []
    for path in paths.split(","):
        doc = fitz.open(path)
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text).strip()