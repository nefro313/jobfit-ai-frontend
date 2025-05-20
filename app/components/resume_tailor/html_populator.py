
import json
from app.core.logger import get_logger
from typing import Dict, Any, Union


from app.schema.resume_data import ResumeData
from jinja2 import Environment, FileSystemLoader
import os

# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler("resume_processor.log"),
#         logging.StreamHandler()
#     ]
# )
logger = get_logger(__name__)


def populate_html_template(template_path: str, resume_data: Dict[str, Any]) -> str:
    """
    Populate HTML template with resume data
    
    Args:
        template_path: Path to the HTML template
        resume_data: Resume data dictionary
        
    Returns:
        Populated HTML string
    """
    try:
        # Create Jinja2 environment
        template_dir = os.path.dirname(template_path)
        template_file = os.path.basename(template_path)
        
        env = Environment(loader=FileSystemLoader(template_dir if template_dir else '.'))
        template = env.get_template(template_file)
        
        # Render the template with resume data
        return template.render(resume=resume_data)
    except Exception as e:
        logger.exception(f"Error populating HTML template: {str(e)}")
        raise

# def extract_resume_json(response: str) -> Optional[Dict[str, Any]]:
#     """
#     Extract JSON data from API response
    
#     Args:
#         response: API response string
        
#     Returns:
#         Extracted JSON data or None if extraction fails
#     """
#     try:
#         # If response is already a dictionary, return it directly
#         if isinstance(response, dict):
#             return response
        

        
#         # First, try to parse the entire response as JSON
#         try:
#             return json.loads(clean_response)
#         except json.JSONDecodeError:
#             pass
        
#         # Extract JSON content between ``` markers if not directly JSON
#         json_match = re.search(r'```json\n(.*?)```', clean_response, flags=re.DOTALL)
#         if json_match:
#             json_str = json_match.group(1).strip()
#             return json.loads(json_str)
        
#         logger.error("Could not extract JSON data from response")
#         return None
        
    # except Exception as e:
    #     logger.exception(f"Error extracting resume JSON: {str(e)}")
    #     return None

def process_resume_data(resume_input: Union[Dict[str, Any], str]) -> str:
    """
    Process resume data and generate HTML
    
    Args:
        resume_input: Resume data as dictionary or JSON string
        
    Returns:
        Populated HTML string
    """
    try:
        logger.info(f"Resume function started{resume_input}")
        # Parse string input to dict
        # if isinstance(resume_input, str):
        #     resume_json = json.loads(resume_input)
        #     return

        # Validate with Pydantic
        resume_data = ResumeData(**resume_input)
        logger.info("Resume data validated successfully")

        # Template path
        template_path = os.path.join(
            "data/resume_templates",
            "resume_templates.html"
        )

        # Render HTML
        populated_html = populate_html_template(template_path, resume_data.model_dump())

        # Save HTML (optional)
        output_path = os.path.join(
            os.path.dirname(template_path),
            "populated_resume.html"
        )

        with open(output_path, 'w') as f:
            f.write(populated_html)

        logger.info(f"Resume HTML generated successfully at {output_path}")
        return populated_html

    except Exception as e:
        logger.error(f"Error processing resume data: {e}")
        raise 