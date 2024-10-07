# Aqui você pode definir quais módulos devem ser importados quando o pacote src é importado.
#from .config import SCRAPER_CONFIG, DATABASE_CONFIG, CSV_CONFIG
from .scraper import get_content
from .parser import load_from_db
