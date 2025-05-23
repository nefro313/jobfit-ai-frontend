# JobFit AI Suite

JobFit AI Suite is an AI-powered platform designed to assist users in optimizing their job application materials and interview preparation. It offers a suite of tools to analyze resumes, decode job postings, generate tailored resumes, and practice HR behavioral questions.

## Deployment

The application is live and can be accessed here:
[**JobFit AI Suite Deployment**](https://jobfitaii.streamlit.app)

## Core Features

*   **ATS Dashboard:** Analyzes your resume against a job description, providing feedback and optimization tips to improve its compatibility with Applicant Tracking Systems (ATS).
*   **HR Q&A Assistant:** Helps you prepare for interviews by generating AI-powered answers to common behavioral questions, allowing you to practice and refine your responses.
*   **Job Post Analyzer:** Decodes job postings to identify key skills, qualifications, and responsibilities, helping you understand what employers are looking for.
*   **Resume Tailor:** Creates targeted resumes by leveraging your existing resume, a specific job posting link, your GitHub profile (optional), and a personal statement to highlight the most relevant aspects of your experience.

## Built With

*   [Streamlit](https://streamlit.io/) - The primary framework for building the interactive web application.
*   [Pydantic](https://docs.pydantic.dev/) - Used for data validation and settings management.
*   [Jinja2](https://jinja.palletsprojects.com/) - Employed for templating, likely for generating parts of the UI or reports.
*   [Playwright](https://playwright.dev/) - Used for browser automation tasks, potentially for features involving web scraping or interaction (e.g., fetching job posting details or GitHub information for the Resume Tailor).

## Installation & Setup

To run the JobFit AI Suite locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/jobfit-ai-frontend.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd jobfit-ai-frontend
    ```
3.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Install Playwright and its browser dependencies:**
    Playwright is used for certain features. Ensure it's properly set up:
    ```bash
    playwright install
    playwright install-deps
    ```
    *Note: `playwright install-deps` is primarily for Linux. On Windows and macOS, `playwright install` usually handles browser binaries. If you encounter issues, refer to the [official Playwright documentation](https://playwright.dev/docs/browsers).*

6.  **Run the Streamlit application:**
    ```bash
    streamlit run Home_Dashboard.py
    ```

## Usage

Once the application is running:
1.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).
2.  The **Home Dashboard** will display the available tools.
3.  Click on any of the feature cards (e.g., "ATS Dashboard", "HR Q&A Assistant", "Job Post Analyzer", "Resume Tailor") to navigate to that specific tool.
4.  Follow the on-screen instructions for each tool, providing the required inputs (e.g., uploading your resume, pasting job descriptions, providing links).

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions for improvements or bug fixes.

## License

Distributed under the MIT License. See `LICENSE` for more information.
