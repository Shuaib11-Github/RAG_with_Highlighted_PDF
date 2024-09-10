import pandas as pd  # Importing pandas for data manipulation.
import streamlit as st  # Importing Streamlit for creating web apps.
import os  # Importing the os library for interacting with the operating system.
import fitz  # Importing PyMuPDF for working with PDF files.
import pymupdf  # Importing PyMuPDF for working with PDF files.
import tempfile  # Importing tempfile to create temporary files.
from langchain.chains import RetrievalQA  # Importing RetrievalQA for question-answering capabilities.
import io  # Importing io for stream handling.
from streamlit_pdf_viewer import pdf_viewer  # Importing a component to display PDFs in Streamlit.
import json  # Importing json for parsing and generating JSON data.
from langchain_community.document_loaders import PyPDFLoader  # Importing a loader to read PDF files into the app.
from langchain_community.vectorstores import Qdrant  # Importing Qdrant for vector storage and retrieval.
from langchain_core.prompts import PromptTemplate  # Importing PromptTemplate for customizing language model prompts.
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # Importing OpenAI's tools for embeddings and chat functionalities.
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings # Importing Google Generative AI tools for embeddings and chat functionalities.
from langchain_text_splitters import CharacterTextSplitter  # Importing a tool to split text into character-based chunks.
from dotenv import load_dotenv  # Importing dotenv to load environment variables from a .env file.
import google.generativeai as genai # Importing Google Generative AI for text generation.

load_dotenv()  # Loading environment variables from a .env file.

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Configuring Google Generative AI with the API key.

st.set_page_config(page_title="📚 ChatPDF")  # Sets the configuration of the Streamlit page, including the title.

st.markdown("<h1 style='text-align: center;'>📚 ChatPDF</h1>", unsafe_allow_html=True)  # Displays a centered header on the page.
st.subheader("Upload a document to get started.")  # Adds a subheader prompting users to upload a document.

@st.cache_data  # Streamlit decorator to cache data for faster subsequent access.
def load_pdf(file):
    return pymupdf.open(stream=file, filetype="pdf")  # Uses PyMuPDF to open a PDF from a file-like object.

def extract_documents_from_file(file):
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # Creates a temporary file.
    temp_file.write(file)  # Writes the uploaded file data to the temporary file.
    temp_file.close()  # Closes the file to ensure data is written.

    loader = PyPDFLoader(temp_file.name)  # Initializes the PDF loader with the temporary file's path.
    documents = loader.load()  # Loads the document using the loader.
    return documents  # Returns the loaded documents.

def find_pages_with_excerpts(doc, excerpts):
    pages_with_excerpts = []  # Initializes a list to store pages containing excerpts.
    for page_num in range(len(doc)):  # Iterates over all pages in the document.
        page = doc.load_page(page_num)  # Loads each page.
        for excerpt in excerpts:  # Iterates over each excerpt to search for.
            text_instances = page.search_for(excerpt)  # Searches for the excerpt on the page.
            if text_instances:  # If the excerpt is found on the page,
                pages_with_excerpts.append(page_num)  # Add the page number to the list.
                break  # Stop searching on this page after finding the first instance.
    print("Pages with excerpts:", pages_with_excerpts)  # Debugging output
    return pages_with_excerpts if pages_with_excerpts else [0]  # Returns pages or [0] if none found.

@st.cache_resource  # Caches the resource to avoid re-loading on every call.
def get_llm():
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    # llm = ChatOpenAI(
    #     model="gpt-3.5-turbo",  # Specifies the model type.
    #     temperature=0,  # Sets the randomness to zero for consistent responses.
    #     openai_api_key=os.getenv("OPEN_AI_KEY")  # Fetches the API key from environment variables.
    # )
    return llm  # Returns the configured language model.

@st.cache_resource  # Caches the resource to enhance performance.
def get_embeddings():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # embeddings = OpenAIEmbeddings(
    #     model="text-embedding-ada-002",  # Specifies the embeddings model.
    #     openai_api_key=os.getenv("OPEN_AI_KEY")  # Uses the OpenAI API key from environment variables.
    # )
    return embeddings  # Returns the embeddings object.

@st.cache_resource  # Uses caching to optimize resource loading.
def get_qa(_documents):
    text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)  # Configures a text splitter.
    texts = text_splitter.split_documents(_documents)  # Splits documents into manageable texts.

    db = Qdrant.from_documents(
        documents=texts,  # The texts to index.
        embedding=get_embeddings(),  # Uses embeddings for indexing.
        collection_name="my_documents",  # Names the collection.
        location=":memory:",  # Stores the index in memory.
    )

    retriever = db.as_retriever(
        search_type="mmr",  # Uses Maximal Marginal Relevance for retrieving documents.
        search_kwargs={"k": 2, "lambda_mult": 0.8}  # Configures retrieval parameters.
    )

    qa = RetrievalQA.from_chain_type(
        get_llm(),  # Uses the language model for answering.
        chain_type="stuff",  # Generic placeholder for chain type.
        retriever=retriever,  # Sets the retriever.
        return_source_documents=True,  # Configures to return source documents.
        chain_type_kwargs={"prompt": CUSTOM_PROMPT},  # Uses a custom prompt for questions.
    )
    return qa  # Returns the configured QA system.

