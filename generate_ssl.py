import datetime

from cryptography import x509 #used to create and manage SSL/TLS certificates.
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa #Imports RSA functionality, used here to generate a public-private key pair.
from cryptography.x509.oid import NameOID  #object identifiers, Imports predefined OID constants for certificate fields like country, state, common name, etc.

# Generate private key
key = rsa.generate_private_key(
    public_exponent=65537, # this is a param
    key_size=2048
)

# Create self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Karnataka"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Bangalore"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CN Mini Project"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

cert = x509.CertificateBuilder().subject_name(
    subject  # who owns the certificate
).issuer_name(
    issuer # who signed it
).public_key(
    key.public_key()  #This is how clients encrypt data, sever uses private key to decrypt
).serial_number(
    x509.random_serial_number()  #Unique ID 
).not_valid_before(
    datetime.datetime.now(datetime.timezone.utc)
).not_valid_after(
    datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
).sign(key, hashes.SHA256())

# Save key
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()
    ))

# Save certificate
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("SSL certificate generated: cert.pem and key.pem")