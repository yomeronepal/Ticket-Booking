from werkzeug.security import generate_password_hash, check_password_hash


class Password:
    def hash_password(self, password):
        hashed_password = generate_password_hash(password)
        return hashed_password

    def check_password(self, hashed_password, password):
        is_password_correct = check_password_hash(hashed_password, password)
        return is_password_correct
