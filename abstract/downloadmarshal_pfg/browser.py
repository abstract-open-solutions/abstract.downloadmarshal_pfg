from zope.publisher.browser import BrowserPage
from Products.statusmessages.interfaces import IStatusMessage

from abstract.downloadmarshal.browser.download import ERROR_MESSAGE
from abstract.downloadmarshal_pfg import messageFactory as _


class DownloadRedirect(BrowserPage):

    def __call__(self):
        download_data = self.request.get('download_data')
        if not download_data:
            IStatusMessage(self.request).addStatusMessage(
                ERROR_MESSAGE,
                type="error"
            )
            url = self.context.absolute_url()

        else:
            url = '%(url)s?%(token_var)s=%(token)s' % download_data
        self.request.response.redirect(url)
