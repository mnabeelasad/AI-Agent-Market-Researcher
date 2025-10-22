# import streamlit as st
# import requests

# # ... (Page Config, Backend URL, and Session State remain the same) ...
# st.set_page_config(
#     page_title="AI Report Agent",
#     page_icon="🤖",
#     layout="wide"
# )

# BACKEND_URL = "http://127.0.0.1:8000"

# if "report_generated" not in st.session_state:
#     st.session_state.report_generated = False
# if "report_content" not in st.session_state:
#     st.session_state.report_content = ""
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# st.title("📄 AI Report Generator & Q&A Agent")
# st.markdown("Upload one or more `.docx` blueprints to generate a report, then ask questions about it.")

# # ... (Sidebar for report generation remains the same) ...
# with st.sidebar:
#     st.header("1. Generate Report")
#     uploaded_files = st.file_uploader(
#         "Upload your .docx blueprint(s)",
#         type="docx",
#         key="docx_uploader",
#         accept_multiple_files=True
#     )
#     user_prompt = st.text_area(
#         "Optional: Add specific instructions (leave empty for auto-prompt)", height=100
#     )

#     if st.button("Generate Report", type="primary", disabled=not uploaded_files):
#         with st.status("Generating your report...", expanded=True) as status:
#             st.write("Sending blueprint(s) to the backend...")

#             files_payload = []
#             for file_obj in uploaded_files:
#                 files_payload.append(
#                     ('files', (file_obj.name, file_obj.getvalue(), file_obj.type))
#                 )

#             data = {'user_prompt': user_prompt}

#             try:
#                 response = requests.post(
#                     f"{BACKEND_URL}/generate-report/",
#                     files=files_payload,
#                     data=data,
#                     stream=True
#                 )
#                 response.raise_for_status()

#                 report_placeholder = st.empty()
#                 full_response = ""

#                 status.update(label="Streaming report from AI agent...", state="running")
#                 for chunk in response.iter_content(chunk_size=None):
#                     if chunk:
#                         full_response += chunk.decode('utf-8')
#                         report_placeholder.markdown(full_response + "▌")

#                 report_placeholder.markdown(full_response)

#                 st.session_state.report_content = full_response
#                 st.session_state.report_generated = True
#                 st.session_state.messages = []
#                 status.update(label="Report generation complete!", state="complete")

#             except requests.exceptions.RequestException as e:
#                 st.error(f"Failed to connect to backend: {e}")
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")

# col1, col2 = st.columns(2)

# with col1:
#     st.header("Generated Report")
#     if st.session_state.report_content:
#         st.markdown(st.session_state.report_content)
#     else:
#         st.info("Your generated report will appear here.")

# with col2:
#     st.header("Ask Questions About the Report")

#     if not st.session_state.report_generated:
#         st.info("Generate a report first to enable the Q&A feature.")
#     else:
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         # --- THIS CHAT INPUT LOGIC IS NOW UPDATED FOR STREAMING ---
#         if prompt := st.chat_input("What is this report about?"):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             with st.chat_message("assistant"):
#                 # Define a generator function that yields chunks from the backend
#                 def stream_chat_response():
#                     try:
#                         payload = {"question": prompt}
#                         with requests.post(f"{BACKEND_URL}/query-report/", json=payload, stream=True) as response:
#                             response.raise_for_status()
#                             for chunk in response.iter_content(chunk_size=None):
#                                 if chunk:
#                                     yield chunk.decode('utf-8')
#                     except requests.exceptions.RequestException as e:
#                         yield f"Error connecting to backend: {e}"
                
#                 # Use st.write_stream to display the streaming content
#                 # This will automatically display the chunks and return the full response at the end
#                 full_response = st.write_stream(stream_chat_response)
#                 st.session_state.messages.append({"role": "assistant", "content": full_response})

import streamlit as st
import requests

# ... (Page Config, Backend URL, and Session State remain the same) ...
st.set_page_config(
    page_title="AI Report Agent",
    page_icon="🤖",
    layout="wide"
)

# BACKEND_URL = "BACKEND_URL = https://ai-agent-backend-8z7l.onrender.com"
# This is the correct way
BACKEND_URL = "https://ai-agent-backend-8z7l.onrender.com"


if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
if "report_content" not in st.session_state:
    st.session_state.report_content = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📄 AI Report Generator & Q&A Agent")
st.markdown("Upload one or more `.docx` blueprints to generate a report, then ask questions about it.")

# ... (Sidebar for report generation remains the same) ...
with st.sidebar:
    st.header("1. Generate Report")
    uploaded_files = st.file_uploader(
        "Upload your .docx blueprint(s)",
        type="docx",
        key="docx_uploader",
        accept_multiple_files=True
    )
    user_prompt = st.text_area(
        "Optional: Add specific instructions (leave empty for auto-prompt)", height=100
    )

    if st.button("Generate Report", type="primary", disabled=not uploaded_files):
        with st.status("Generating your report...", expanded=True) as status:
            st.write("Sending blueprint(s) to the backend...")

            files_payload = []
            for file_obj in uploaded_files:
                files_payload.append(
                    ('files', (file_obj.name, file_obj.getvalue(), file_obj.type))
                )

            data = {'user_prompt': user_prompt}

            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate-report/",
                    files=files_payload,
                    data=data,
                    stream=True
                )
                response.raise_for_status()

                report_placeholder = st.empty()
                full_response = ""

                status.update(label="Analyzing blueprint and streaming report...", state="running")
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        full_response += chunk.decode('utf-8')
                        report_placeholder.markdown(full_response + "▌")

                report_placeholder.markdown(full_response)

                st.session_state.report_content = full_response
                st.session_state.report_generated = True
                st.session_state.messages = []
                status.update(label="Report generation complete!", state="complete")

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Main Content Area ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Generated Report")
    if st.session_state.report_content:
        # Create two columns for the download buttons
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            st.download_button(
                label="⬇️ Download as Markdown",
                data=st.session_state.report_content,
                file_name="generated_report.md",
                mime="text/markdown",
            )
        
        with btn_col2:
            # --- ADD PDF DOWNLOAD LOGIC ---
            if st.button("📄 Download as PDF"):
                with st.spinner("Generating PDF..."):
                    try:
                        payload = {"markdown_text": st.session_state.report_content}
                        response = requests.post(f"{BACKEND_URL}/generate-pdf/", json=payload)
                        response.raise_for_status()
                        
                        # Use a second download button to present the received PDF
                        st.download_button(
                            label="Click to Download PDF",
                            data=response.content,
                            file_name="generated_report.pdf",
                            mime="application/pdf"
                        )
                        st.success("PDF is ready for download!")

                    except requests.exceptions.RequestException as e:
                        st.error(f"Failed to generate PDF: {e}")
        
        st.markdown("---")
        st.markdown(st.session_state.report_content)
    else:
        st.info("Your generated report will appear here.")

# ... (Chat column remains the same) ...
with col2:
    st.header("Ask Questions About the Report")

    if not st.session_state.report_generated:
        st.info("Generate a report first to enable the Q&A feature.")
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What is this report about?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                def stream_chat_response():
                    try:
                        payload = {"question": prompt}
                        with requests.post(f"{BACKEND_URL}/query-report/", json=payload, stream=True) as response:
                            response.raise_for_status()
                            for chunk in response.iter_content(chunk_size=None):
                                if chunk:
                                    yield chunk.decode('utf-8')
                    except requests.exceptions.RequestException as e:
                        yield f"Error connecting to backend: {e}"
                
                full_response = st.write_stream(stream_chat_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})