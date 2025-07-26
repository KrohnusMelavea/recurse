from uuid import UUID

def parse_nullable_guid(id: str) -> UUID:
 return UUID(hex=id) if id is not None else None