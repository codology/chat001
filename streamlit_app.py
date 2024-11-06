import streamlit as st
import kpdf, claude


def main():
    anthropic_key = st.text_input("Anthropic API Key", type="password")
    if not anthropic_key:
        st.info("Please add your Anthropic API key to continue.", icon="🗝️")
    if anthropic_key:
        uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")
        if uploaded_file is not None:
            reader = kpdf.PDFReader(uploaded_file)
            reader.extract_all_data()
            data = reader.get_data(reader.TEXT)
            # st.write(data)
            model = st.selectbox(
                "Model Name",
                (
                    claude.ClaudeModels.LEGACY_CLAUDE_2,
                    claude.ClaudeModels.SONNET_35_LATEST,
                    claude.ClaudeModels.SONNET_3,
                    claude.ClaudeModels.OPUS_3,
                    claude.ClaudeModels.HAIKU_3,
                ),
            )

            prompt = st.text_input("Ask Question from the doc")
            chunk = st.text_input("Limit search to this part of the document. (Leave blank for entire document)")

            if model and st.button("Search") and prompt:
                service = claude.ClaudeApi(model, anthropic_key)
                context = chunk if len(chunk) > 5 else None          
                service.query_document(data, prompt, context)
                resp = service.get_response()
                st.write(resp)


if __name__ == "__main__":
    main()
