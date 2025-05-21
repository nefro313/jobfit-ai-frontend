
import os
# import tempfile
# from pathlib import Path
from app.core.logger import get_logger
from typing import Union, Optional
# from playwright.sync_api import sync_playwright



# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler("pdf_generator.log"),
#         logging.StreamHandler()
#     ]
# )
logger = get_logger(__name__)

def create_pdf_from_html( output_path: Optional[str] = None) -> Union[bytes, str]:
    """
    Convert HTML content to PDF using Playwright
    
    Args:
        html_content: HTML content as string
        output_path: Optional path to save the PDF file
        
    Returns:
        PDF as bytes if output_path is None, otherwise the path to the saved PDF
    """
    try:
        # Create temporary file for HTML
        # with tempfile.NamedTemporaryFile(suffix='.html', mode='w', delete=False) as tmp_html:
        #     tmp_html.write(html_content)
        #     html_path = tmp_html.name
        
        # logger.info(f"Created temporary HTML file at {html_path}")
        
        # Convert HTML to URI format
        # file_url = Path(html_path).as_uri()
        
        
        # Use Playwright to generate PDF
        # with sync_playwright() as p:
        #     browser = None
        #     try:
        #         browser = p.chromium.launch()
        #         page = browser.new_page()
                
        #         # Navigate to the HTML file
        #         logger.info(f"Navigating to HTML at {file_url}")
        #         page.goto(file_url)
                
        #         # Generate PDF
        #         logger.info(f"Generating PDF at {output_path}")
        #         page.pdf(path=output_path, format='A4')
        #     except Exception as e:
        #         logger.error({e})
                
        #     finally:
        #         if browser:
        #             browser.close()
        
        # # Clean up temporary HTML file
        # os.unlink(html_path)
        
        # If no output path was provided, read the PDF into memory and return as bytes

        with open(output_path, 'rb') as f:
            pdf_bytes = f.read()
            
            # Clean up temporary PDF file
            # os.unlink(output_path)
            
            return pdf_bytes
        
        # return output_path
        
    except Exception as e:
        logger.exception(f"Error generating PDF: {str(e)}")
        raise

# def create_pdf_from_html_file(output_path: Optional[str] = None) -> Union[bytes, str]:
#     """
#     Convert HTML file to PDF using Playwright
    
#     Args:
#         html_file_path: Path to HTML file
#         output_path: Optional path to save the PDF file
        
#     Returns:
#         PDF as bytes if output_path is None, otherwise the path to the saved PDF
#     """
#     try:
#         with open(html_file_path, 'r') as f:
#             html_content = f.read()
        
#         return create_pdf_from_html(html_content, output_path)
        
#     except Exception as e:
#         logger.exception(f"Error reading HTML file {html_file_path}: {str(e)}")
#         raise