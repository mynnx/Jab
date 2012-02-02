from wokkel.xmppim import MessageProtocol, PresenceClientProtocol
from twisted.words.protocols.jabber.jid import JID
from twisted.words.xish import domish
from twisted.python import log


class JabProtocol(MessageProtocol, PresenceClientProtocol):
    def __init__(self):
        super(JabProtocol, self).__init__()

    def connectionMade(self):
        log.msg("Connected!")
        self.available(statuses={None: "just chillin' in the reactor"})

    def connectionLost(self, reason):
        print "Disconnected!"

    def onMessage(self, msg):
        if msg["type"] == 'chat' and getattr(msg, "body", False):
            from_jid = JID(msg["from"])
            log.msg("message from %s: %s" % (from_jid, msg.body))

            reply = domish.Element((None, "message"))
            reply["to"] = msg["from"]
            reply["from"] = msg["to"]
            reply["type"] = 'chat'
            reply.addElement("body", content="echo: " + str(msg.body))

            self.send(reply)

class JabMessageHandler(object):
    def __init__(self, protocol):
        self.protocol = protocol

    def handle_message(self, message, jid):
        action = self.parse_message(message, jid)
        action(self.protocol, message, jid)

    def parse_message(self, message, jid):
        if "what time is it" in message.body:
            return JabActions.say_four_thirty
        elif "how are you" in message.body:
            return JabActions.say_pretty_well

class JabActions(object):
    @classmethod
    def say_four_thirty(kls, prot, msg, jid):
        pass
