from ingestion import extract_pdf_with_pages, chunk_text

PDF_PATH = "data/uploads/article5.pdf"  # change if your PDF is elsewhere

def main():
    print("Testing PDF extraction...")
    pages = extract_pdf_with_pages(PDF_PATH)

    print(f"Total pages extracted: {len(pages)}")
    print("First page sample:")
    print(pages[0])
    print("-" * 50)

    print("Testing chunking...")
    chunks = chunk_text(pages)

    print(f"Total chunks created: {len(chunks)}")
    print("First chunk sample:")
    print(chunks[0])

if __name__ == "__main__":
    main()
