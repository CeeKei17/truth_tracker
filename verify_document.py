import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

def verify_file(file_path, public_key_path, signature_path):
    print(f"[*] Initiating validation audit for: '{file_path}'")

    # 1. Structural pre-flight checks
    if not os.path.exists(file_path):
        print(f"[-] Error: Target file '{file_path}' not found.")
        return False
    if not os.path.exists(public_key_path):
        print(f"[-] Error: Public key '{public_key_path}' not found.")
        return False
    if not os.path.exists(signature_path):
        print(f"[-] Error: Signature file '{signature_path}' not found.")
        return False

    try:
        # 2. Load the public key from the local PEM storage
        with open(public_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        # 3. Read the target document contents in binary mode
        with open(file_path, "rb") as target_file:
            document_data = target_file.read()

        # 4. Read the raw binary signature data
        with open(signature_path, "rb") as sig_file:
            signature_data = sig_file.read()

        print("[*] Recomputing SHA-256 hash and evaluating RSA-PSS signature...")

        # 5. Perform the cryptographic verification math
        public_key.verify(
            signature_data,
            document_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("[+] VERIFICATION SUCCESSFUL: Document integrity is intact.")
        print("[+] AUTHENTICITY CONFIRMED: Signature corresponds perfectly to the public key identity.")
        return True

    except InvalidSignature:
        print("[-] VERIFICATION CRITICAL FAILURE: The signature is INVALID.")
        print("[-] Security Warning: The file has been modified, or the signature was forged.")
        return False
    except Exception as e:
        print(f"[-] Critical system error during verification workflow: {e}")
        return False

if __name__ == "__main__":
    verify_file(
        file_path="contract.txt",
        public_key_path="public_key.pem",
        signature_path="contract.sig"
    )
