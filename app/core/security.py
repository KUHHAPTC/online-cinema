from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """Implementation of cryptographic algorithm blowfish."""

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Get salt+hash(password+salt)."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Compare user`s password with suggested password.

        Parameters
        ----------
        plain_password: str
            Password to check
        hashed_password: str
            Hashed password with salt

        Returns
        -------
        bool: True if password is correct and False otherwise

        """
        return pwd_context.verify(plain_password, hashed_password)
