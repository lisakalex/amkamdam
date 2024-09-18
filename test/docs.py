from spire.doc import *
from spire.doc.common import *

# Create an object of the Document class
document = Document()
# Load a Markdown file
document.LoadFromFile("devops-learning-plan-chatgpt.md")

# Save the Markdown file to a Word DOCX file
document.SaveToFile("MdToDocx.docx", FileFormat.Docx)
# Save the Markdown file to a Word DOC file
document.SaveToFile("MdToDoc.doc", FileFormat.Doc)
document.Close()
