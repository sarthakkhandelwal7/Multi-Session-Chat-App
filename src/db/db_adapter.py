from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

class DatabaseAdapter(ABC):    
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def execute_query(self, query, params=None):
        pass

    @abstractmethod
    @asynccontextmanager
    async def get_session(self, query_type: str) -> AsyncGenerator[Any, None]:
        pass