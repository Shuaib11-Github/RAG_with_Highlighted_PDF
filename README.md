# RAG_with_Highlighted_PDF

Highlight PDF Content Streamlit App
This project is a Streamlit application designed to highlight specific content within PDF files. The app parses the PDF and allows users to select and highlight portions of the content interactively.

Features
Load and view PDF content.
Highlight specific text in the PDF.
Interactive user interface with Streamlit.

Project Structure
.env: Environment variables for sensitive information like API keys.
app.py: The main application file containing the Streamlit app logic.
requirements.txt: List of Python dependencies required for the project.

Requirements
Ensure you have the following installed:
Python 3.8+
pip (Python package manager)

Setup Instructions
1. Clone the Repository
If the project is on a GitHub repository, clone the repository using:

    `git clone <repository_url>`

2. Install Dependencies
Navigate to the project directory and install the required dependencies using pip:

    `pip install -r requirements.txt`

3. Set Up Environment Variables
Copy the example .env.example file to .env and configure any necessary environment variables.

    `.env`
Edit the .env file to add your own environment settings (such as API keys or configurations). If no modifications are necessary, you can skip this step.

4. Run the Application
Start the Streamlit app using the following command:

    `streamlit run app.py`

This command will launch the application in your browser, where you can interact with it to upload and highlight PDF content.

Usage
After launching the app, the interface will allow you to upload a PDF.
Use the tools in the app to highlight the specific sections of the PDF content.
The highlighted PDF content will be displayed for your review.

Troubleshooting
Dependency Issues: Ensure all dependencies listed in requirements.txt are installed correctly.
Environment Variables: Double-check the values in the .env file if you're using any APIs or external services.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
