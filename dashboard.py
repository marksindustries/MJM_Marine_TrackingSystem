import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import tempfile
import os
# Assuming this is your custom module
from functions import ProcessDocuments, composeMail
from questionsList import QuestionsList  # Assuming this is your custom module


def main():
    st.set_page_config(page_title="MJM Marine",
                       page_icon=":bar_chart:", layout="wide")

    # Logo and title centered
    st.image("MJM_Marine/MJM-Marine-logo.jpg", width=300)
    st.title("MJM Marine Ltd")

    if "temp_file_path" not in st.session_state:
        st.session_state.temp_file_path = None

    if "answers" not in st.session_state:
        st.session_state.answers = {
            "Employer Liability": None,
            "Worker Compensation": None,
            "Public Liability": None,
            "General Liability": None,
            "Professional Liability": None,
            "Contractors All Risks Insurance": None,
        }
    if "mail_answer" not in st.session_state:
        st.session_state.mail_answer = None

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    with st.sidebar:
        st.title("Upload the Insurance Policy Document")
        uploaded_file = st.file_uploader("Choose a file", type="pdf")

        if uploaded_file is not None:
            # Delete the old temporary file if it exists
            if st.session_state.temp_file_path:
                try:
                    os.remove(st.session_state.temp_file_path)
                except OSError as e:
                    st.error(f"Error deleting old file: {e}")
                finally:
                    st.session_state.temp_file_path = None

            st.session_state.uploaded_file = uploaded_file

        view_pdf = st.button("View PDF")

        if view_pdf and st.session_state.uploaded_file is not None:
            pdf_viewer(st.session_state.uploaded_file.getvalue())

    tabs = st.tabs(["Employer Liability", "Worker Compensation", "Public Liability", "General Liability",
                    "Professional Liability", "Contractors All Risks Insurance"])

    tab_names = [
        "Employer Liability", "Worker Compensation", "Public Liability", "General Liability",
        "Professional Liability", "Contractors All Risks Insurance"
    ]

    questions_lists = [
        QuestionsList.EmployersLiabilityQuestions,
        QuestionsList.WorkersCompenstionsQuestions,
        QuestionsList.PublicOrProductLiabilityQuestions,
        QuestionsList.GeneralLiabilityQuestions,
        QuestionsList.ProfessinonalLiabilityQuestions,
        QuestionsList.ContractorsAllRiskInsuranceQuestions,
    ]

    for tab, tab_name, questions_list in zip(tabs, tab_names, questions_lists):
        with tab:
            st.header(tab_name)
            process_tab, email_tab = st.tabs(['process', 'email'])

            with process_tab:
                process = st.button("Process", key=tab_name)
                if st.session_state.uploaded_file is None:
                    st.warning("Please upload a PDF file")
                elif process:
                    try:
                        # Delete the old temporary file if it exists
                        if st.session_state.temp_file_path:
                            try:
                                os.remove(st.session_state.temp_file_path)
                            except OSError as e:
                                st.error(f"Error deleting old file: {e}")

                        # Create a new temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                            temp_file.write(
                                st.session_state.uploaded_file.getvalue())
                            st.session_state.temp_file_path = temp_file.name

                        # Process the document and store the answer in session state for the current tab
                        st.session_state.answers[tab_name] = ProcessDocuments(
                            st.session_state.temp_file_path,
                            questions_list=questions_list['questionsList'],
                            data=questions_list['data'],
                        )

                    except Exception as e:
                        st.error(f"An error occurred: {e}")

                # Display the answer if it exists in session state for the current tab
                if st.session_state.answers[tab_name] is not None:
                    st.dataframe(st.session_state.answers[tab_name])

            with email_tab:
                # Unique key for email button
                email_button_key = f"email_button_{tab_name}"
                mail = st.button("Compose a mail", key=email_button_key)
                if mail:
                    st.session_state.mail_answer = composeMail(
                        st.session_state.answers[tab_name])

                    st.text_area(
                        "Email To Sub Contractor",
                        st.session_state.mail_answer, height=600
                    )


if __name__ == "__main__":
    main()
