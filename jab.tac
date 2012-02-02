from ConfigParser import ConfigParser

from twisted.application import internet, service
from twisted.words.protocols.jabber.jid import JID
from twisted.web import server
from wokkel import client

from protocol import JabProtocol
from http import RootResource

config = ConfigParser()
config.read('jab.conf')

jid = JID(config.get("jab", "jid"))
password = config.get("jab", "password")

application = service.Application('XMPP client')

xmpp_client = client.XMPPClient(jid, password)
xmpp_client.setServiceParent(application)
#xmpp_client.logTraffic = True

jab = JabProtocol()
jab.setHandlerParent(xmpp_client)

jab_http = RootResource(xmpp_prot=jab)
site = server.Site(jab_http)
i = internet.TCPServer(8080, site)
i.setServiceParent(application)
