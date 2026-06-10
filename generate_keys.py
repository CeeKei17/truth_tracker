import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_key_pair():
    print("[*] Generating 4096-bit RSA key pair...")

    # Generate the private key with the secure exponent 65537
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

    # Extract the public key mathematically tied to the private key
    public_key = private_key.public_key()

    # Serialize and save the private key (Unencrypted for this beginner phase, but restricted via OS permissions)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open("private_key.pem", "wb") as priv_file:
        priv_file.write(private_pem)

    # Secure the private key file permissions immediately (Linux/macOS specific)
    os.chmod("private_key.pem", 0o600)
    print("[+] Private key saved to 'private_key.pem' with secure permissions (chmod 600).")

    # Serialize and save the public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open("public_key.pem", "wb") as pub_file:
        pub_file.write(public_pem)

    print("[+] Public key saved to 'public_key.pem'.")
    print("[*] Key generation completed successfully.")

if __name__ == "__main__":
    generate_key_pair()
