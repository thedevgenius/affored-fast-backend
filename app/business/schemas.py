from pydantic import BaseModel, Field
class BusinessCreate(BaseModel):
    name: str = Field(..., description="Name of the business")
    slug: str = Field(..., description="Unique identifier for the business")
    description: str = Field(None, description="Description of the business")
    # address: str = Field(None, description="Address of the business")