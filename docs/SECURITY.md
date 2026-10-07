# CyberGuard Security Architecture

## 1. Authentication & Role-Based Access Control (RBAC)
- **Password Storage**: Passwords are never stored in plaintext. Uses `bcrypt` with work factor 12.
- **JWT Cryptography**: Signed using HMAC-SHA256 (`HS256`) with a configurable secret key. Expiry defaults to 24 hours.
- **Server-Side Role Enforcement**: The user-supplied role in frontend requests is strictly ignored for authorization. Roles (`USER`, `ADMIN`, `CONSULTANT`) are verified against the validated database record retrieved from the JWT payload.

## 2. Input Validation & File Security
- **MIME & Magic Byte Verification**: Uploaded images are checked for valid PNG/JPG/WEBP headers to prevent executable code injection.
- **Path Traversal Protection**: Uploaded files are assigned cryptographic UUID filenames (`uuid4().hex`) and saved in isolated storage directories. Original client filenames are sanitized.
- **File Size Quotas**: Uploads are restricted to 10MB per image.

## 3. Threat Mitigation
- **SQL Injection**: Prevented using SQLAlchemy parameter binding and ORM models.
- **Cross-Site Scripting (XSS)**: All user inputs sanitized before rendering; JSON-encoded responses prevent script execution.
- **Rate Limiting**: Critical endpoints (`/auth/login`, `/analyze/image`) have rate limit thresholds to prevent credential stuffing and DoS attacks.
