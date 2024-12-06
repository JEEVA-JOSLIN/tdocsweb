from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import magic

app = FastAPI()

# Enable CORS for all origins (you can restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with the frontend domain, e.g., ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize magic
magic_instance = magic.Magic()

# File upload and identification endpoint
@app.post("/identify")
async def identify_file(file: UploadFile = File(...)):
    try:
        # Read the file
        file_content = await file.read()

        # Identify the MIME type using libmagic
        mime_type = magic.from_buffer(file_content, mime=True)
        file_type = magic_instance.from_buffer(file_content)
        
        # Return result as JSON
        return {"file_type": file_type, "mime_type": mime_type}
    except Exception as e:
        return {"error": str(e)}
