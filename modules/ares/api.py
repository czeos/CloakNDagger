from modules.ares.models import Company
from modules.ares import ares_logger
#TODO: add the real implementation
def serch_by_name(name: str):
    ares_logger.debug('logger test')
    return Company(name='success')