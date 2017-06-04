import PyPDF2
from io import BytesIO


class PdfNotEqualException(Exception):
    """Two PDF are not the same for some reason."""


def compare_pdf(stream1, stream2):
    """Check if two pdf streams are the same.

    Pdf comparison is a bit tricky because there are very subtle things
    that can change. Here a I perform a soft comparison checking
    the main fields and the text in the pdfs is the same.
    This wont detect differences in layout

    Args:
        stream1(stream): pdf file stream to compare (e.g. BytesIO())
        stream2(stream): pdf file stream to compare (e.g. BytesIO())

    Return:
        (bool) True if the pdf have the same content, False otherwise
    """
    pdf1 = PyPDF2.PdfFileReader(stream1)
    pdf2 = PyPDF2.PdfFileReader(stream2)

    if len(pdf1.pages) != len(pdf2.pages):
        raise PdfNotEqualException('Number of pages differs.')

    document_infos = ['author', 'title', 'producer', 'subject', 'creator']

    for document_info in document_infos:
        info1 = getattr(pdf1.documentInfo, document_info)
        info2 = getattr(pdf2.documentInfo, document_info)
        if info1 != info2:
            raise PdfNotEqualException('Document info {} != {}.'.format(info1, info2))

    for pag1, pag2 in zip(pdf1.pages, pdf2.pages):
        text1 = pag1.extractText()
        text2 = pag2.extractText()
        if text1 != text2:
            raise PdfNotEqualException('Page content {} != {}.'.format(text1, text2))

    return True
