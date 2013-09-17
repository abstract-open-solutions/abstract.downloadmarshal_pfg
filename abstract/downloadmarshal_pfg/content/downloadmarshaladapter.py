"""Definition of the DownloadMarshalAdapter content type
"""

from Acquisition import aq_inner
from Acquisition import aq_parent
from AccessControl import ClassSecurityInfo

from zope.interface import implements
from zope.component import getMultiAdapter

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFPlone.interfaces import IPloneSiteRoot

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
            description=_(u'if none the container of the form folder will be used as resource'),
        ),
        searchable=0,
        required=0,
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
        resource = self._get_resource()
        marshal = getMultiAdapter((resource, request), IMarshal)
        url = marshal.generate_token_url(resource)
        request.response.redirect(url)

    def _get_resource(self):
        resource_path = self.getResource_path()
        if resource_path:
            resource = self.restrictedTraverse(resource_path)
        else:
            resource = self
            # get form folder
            while not resource.meta_type == 'FormFolder':
                resource = aq_parent(aq_inner(resource))
                if IPloneSiteRoot.providedBy(resource):
                    resource = None
                    break
            # get form folder parent
            if resource and resource.meta_type == 'FormFolder':
                resource = aq_parent(aq_inner(resource))
        if resource is None:
            raise LookupError("Cannot find any resource!")
        return resource

atapi.registerType(DownloadMarshalAdapter, PROJECTNAME)
