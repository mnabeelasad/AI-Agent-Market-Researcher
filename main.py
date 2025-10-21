# # import os
# # from typing import List
# # from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# # from fastapi.responses import StreamingResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # from dotenv import load_dotenv
# # from pydantic import BaseModel
# # from agent import ReportAgent

# # # ... (App Initialization, CORS, and Agent Singleton remain the same) ...
# # load_dotenv()
# # app = FastAPI(
# #     title="AI Report Generation Agent API",
# #     description="API for generating reports from blueprints and answering questions about them.",
# #     version="1.0.0"
# # )

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # api_key = os.getenv("OPENAI_API_KEY")
# # if not api_key:
# #     raise RuntimeError("OPENAI_API_KEY not found in .env file")
# # report_agent = ReportAgent(openai_api_key=api_key)

# # class QueryRequest(BaseModel):
# #     question: str

# # @app.post("/generate-report/")
# # async def generate_report(
# #     user_prompt: str = Form(""),
# #     files: List[UploadFile] = File(...)
# # ):
# #     for file in files:
# #         if file.content_type != 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
# #             raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}. Please upload .docx files only.")

# #     try:
# #         return StreamingResponse(
# #             report_agent.stream_report_generation(files, user_prompt),
# #             media_type="text/event-stream"
# #         )
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# # # --- THIS ENDPOINT NOW RETURNS A STREAMING RESPONSE ---
# # @app.post("/query-report/")
# # async def query_report(request: QueryRequest):
# #     """
# #     Accepts a question and streams an answer based on the last generated report.
# #     """
# #     if not report_agent.report_context:
# #         raise HTTPException(status_code=400, detail="No report has been generated yet. Please generate a report first.")

# #     try:
# #         # Call the new streaming method in the agent
# #         return StreamingResponse(
# #             report_agent.stream_answer(request.question),
# #             media_type="text/event-stream"
# #         )
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"An error occurred during query: {str(e)}")

# # @app.get("/")
# # def read_root():
# #     return {"status": "ok", "message": "Welcome to the AI Report Agent API!"}

# import os
# import io
# from typing import List
# from fastapi import FastAPI, UploadFile, File, Form, HTTPException
# from fastapi.responses import StreamingResponse
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from pydantic import BaseModel
# from agent import ReportAgent
# from fpdf import FPDF
# from markdown_it import MarkdownIt

# # ... (App Initialization, CORS, and Agent Singleton remain the same) ...
# load_dotenv()
# app = FastAPI(
#     title="AI Report Generation Agent API",
#     description="API for generating reports from blueprints and answering questions about them.",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# api_key = os.getenv("OPENAI_API_KEY")
# if not api_key:
#     raise RuntimeError("OPENAI_API_KEY not found in .env file")
# report_agent = ReportAgent(openai_api_key=api_key)

# class QueryRequest(BaseModel):
#     question: str
    
# class PDFRequest(BaseModel):
#     markdown_text: str

# # ... (generate_report, query_report, and root endpoints remain the same) ...
# @app.post("/generate-report/")
# async def generate_report(
#     user_prompt: str = Form(""),
#     files: List[UploadFile] = File(...)
# ):
#     for file in files:
#         if file.content_type != 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
#             raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}. Please upload .docx files only.")
#     try:
#         return StreamingResponse(
#             report_agent.stream_report_generation(files, user_prompt),
#             media_type="text/event-stream"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @app.post("/query-report/")
# async def query_report(request: QueryRequest):
#     if not report_agent.report_context:
#         raise HTTPException(status_code=400, detail="No report has been generated yet. Please generate a report first.")
#     try:
#         return StreamingResponse(
#             report_agent.stream_answer(request.question),
#             media_type="text/event-stream"
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred during query: {str(e)}")

# @app.get("/")
# def read_root():
#     return {"status": "ok", "message": "Welcome to the AI Report Agent API!"}

# @app.post("/generate-pdf/")
# async def generate_pdf(request: PDFRequest):
#     """
#     Accepts Markdown text and returns a PDF file.
#     """
#     markdown_text = request.markdown_text
    
#     pdf = FPDF()
#     pdf.add_page()
#     # Add support for Unicode characters
#     pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
#     pdf.set_font("DejaVu", size=12)
    
#     md = MarkdownIt()
#     html_text = md.render(markdown_text)
    
#     # Very basic HTML to text conversion for the PDF
#     # This part can be improved for better styling
#     html_text = html_text.replace('<h1>', '').replace('</h1>', '\n')
#     html_text = html_text.replace('<h2>', '').replace('</h2>', '\n')
#     html_text = html_text.replace('<h3>', '').replace('</h3>', '\n')
#     html_text = html_text.replace('<h4>', '').replace('</h4>', '\n')
#     html_text = html_text.replace('<p>', '').replace('</p>', '\n')
#     html_text = html_text.replace('<ul>', '').replace('</ul>', '')
#     html_text = html_text.replace('<li>', '  • ').replace('</li>', '\n')
#     html_text = html_text.replace('<strong>', '').replace('</strong>', '')
#     html_text = html_text.replace('<em>', '').replace('</em>', '')
    
#     pdf.write(8, html_text)
    
#     # --- THIS IS THE CORRECTED LINE ---
#     # pdf.output() returns the PDF as a bytes object directly.
#     # The unnecessary .encode('latin-1') has been removed.
#     pdf_bytes = pdf.output()
    
