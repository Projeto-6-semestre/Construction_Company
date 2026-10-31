import logging
import sys

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    """Chamado explicitamente no startup (app/main.py) - nunca no import de modulo."""
    level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    # Bibliotecas de terceiros tendem a ser muito verbosas em DEBUG; deixa so o nosso codigo falante.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
