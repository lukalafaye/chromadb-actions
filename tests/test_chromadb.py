import pytest

# import pandas as pd
import subprocess
import os 
import time

from chroma.launch import connect_to_chromadb

@pytest.fixture(scope="module")
def setup_docker_container():
    # Export environment variables
    os.environ['CHROMA_CLIENT_AUTHN_CREDENTIALS'] = os.getenv('CHROMA_CLIENT_AUTHN_CREDENTIALS')
    os.environ['CHROMA_CLIENT_AUTHN_PROVIDER'] = os.getenv('CHROMA_CLIENT_AUTHN_PROVIDER')
    os.environ['CHROMA_AUTH_TOKEN_TRANSPORT_HEADER'] = 'Authorization'

    print(os.getenv('CHROMA_CLIENT_AUTHN_CREDENTIALS'), os.getenv('CHROMA_CLIENT_AUTHN_PROVIDER'), os.getenv('CHROMA_AUTH_TOKEN_TRANSPORT_HEADER'))

    # Check if the container is already running
    container_name = "chromadb-chroma"
    result = subprocess.run(
        ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )

    print('result', result)

    if container_name in result.stdout:
        print(f"The container {container_name} is already running.\n")
    else:
        print(f"The container {container_name} is not running. Starting it now...\n")

        # Run the Docker container with the specified configurations
        try:
            subprocess.run([
                "docker", "run", "-d", "--rm",
                "-e", f"CHROMA_SERVER_AUTHN_CREDENTIALS={os.getenv('CHROMA_SERVER_AUTHN_CREDENTIALS')}",
                "-e", f"CHROMA_SERVER_AUTHN_PROVIDER={os.getenv('CHROMA_SERVER_AUTHN_PROVIDER')}",
                "-e", f"CHROMA_AUTH_TOKEN_TRANSPORT_HEADER={os.getenv('CHROMA_AUTH_TOKEN_TRANSPORT_HEADER')}",
                "-p", "8000:8000",
                "-v", "./chroma:/chroma/chroma",
                "--name", container_name,
                "chromadb/chroma:latest"
            ], check=True)
            print(f"Successfully started {container_name}.\n")
            time.sleep(70)

        except subprocess.CalledProcessError:
            print(f"Failed to start {container_name}.\n")
            pytest.fail(f"Failed to start {container_name}!", pytrace=False)

    yield

    subprocess.run(["docker", "stop", "chromadb-chroma"])
    subprocess.run(["docker", "rm", "chromadb-chroma"])

@pytest.mark.usefixtures("setup_docker_container")
def test_connect_to_chromadb():
    client = connect_to_chromadb()

    # Add additional checks if needed, e.g., verifying client connection
    assert client is not None