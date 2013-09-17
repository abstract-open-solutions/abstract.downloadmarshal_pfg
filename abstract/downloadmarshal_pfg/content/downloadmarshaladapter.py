"""Definition of the DownloadMarshalAdapter content type
"""

from AccessControl import ClassSecurityInfo

from zope.interface import implements
from zope.component import getMultiAdapter

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from Products.PloneFormGen.content.actionAdapter import \
    FormActionAdapter, FormAdapterSchema

from abstract.downloadmarshal.interfaces import IMarshal

from abstract.downloadmarshal_pfg.interfaces import IDownloadMarshalAdapter
from abstract.downloadmarshal_pfg.config import PROJECTNAME
from abstract.downloadmarshal_pfg import _


DownloadMarshalAdapterSchema = FormAdapterSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'resource_path',
        widget=atapi.StringWidget(
            label=_(u'path to download resource'),
            # description=_(u''),
        ),
        searchable=0,
        required=1,
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

DownloadMarshalAdapterSchema['title'].storage = atapi.AnnotationStorage()
DownloadMarshalAdapterSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(DownloadMarshalAdapterSchema, moveDiscussion=False)


class DownloadMarshalAdapter(FormActionAdapter):
    """Description of the Example Type"""
    implements(IDownloadMarshalAdapter)

    portal_type = meta_type = "DownloadMarshalAdapter"
    schema = DownloadMarshalAdapterSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    security = ClassSecurityInfo()

    security.declarePrivate('onSuccess')
    def onSuccess(self, fields, REQUEST=None):
        request = REQUEST or self.REQUEST

        resource_path = self.getResource_path()
        resource = self.restrictedTraverse(resource_path)
        marshal = getMultiAdapter((resource, request), IMarshal)
        url = marshal.generate_token_url(resource)
        print url


atapi.registerType(DownloadMarshalAdapter, PROJECTNAME)
