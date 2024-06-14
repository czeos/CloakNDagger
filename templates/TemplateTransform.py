from maltego_trx.overlays import OverlayPosition, OverlayType
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg

from extensions import registry
from settings import hunchly_transformset

#
# @registry.register_transform(
#     display_name="<set transfor name>",
#     input_entity='< set input entity>',
#     description="<trnsform description>",
#     output_entities=['<output entities>'],
#     transform_set= '<trnsformtion settiong>'
#
# )
# class TemplateTransform(DiscoverableTransform):
#     """
#     Programers documentation
#     NOTE: Name of the class hve to be sme
#     """
#
#     @classmethod
#     def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
#         pass
#
#
