import importlib
import logging
import pkgutil
from pathlib import Path

logger = logging.getLogger(__name__)


def import_entities():
    base_path = Path(__file__).resolve().parent.parent.parent / "modules"
    package = "app.modules"

    for _, module_name, _ in pkgutil.iter_modules([str(base_path)]):
        entities_path = f"{package}.{module_name}.domain.entities"
        try:
            importlib.import_module(entities_path)
            logger.debug(f"Imported entities from {entities_path}")
        except ModuleNotFoundError:
            continue
