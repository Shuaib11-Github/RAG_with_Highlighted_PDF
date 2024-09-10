
# RAG_with_Highlighted_PDF

This project is a **Streamlit application** designed to chat with specific content within PDF files. The app parses the PDF and allows users to ask questions or engage in a conversation about the PDF content interactively.

## Features

- Load and view PDF content.
- Chat with the PDF to ask questions or get insights based on the content.
- Interactive user interface built with Streamlit.

## Project Structure

- **`.env`**: Environment variables for sensitive information like API keys.
- **`app.py`**: The main application file containing the Streamlit app logic.
- **`requirements.txt`**: List of Python dependencies required for the project.

## Requirements

Ensure you have the following installed:

- **Python 3.8+**
- **Conda** (Package and environment manager)

## Setup Instructions

### 1. Clone the Repository

If the project is on a GitHub repository, clone the repository using the following command:

`git clone <repository_url>`

### 2. Create a Conda Environment

Navigate to the project directory and create a new Conda environment using the following command:

`conda create --name pdf_highlighter_env python=3.8`

Activate the environment:

`conda activate pdf_highlighter_env`

### 3. Install Dependencies

After activating the environment, install the required dependencies using the \`requirements.txt\` file:

`pip install -r requirements.txt`

### 4. Set Up Environment Variables

Create a \`.env\` and configure any necessary environment variables:

`.env`

Edit the \`.env\` file to add your own environment settings (such as API keys or configurations). If no modifications are necessary, you can skip this step.

### 5. Run the Application

Start the Streamlit app using the following command:

`streamlit run app.py`

This command will launch the application in your browser, where you can interact with it to upload and highlight PDF content.

## Usage

1. Upload a PDF: After launching the app, the interface will prompt you to upload a PDF file.
2. Ask Questions: In the text input box, you can ask questions about the PDF content. For example, "What is the main idea of the document?"
3. Answer Generation: The app processes your question using the Google Generative AI or Langchain model, extracts the relevant text from the PDF, and displays the answer along with the source.
4. Highlighted Sections: The app will highlight the portions of the PDF that are relevant to the query using red-colored annotations, so the user can easily see where the answer is coming from.
5. Interactive Chat: You can continue to ask follow-up questions about the PDF, and the app will provide additional answers, continually highlighting relevant sections.

## Troubleshooting

- Dependency Issues: Ensure all dependencies listed in requirements.txt are installed correctly.
- Environment Variables: Ensure that the values in the .env file are correct, especially if you're using external services or APIs for PDF processing.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
