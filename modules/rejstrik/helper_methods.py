from tools.base import EntityDisplay
from maltego_trx.overlays import OverlayPosition, OverlayType


def edges_to_entities(item,data,edge):
    data.dateStart = edge.data.dateStart
    data.dateEnd = edge.data.dateEnd
    
    data.dateStartLogo = EntityDisplay(value=edge.data.dateStart, position=OverlayPosition.NORTH_WEST,
                                        overlay_type=OverlayType.TEXT)
    data.dateEndLogo = EntityDisplay(value=edge.data.dateEnd, position=OverlayPosition.SOUTH_WEST,
                                        overlay_type=OverlayType.TEXT)
    data.desc = EntityDisplay(value=edge.data.label, position=OverlayPosition.NORTH,
                                        overlay_type=OverlayType.TEXT)
        
    return data