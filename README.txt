.. contents::

HOW TO
------
- Create a PloneFormGen form and add a DownloadMarshalAdapter
- Edit the Form Folder and fill the property 'Custom action' in the tab 'Overrides' with this value: "traverse_to:string:pfg_download_redirect"

When a user fill the form correctly he will be redirect to download resource url and it will be set a 'download-token' property in the request.

You can use this token to retrieve the url to download the resource.
Here an example for the resource view:

    >>> from abstract.downloadmarshal.adapters import URL_PATTERN
        ...
    >>> class View(BrowserView):
        ...
    >>>     def download_url(self):
    >>>         token = self.request.get('download-token')
    >>>         if token:
    >>>         return URL_PATTERN % {
    >>>                 'url': self.context.absolute_url(),
    >>>                 'fieldname': 'file',
    >>>                 'token_var': 'download-token',
    >>>                 'token': token
    >>>             }
        ...
    >>>     def get_metatag_refresh(self):
    >>>         url = self.download_url()
    >>>         if url:
    >>>             return "5; url=%s" % url

and its template:

    ...

    <metal:headslot fill-slot="head_slot">
        <meta http-equiv="refresh"
          tal:define="meta_content view/get_metatag_refresh"
          tal:condition="meta_content"
          tal:attributes="content meta_content" />
    </metal:headslot>

    ...
        <div class="container">
          <div class="row">
            <div class="span12">
              <div class="download-timer"
                  tal:define="download_url view/download_url"
                  tal:condition="download_url">
                <p>Your download will start in 5 seconds...
                  <br/>
                  Problems with the download?
                  Please use this
                    <a href="#"
                      tal:attributes="href download_url">direct link</a>.
                </p>
              </div>
            </div>
          </div>
        </div>

    ...