def get_highlight_info(doc, excerpts):
    annotations = []  # List to store annotations.
    for page_num in range(len(doc)):  # Iterates over each page.
        page = doc[page_num]  # Accesses the page.
        for excerpt in excerpts:  # Loops through each excerpt.
            text_instances = page.search_for(excerpt)  # Searches for text instances on the page.
            if text_instances:  # If found,
                for inst in text_instances:  # For each instance,
                    annotations.append(  # Append an annotation dict.
                        {
                            "page": page_num + 1,  # Page number (1-indexed).
                            "x": inst.x0,  # X-coordinate of the text box.
                            "y": inst.y0,  # Y-coordinate of the text box.
                            "width": inst.x1 - inst.x0,  # Width of the text box.
                            "height": inst.y1 - inst.y0,  # Height of the text box.
                            "color": "red",  # Annotation color.
                        }
                    )
    return annotations  # Return all annotations.

custom_template = """
    Context provided below contains the relevant information needed to answer the user question. Use the context effectively by referencing only pertinent details directly related to the query. If the information is insufficient or unclear, respond with an explanation of what additional information might be needed instead of speculating.

    Provided Context:
    {context}

    Question: {question}

    Example:
    {{
        "answer": "The process increases efficiency by 20%.",
        "sources": "According to the third paragraph, the implementation of the new system has enhanced operational efficiency by 20%."
    }}

    Please format your answer as a JSON object, ensuring that it is valid and can be parsed using json.loads() in Python. Structure your response in the following manner:
    {{
        "answer": "Your detailed answer here.",
        "sources": "Directly cite relevant sentences or paragraphs from the context that support your answer. Include ONLY RELEVANT TEXT. Do not add extraneous information or assumptions."
    }}
    
    The JSON must be a valid json format and can be read with json.loads() in
    Python. Answer:
"""

CUSTOM_PROMPT = PromptTemplate(
    template=custom_template,  # Sets the custom template.
    input_variables=["context", "question"]  # Defines input variables for the template.
)

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")  # Creates a file uploader in the UI.

if uploaded_file is not None:  # Checks if a file has been uploaded.
    file = uploaded_file.read()  # Reads the uploaded file.

    with st.spinner("Processing file..."):  # Shows a spinner during processing.
        documents = extract_documents_from_file(file)  # Extracts documents from the file.
        st.session_state.doc = fitz.open(stream=io.BytesIO(file), filetype="pdf")  # Opens the PDF for viewing.

    if documents:  # If documents were successfully extracted,
        qa = get_qa(documents)  # Sets up the QA system with the documents.
        if "chat_history" not in st.session_state:  # Initializes chat history if not already present.
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello! How can I assist you today? "}
            ]

        for msg in st.session_state.chat_history:  # Displays each message in the chat history.
            st.chat_message(msg["role"]).write(msg["content"])

        if user_input := st.chat_input("Your message"):  # Takes user input from a chat box.
            st.session_state.chat_history.append(
                {"role": "user", "content": user_input}
            )
            st.chat_message("user").write(user_input)

            with st.spinner("Generating response..."):  # Shows a spinner while generating a response.
                try:
                    result = qa.invoke({"query": user_input})  # Invokes the QA system with the user query.
                    parsed_result = json.loads(result['result'])  # Parses the resulting JSON.

                    answer = parsed_result['answer']  # Extracts the answer from the parsed result.
                    sources = parsed_result['sources']  # Extracts source references from the parsed result.

                    # sources = sources.split(". ") if pd.notna(sources) else []  # Splits sources into sentences if present.
                    if isinstance(sources, str):
                        sources = sources.split(". ") if pd.notna(sources) else []
                    elif isinstance(sources, list):
                        sources = [item for src in sources for item in src.split(". ") if pd.notna(src)] if sources else []


                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": answer}
                    )
                    st.chat_message("assistant").write(answer)

                    st.session_state.sources = sources  # Updates session state with new sources.
                    st.session_state.chat_occurred = True  # Sets a flag indicating chat interaction occurred.

                except json.JSONDecodeError:  # Handles errors in JSON parsing.
                    st.error(
                        "There was an error parsing the response. Please try again."
                    )

            if file and st.session_state.get("chat_occurred", False):  # If a file is present and a chat occurred,
                doc = st.session_state.doc  # Gets the document from session state.
                st.session_state.total_pages = len(doc)  # Stores the total number of pages in the document.
                if "current_page" not in st.session_state:  # Initializes the current page if not set.
                    st.session_state.current_page = 0

                pages_with_excerpts = find_pages_with_excerpts(doc, sources)  # Finds pages with excerpts.

                if "current_page" not in st.session_state:  # Initializes the current page if not set.
                    st.session_state.current_page = pages_with_excerpts[0]

                st.session_state.cleaned_sources = sources  # Saves cleaned sources to session.
                st.session_state.pages_with_excerpts = pages_with_excerpts  # Saves pages with excerpts to session.

                st.markdown("### PDF Preview with Highlighted Excerpts")  # Adds a section title.

                col1, col2, col3 = st.columns([1, 3, 1])  # Creates layout columns for navigation buttons.
                with col1:
                    if st.button("Previous Page") and st.session_state.current_page > 0:  # Previous page button.
                        st.session_state.current_page -= 1
                with col2:
                    st.write(
                        f"Page {st.session_state.current_page + 1} of {st.session_state.total_pages}"
                    )
                with col3:
                    if (
                        st.button("Next Page")
                        and st.session_state.current_page
                        < st.session_state.total_pages - 1
                    ):
                        st.session_state.current_page += 1

                annotations = get_highlight_info(doc, st.session_state.sources)  # Gets annotations for the PDF.

                if annotations:
                    first_page_with_excerpts = min(ann["page"] for ann in annotations)  # Finds the first page with annotations.
                else:
                    first_page_with_excerpts = st.session_state.current_page + 1

                pdf_viewer(
                    file,
                    width=700,
                    height=800,
                    annotations=annotations,
                    pages_to_render=[first_page_with_excerpts],  # Displays the PDF viewer with annotations.
                )

