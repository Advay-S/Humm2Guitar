from unstructured.partition.pdf import partition_pdf_or_image
from unstructured.partition.utils.constants import OCR_AGENT_TESSERACT



class DocumentParser:
    """
    Parses a PDF and returns clean text chunks ready for embedding.

    Usage:
        parser = DocumentParser()
        chunks = parser.parse("/path/to/file.pdf")
    """

    def __init__(self, strategy: str = "fast"):
        self.strategy = strategy

    def parse(self, filepath: str) -> list[str]:
        """
        Takes a path to a PDF file.
        Returns a list of clean text strings (chunks).
        """
        print(f"📄 Parsing: {filepath}")

        elements = partition_pdf_or_image(
            filename=filepath,
            strategy=self.strategy,
            detect_language_per_element=True,
            extract_images_in_pdf=False,
            starting_page_number=1,
            extract_forms=True,
            pdfminer_line_margin=None,
            pdfminer_char_margin=None,
            pdfminer_line_overlap=None,
            chunking_strategy="by_title",
            ocr_agent=OCR_AGENT_TESSERACT,
            infer_table_structure=True,
            table_ocr_agent=OCR_AGENT_TESSERACT
        )

        chunks = []
        for element in elements:
            if element.category in ["Header", "Footer"]:
                continue

            content = element.metadata.text_as_html if element.category == "Table" else element.text

            if content and content.strip():
                chunks.append(content)

        print(f"✅ Extracted {len(chunks)} chunks from {filepath}")
        return chunks
 
