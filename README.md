# Cryptographic Non-Repudiation "Truth Tracker"

An enterprise-grade document integrity and cryptographic signature validation tool designed to enforce non-repudiation and prevent unauthorized tampering in administrative, financial, and legal document processing.

## 1. Problem Statement & Regional Context

In many business sectors across East Africa and Tanzania, internal workflows, supplier procurement receipts, corporate approvals, and contractual invoices are regularly handled over unsecured channels using standard PDF attachments and unauthenticated email chains.

This introduces critical vulnerabilities:
* **Lack of Integrity**: Documents can be modified mid-transit or post-approval without leaving a trace.
* **Spoofing & Impersonation**: Attackers can easily spoof corporate email addresses to submit fraudulent invoices or unauthorized approvals.
* **Repudiation**: A party can sign a contract or authorize a significant fund transfer and later claim they never sent the approval.

The **Truth Tracker** eliminates these risks by applying an asymmetric Public Key Infrastructure (PKI) model to verify that documents are genuinely authentic and remain completely unaltered from the exact moment they were signed.



## 2. Cryptographic Architecture

The application relies on strong, industry-standard cryptographic primitives decoupled from system-wide libraries:

* **Hashing Engine**: Uses the **SHA-256** algorithm to compile file contents into a unique, one-way 32-byte (256-bit) digest block. File streams are managed in rigid 4KB memory chunks to keep system RAM utilization low and protect against resource starvation attacks.
* **Asymmetric Infrastructure**: Leverages the **RSA** algorithm with an enterprise-grade key size of **4096 bits** to defend against factoring attacks.
* **Padding Mechanism**: Employs **RSA-PSS (Probabilistic Signature Scheme)** alongside an internal Mask Generation Function (MGF1) backed by SHA-256. This introduces a randomized salt value that prevents dictionary attacks and makes signatures non-deterministic.

### System Workflow Block Diagram

###PHASE A: SIGNING WORKFLOW


[ Document ] ──(4KB Blocks)──> [ SHA-256 Engine ] ──> [ 32-Byte Hash ]
                                                            │
  ┌─────────────────────────────────────────────────────────┘
  ▼
[ RSA-PSS Padding ] ──(+ Randomized Salt)──> [ RSA Encryption ]
                                                    ▲
                                                    │
                                      [ 4096-bit Private Key ]
                                                    │
                                                    ▼
                                      [ 512-Byte Detached Signature ]
                                      (Saved as 'contract.txt.sig')


###PHASE B: VERIFICATION WORKFLOW


[ Received Document ] ───────────> [ SHA-256 Engine ] ───────────> [ New Hash ]
                                                                       │
                                                                 (Match Check)
                                                                       │
[ Received Signature ] ──> [ RSA Verification Engine ] ──> [ Decrypted Hash ]
                                  ▲
                                  │
                       [ Signer Public Key ]



## 3. Technology Stack

* **Language**: Python 3
* **Cryptographic Framework**: `cryptography` (Hazmat Primitives layer)
* **Version Control**: Git / GitHub
* **Environment**: Isolated Local Virtual Environments (`venv`)
* **Target OS Deployments**: Production-ready for Linux Enterprise Distributions (RHEL, Ubuntu Server)


## 4. Setup and Installation

### Prerequisites
Ensure your Linux machine has Python 3, pip, and Git configured.

### Step-by-Step Installation
1. Clone the project repository or open your local workspace directory.
2. Initialize and activate the isolated virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Upgrade the local package manager and install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```


## 5. Usage Instructions

The toolkit features a unified Command Line Interface (CLI) application (`truth_tracker.py`) alongside standalone testing utilities.

### Step 1: Generate Key Pairs
Generate your asymmetric 4096-bit RSA security keys:
```bash
python3 generate_keys.py
```
*Security Note: The script saves files directly to disk and changes file system permissions using `chmod 600` on `private_key.pem` to restrict local unauthorized read-access.*

### Step 2: Sign a Document
To cryptographically sign a document using your secret identity key:
```bash
python3 truth_tracker.py sign -f contract.txt -k private_key.pem
```
This generates a 512-byte signature file named `contract.txt.sig`.

### Step 3: Verify Signature and Document Integrity
To run an independent security check against a file and its signature:
```bash
python3 truth_tracker.py verify -f contract.txt -s contract.txt.sig -k public_key.pem
```


## 6. Security Testing & Tamper Detection Procedures

To validate system reliability under real attack vectors, execute the following audit test:

1. **Verify Original File**:
```bash
python3 truth_tracker.py verify -f contract.txt -s contract.txt.sig -k public_key.pem
# Output: VERIFICATION SUCCESSFUL
```
2. **Inject Unauthorized Document Modifications**:
Modify the file parameters (such as changing an amount string using a stream editor):
```bash
sed -i 's/APPROVED/DENIED/g' contract.txt
```
3. **Audit the Tampered File**:
```bash
python3 truth_tracker.py verify -f contract.txt -s contract.txt.sig -k public_key.pem
```
**System Response**:
```text
[-] VERIFICATION CRITICAL FAILURE: The signature is INVALID.
[-] Security Warning: The file has been modified, or the signature was forged.
```


## 7. Lessons Learned & Future Architectural Enhancements

* **Lessons Learned**: Parameter matching across cryptographic operations is absolute; signing configurations (padding types, hash block widths) must be strictly mirrored step-for-step during verification, or validation checks will reject the operation.
* **Future Security Roadmap**:
1. **Key Encapsulation**: Upgrade private key storage by applying AES-256 passphrase-based encryption to keys stored on disk.
2. **Hardware Abstraction**: Bridge the core interface logic with Hardware Security Modules (HSMs) or TPM chips via PKCS#11 wrappers.
3. **Public Registries**: Introduce certificate chain validation to link corporate identities with public keys using centralized X.509 authority frameworks.
