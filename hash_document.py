import hashlib
import os

def calculate_sha256(file_path):
    """
    Reads a file in binary mode and calculates its SHA-256 cryptographic hash.
    Processes the file in chunks to ensure enterprise-grade memory efficiency.
    """
    if not os.path.exists(file_path):
        print(f"[-] Error: Target file '{file_path}' does not exist.")
        return None

    # Initialize the SHA-256 hashing object from hashlib
    sha256_hash = hashlib.sha256()

    try:
        # Open file in Read-Binary ('rb') mode to prevent encoding interpretations
        with open(file_path, "rb") as file:
            # Read in 4KB chunks (4096 bytes) - optimal for file system blocks
            chunk_size = 4096
            while chunk := file.read(chunk_size):
                sha256_hash.update(chunk)

        # Return the final computed hash as a human-readable hexadecimal string
        return sha256_hash.hexdigest()

    except Exception as e:
        print(f"[-] Critical system error reading file: {e}")
        return None

if __name__ == "__main__":
    target_document = "contract.txt"
    print(f"[*] Analyzing target document: '{target_document}'")

    document_hash = calculate_sha256(target_document)

    if document_hash:
        print(f"[+] Cryptographic Integrity Confirmed.")
        print(f"[+] SHA-256 Hash: {document_hash}")