#     return StreamingResponse(
#         io.BytesIO(pdf_bytes),
#         media_type="application/pdf",
#         headers={"Content-Disposition": "attachment; filename=generated_report.pdf"}
#     )

import os
import io
import re
from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from agent import ReportAgent
from fpdf import FPDF

# --- App Initialization & Setup ---
load_dotenv()
app = FastAPI(
    title="AI Report Generation Agent API",
    description="API for generating reports from blueprints and answering questions about them.",
    version="1.0.0"
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
api_key = os.getenv("OPENAI_API_KEY")
if not api_key: raise RuntimeError("OPENAI_API_KEY not found in .env file")
report_agent = ReportAgent(openai_api_key=api_key)

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    question: str
    
class PDFRequest(BaseModel):
    markdown_text: str

# --- THIS IS THE NEW, SMARTER PDF CLASS ---
class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, "Generated Market Report", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
        
    def draw_table(self, data):
        if not data:
            return
        
        self.set_font("DejaVu", "B", 10)
        self.set_fill_color(200, 220, 255)
        
        # Calculate optimal column widths
        col_widths = []
        for header_cell in data[0]:
            col_widths.append(self.get_string_width(header_cell) + 6)
        
        for row in data[1:]:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    width = self.get_string_width(cell) + 6
                    if width > col_widths[i]:
                        col_widths[i] = width
                else:
                    col_widths.append(self.get_string_width(cell) + 6) # Add new column width if row has more cells
        
        # Draw Header
        for i, header_text in enumerate(data[0]):
            self.cell(col_widths[i], 10, header_text, 1, 0, "C", 1)
        self.ln()

        # Draw Data
        self.set_font("DejaVu", "", 10)
        for row in data[1:]:
            for i, cell in enumerate(row):
                # Ensure we don't try to access an index that doesn't exist
                if i < len(col_widths):
                    self.cell(col_widths[i], 10, cell, 1)
            self.ln()
        self.ln(5) # Space after table

    # --- THIS IS THE NEW, REUSABLE FUNCTION TO HANDLE BOLDING ---
    def write_with_bold(self, text, size=11, height=8):
        # Split line by bold markers `**`
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                self.set_font("DejaVu", "B", size)
                self.write(height, part[2:-2])
            else:
                self.set_font("DejaVu", "", size)
                self.write(height, part)
        self.ln(height) # Move to the next line

    def write_markdown(self, text):
        lines = text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                self.ln(5)
                i += 1
                continue

            # Handle headings
            if line.startswith("# "):
                self.set_font("DejaVu", "B", 18)
                self.multi_cell(0, 10, line[2:].strip(), 0, "L")
                self.ln(4)
            elif line.startswith("## "):
                self.set_font("DejaVu", "B", 15)
                self.multi_cell(0, 9, line[3:].strip(), 0, "L")
                self.ln(3)
            elif line.startswith("### "):
                self.set_font("DejaVu", "B", 12)
                self.multi_cell(0, 8, line[4:].strip(), 0, "L")
                self.ln(2)
            # Handle tables
            elif line.startswith("|"):
                table_data = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    row_text = lines[i].strip()
                    if re.match(r'^[|: \-]+\|$', row_text): # Skip separator line like |:---|:---|
                        i += 1
                        continue
                    cells = [cell.strip() for cell in row_text.split('|')][1:-1]
                    table_data.append(cells)
                    i += 1
                self.draw_table(table_data)
                continue # Continue to next loop iteration
            # Handle bullet points
            elif line.startswith("* ") or line.startswith("- "):
                self.set_x(15) # Indent
                # Call the new function to handle bolding *within* bullets
                self.write_with_bold(f"• {line[2:].strip()}", size=11, height=8)
            # Handle regular text
            else:
                self.set_x(10) # Standard indent
                # Call the new function to handle bolding *within* paragraphs
                self.write_with_bold(line, size=11, height=8)
            i += 1

# --- API Endpoints ---
@app.post("/generate-report/")
async def generate_report(user_prompt: str = Form(""), files: List[UploadFile] = File(...)):
    for file in files:
        if file.content_type != 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}")
    combined_blueprint_text = ""
    for file in files:
        try:
            file_bytes = await file.read()
            text = report_agent._parse_docx(file_bytes)
            combined_blueprint_text += f"--- CONTENT FROM FILE: {file.filename} ---\n{text}\n\n"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file {file.filename}: {e}")
    try:
        return StreamingResponse(
            report_agent.stream_report_generation(combined_blueprint_text, user_prompt),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during generation: {str(e)}")

@app.post("/query-report/")
async def query_report(request: QueryRequest):
    if not report_agent.report_context:
        raise HTTPException(status_code=400, detail="No report generated yet.")
    try:
        return StreamingResponse(
            report_agent.stream_answer(request.question),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during query: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the AI Report Agent API!"}

@app.post("/generate-pdf/")
async def generate_pdf(request: PDFRequest):
    pdf = PDF()
    font_path = os.path.join("fonts", "DejaVuSans.ttf")
    if not os.path.exists(font_path):
        raise HTTPException(status_code=500, detail="Font file not found in backend/fonts/")
    try:
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.add_font("DejaVu", "B", font_path, uni=True)
        pdf.add_font("DejaVu", "I", font_path, uni=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load font: {e}")
        
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.write_markdown(request.markdown_text)
    pdf_bytes = pdf.output()
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=generated_report.pdf"}
    )