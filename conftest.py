import pytest

from src.services.agent_service import AgentService


@pytest.fixture(scope="session")
def service():
    """
    Instancia única de AgentService compartida por todos los tests
    de la sesión (evita recargar el modelo de embeddings en cada test).
    """
    return AgentService()