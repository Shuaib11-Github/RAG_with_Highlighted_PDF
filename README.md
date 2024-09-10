
# RAG_with_Highlighted_PDF

This project is a **Streamlit application** designed to highlight specific content within PDF files. The app parses the PDF and allows users to select and highlight portions of the content interactively.

## Features

- Load and view PDF content.
- Highlight specific text in the PDF.
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

\`\`\`bash
git clone <repository_url>
\`\`\`

### 2. Create a Conda Environment

Navigate to the project directory and create a new Conda environment using the following command:

\`\`\`bash
conda create --name pdf_highlighter_env python=3.8
\`\`\`

Activate the environment:

\`\`\`bash
conda activate pdf_highlighter_env
\`\`\`

### 3. Install Dependencies

After activating the environment, install the required dependencies using the \`requirements.txt\` file:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Set Up Environment Variables

Copy the example \`.env.example\` file to \`.env\` and configure any necessary environment variables:

\`\`\`bash
cp .env.example .env
\`\`\`

Edit the \`.env\` file to add your own environment settings (such as API keys or configurations). If no modifications are necessary, you can skip this step.

### 5. Run the Application

Start the Streamlit app using the following command:

\`\`\`bash
streamlit run app.py
\`\`\`

This command will launch the application in your browser, where you can interact with it to upload and highlight PDF content.

## Usage

1. After launching the app, upload a PDF file through the interface.
2. Use the app's tools to highlight specific sections of the PDF content.
3. The highlighted PDF content will be displayed for your review.

## Troubleshooting

- **Dependency Issues**: Ensure all dependencies listed in \`requirements.txt\` are installed correctly.
- **Environment Variables**: Double-check the values in the \`.env\` file if you're using any APIs or external services.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
