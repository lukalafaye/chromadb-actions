import os 
from chromadb.config import Settings
import chromadb 

def connect_to_chromadb():
    """Connects to Chroma DB server already running..."""

    chroma_client_auth_credentials = os.getenv("CHROMA_CLIENT_AUTHN_CREDENTIALS")
    chroma_client_auth_provider = os.getenv("CHROMA_CLIENT_AUTHN_PROVIDER")

    # Debug print statements
    print("CHROMA_CLIENT_AUTHN_CREDENTIALS:", chroma_client_auth_credentials)
    print("CHROMA_CLIENT_AUTHN_PROVIDER:", chroma_client_auth_provider)

    # Ensure that the credentials and provider are not None
    if not chroma_client_auth_credentials or not chroma_client_auth_provider:
        raise ValueError("Authentication credentials or provider are missing.")

    # Initialize the client with settings
    settings = Settings(
        chroma_client_auth_provider=chroma_client_auth_provider,
        chroma_client_auth_credentials=chroma_client_auth_credentials
    )

    client = chromadb.HttpClient(settings=settings)

    return client
