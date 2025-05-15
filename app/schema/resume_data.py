from typing import Dict, Any, Optional, Union
from pydantic import BaseModel, EmailStr, Field #validator
from typing import List


class ContactInfo(BaseModel):
    address: Optional[str] = None
    phone: str
    email: EmailStr
    github: Optional[str] = None
    linkedin: Optional[str] = None
    
    # @validator('phone')
    # def validate_phone(cls, v):
    #     # Basic phone validation - could be enhanced based on requirements
    #     if not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', v):
    #         raise ValueError('Invalid phone number format')
    #     return v

class EducationItem(BaseModel):
    degree: str
    institution: str
    start_date: str
    end_date: str
    
    # @validator('start_date', 'end_date')
    # def validate_date(cls, v):
    #     # Basic date validation
    #     if v.lower() not in ['present', 'current']:
    #         if not re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$|^\d{4}$', v):
    #             if not re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\s+)\d{4}$', v):
    #                 raise ValueError('Invalid date format. Use MM/DD/YYYY, YYYY, or Mon YYYY')
    #     return v

class ExperienceItem(BaseModel):
    job_title: str
    company: str
    start_date: str
    end_date: str
    achievements: List[str]
    
    # @validator('start_date', 'end_date')
    # def validate_date(cls, v):
    #     # Same validator as in EducationItem
    #     if v.lower() not in ['present', 'current']:
    #         if not re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$|^\d{4}$', v):
    #             if not re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(\s+)\d{4}$', v):
    #                 raise ValueError('Invalid date format. Use MM/DD/YYYY, YYYY, or Mon YYYY')
    #     return v

class ResumeData(BaseModel):
    name: str
    about_me: str
    contact_info: ContactInfo
    education: List[EducationItem]
    experience: List[ExperienceItem]
    skills: List[str]
    soft_skills: List[str]