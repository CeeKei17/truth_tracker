import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

def sign_file(file_path, private_key_path, output_sig_path):
    print(f"[*] Initiating digital signature process for: '{file_path}'")

    # 1. Verification of assets
    if not os.path.exists(file_path):
        print(f"[-] Error: Target file '{file_path}' not found.")
        return False
    if not os.path.exists(private_key_path):
        print(f"[-] Error: Private key '{private_key_path}' not found. Run generate_keys.py first.")
        return False

    try:
        # 2. Load the private key from the local secure storage
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None # Unencrypted private key for this learning stage
            )

        # 3. Read the target document contents in binary mode
        with open(file_path, "rb") as target_file:
            document_data = target_file.read()

        print("[*] Computing hash and applying RSA-PSS private key signature...")

        # 4. Sign the data. The library handles hashing and encryption in one atomic step
        signature = private_key.sign(
            document_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # 5. Output the binary signature payload to a file
        with open(output_sig_path, "wb") as sig_file:
            sig_file.write(signature)

        print(f"[+] Digital signature successfully generated: '{output_sig_path}'")
        return True

    except Exception as e:
        print(f"[-] Critical Error during signing workflow: {e}")
        return False

if __name__ == "__main__":
    sign_file(
        file_path="contract.txt",
        private_key_path="private_key.pem",
        output_sig_path="contract.sig"
    )
