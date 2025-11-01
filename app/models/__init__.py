
from datetime import datetime, date

def snake_to_camel(snake_str: str):
    parts = snake_str.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

class BaseJsonSerializable:
    
    def to_json(self):
        
        return {
            snake_to_camel(column.name): (
                getattr(self, column.name).isoformat()
                if isinstance(getattr(self, column.name), (datetime, date)) and getattr(self, column.name)
                else getattr(self, column.name)
            )
            for column in self.__table__.columns
        }

