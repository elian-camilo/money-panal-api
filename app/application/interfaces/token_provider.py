from abc import ABC, abstractmethod

class ITokenProvider(ABC):
    @abstractmethod
    def generate_token(self, payload: dict) -> str:
        """Generates a token from a payload dictionary."""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> dict | None:
        """Verifies a token and returns the payload if valid, None otherwise."""
        pass
