from app.domain.exceptions.base import DomainException


class AlreadyExistsException(DomainException):
    def __init__(self, entity_name: str, field: str, value: str):
        super().__init__(f"{entity_name} with {field}='{value}' already exists.")
        self.entity_name = entity_name
        self.field = field
        self.value = value
