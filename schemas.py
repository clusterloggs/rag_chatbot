from pydantic import BaseModel
from typing import List, Optional

# NEW: Define a Pydantic model for an in-memory file.
# This matches the dictionary structure being sent by the UI.
class FilePayload(BaseModel):
    filename: str
    content: str

# UPDATED: Modify the main ingestion payload model.
class IngestPayload(BaseModel):
    texts: Optional[List[str]] = None
    # This now expects a list of FilePayload objects, not strings.
    files: Optional[List[FilePayload]] = None

# This model remains the same for the /query endpoint.
class QueryPayload(BaseModel):
    query: str