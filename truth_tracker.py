import argparse
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

def load_private_key(path):
	if not os.path.exists(path):
		raise FileNotFoundError(f"Private key file not found at: {path}")
	with open(path, "rb") as key_file:
		return serialization.load_pem_private_key(key_file.read(), password=None)

def load_public_key(path):
	if not os.path.exists(path):
		raise FileNotFoundError(f"Public key file not found at: {path}")
	with open(path, "rb") as key_file:
		return serialization.load_pem_public_key(key_file.read())

def handle_sign(args):
	print(f"[*] Initiating signing routine for: '{args.file}'")
	try:
		private_key = load_private_key(args.key)

		with open(args.file, "rb") as target_file:
			document_data = target_file.read()

		signature = private_key.sign(
			document_data,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA256()),
				salt_length=padding.PSS.MAX_LENGTH
			),
			hashes.SHA256()
		)

		output_path = args.output if args.output else f"{args.file}.sig"
		with open(output_path, "wb") as sig_file:
			sig_file.write(signature)

		print(f"[+] SUCCESS: Digital signature written to '{output_path}'")

	except Exception as e:
		print(f"[-] Operational Failure during signing execution: {e}")

def handle_verify(args):
	print(f"[*] Initiating verification audit for: '{args.file}'")
	try:
		public_key = load_public_key(args.key)

		if not os.path.exists(args.signature):
			print(f"[-] Error: Signature target path not found: {args.signature}")
			return

		with open(args.file, "rb") as target_file:
			document_data = target_file.read()

		with open(args.signature, "rb") as sig_file:
			signature_data = sig_file.read()

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
		print("[+] AUTHENTICITY CONFIRMED: Valid signature matches public key identity.")

	except InvalidSignature:
		print("[-] VERIFICATION CRITICAL FAILURE: The signature is INVALID.")
		print("[-] Security Warning: The file has been modified, or the signature was forged.")
	except Exception as e:
		print(f"[-] Operational Failure during verification execution: {e}")

def main():
	parser = argparse.ArgumentParser(
		description="Truth Tracker: Cryptographic Non-Repudiation & Document Integrity Engine."
	)
	subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command executions")

	# Sign Sub-command parser
	sign_parser = subparsers.add_parser("sign", help="Sign a target file using a private key.")
	sign_parser.add_argument("-f", "--file", required=True, help="Path to the document file to sign.")
	sign_parser.add_argument("-k", "--key", default="private_key.pem", help="Path to private key (Default: private_key.pem).")
	sign_parser.add_argument("-o", "--output", help="Custom output path for the .sig file (Optional).")

	# Verify Sub-command parser
	verify_parser = subparsers.add_parser("verify", help="Verify a signature against a document and public key.")
	verify_parser.add_argument("-f", "--file", required=True, help="Path to the document file to verify.")
	verify_parser.add_argument("-s", "--signature", required=True, help="Path to the binary signature (.sig) file.")
	verify_parser.add_argument("-k", "--key", default="public_key.pem", help="Path to public key (Default: public_key.pem).")

	args = parser.parse_args()

	if args.command == "sign":
		handle_sign(args)
	elif args.command == "verify":
		handle_verify(args)

if __name__ == "__main__":
	main()
