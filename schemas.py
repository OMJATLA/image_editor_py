from pydantic import BaseModel, validator
import base64

class ImageGenerationRequest(BaseModel):
    fast: bool
    bg_prompt: str
    refine_prompt: bool
    original_quality: bool
    num_results: int
    file: str  # base64 string

    @validator('file')
    def validate_base64(cls, v):
        # Remove data URI prefix if present
        if 'base64,' in v:
            v = v.split('base64,')[1]
        
        # Validate that it's a proper base64 string
        try:
            # Try decoding to check if it's valid base64
            base64.b64decode(v)
            return v  # Return the cleaned base64 string
        except Exception:
            raise ValueError('Invalid base64 string')