from twisted.words.xish import domish
from twisted.web import resource
from twisted.python import log

class XmppResource(resource.Resource):
    def __init__(self, xmpp_prot):
        resource.Resource.__init__(self)
        self.xmpp_prot = xmpp_prot

class GithubResource(XmppResource):
    def render_GET(self, request):
        return "got it!"

    def render_POST(self, request):
        post_data = request.content.read()
        log.msg("GITHUB POST: %s" % post_data)

        reply = domish.Element((None, "message"))
        reply["to"] = "test2@chat.mynnx.com/Marks-MacBook-Air"
        reply["from"] = "test@chat.mynnx.com/twisted"
        reply["type"] = 'chat'
        reply.addElement("body", content=post_data)
        self.xmpp_prot.send(reply)
        return ''


class RootResource(XmppResource):
    def __init__(self, xmpp_prot):
        resource.Resource.__init__(self)
        self.putChild('github_hook', GithubResource(xmpp_prot))

