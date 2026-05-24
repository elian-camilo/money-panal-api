class AppBaseException(Exception):
    """Base exception for the application."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ResourceNotFoundException(AppBaseException):
    """Exception raised when a requested resource is not found."""
    pass


class ValidationException(AppBaseException):
    """Exception raised for validation errors."""
    pass


class UnauthorizedException(AppBaseException):
    """Exception raised for unauthorized access."""
    pass


class InvalidAmountException(AppBaseException):
    """Exception raised for invalid amount values."""
    pass