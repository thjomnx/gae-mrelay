gae-mrelay
==========

A mail relay application for Google App Engine.

'gae-mrelay' can be deployed under a specific name to a 
configured application within the Google App Engine PaaS 
platform.

Once running the application will receive incoming mail
and forward the mail to addresses configured in the mail
body. Lines like the following will trigger the
appropriate forwarding type:

FwdTo: someone@provider.net
FwdCc: someone@provider.net
FwdBcc: someone@provider.net

The lines are removed before the mail is forwarded.

Cheers :)
