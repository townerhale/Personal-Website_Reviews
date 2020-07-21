from passlib.context import CryptContext

# def main():
#         password = input("Enter a password: ")
#         hash = encrypt_password(password)
#
#         if check_encrypted_password(password, hash):
#             print("same")
#         else:
#              print("not")

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


# if __name__ == "__main__":
#     main()

def SQL_Test(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()
