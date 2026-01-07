from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from cryptography.hazmat.primitives import serialization

# load & DER-encode the .p8 private key
with open("snowflake_key.p8", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(), password=None
    )

pkb = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

# create engine
engine = create_engine(
    URL(
        account="YOUR_ACCOUNT",
        user="YOUR_USER",
        database="YOUR_DATABASE",
        schema="YOUR_SCHEMA",
    ),
    connect_args={
        "private_key": pkb,
        "warehouse": "YOUR_WAREHOUSE",
        "role": "YOUR_ROLE",
    },
)

# use the engine
with engine.connect() as conn:
    result = conn.execute("SELECT CURRENT_TIMESTAMP;")
    print(result.fetchone())
