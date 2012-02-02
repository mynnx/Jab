from twisted.words.xish import domish
from twisted.web import resource
from twisted.python import log
import json

class XmppResource(resource.Resource):
    def __init__(self, xmpp_prot):
        resource.Resource.__init__(self)
        self.xmpp_prot = xmpp_prot

class GithubResource(XmppResource):
    def render_GET(self, request):
        return "got it!"

    def render_POST(self, request):
        post_data = json.loads(request.args['payload'][0])
        log.msg("GITHUB POST: %s" % post_data)

        pusher = post_data['pusher']['name']
        repo = post_data['repository']['name']
        date = post_data['repository']['pushed_at']
        commits = [(c['message'], c['url']) for c in post_data['commits']]
        commit_links = '\n'.join(['"{0}"\n<{1}>'.format(*commit) for commit in commits])
        message = ("{pusher} just pushed to {repo} on "
                  "{date}\n\n{commits}").format(pusher=pusher,
                                                 repo=repo,
                                                 date=date,
                                                 commits=commit_links)

        log.msg("ABOUT TO SEND: %s" % message)

        reply = domish.Element((None, "message"))
        reply["to"] = "test2@chat.mynnx.com/Marks-MacBook-Air"
        reply["from"] = "test@chat.mynnx.com/twisted"
        reply["type"] = 'chat'
        reply.addElement("body", content=message)
        self.xmpp_prot.send(reply)
        return ''


class RootResource(XmppResource):
    def __init__(self, xmpp_prot):
        resource.Resource.__init__(self)
        self.putChild('github_hook', GithubResource(xmpp_prot))

