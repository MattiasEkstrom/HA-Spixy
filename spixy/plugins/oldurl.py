import re

from datetime import datetime

from .plugin import Plugin


class OldUrlPlugin(Plugin):
    def __init__(self, config, client):
        client.register_listener("PRIVMSG", self._handle_url)
        self._client = client
        self._store = {'url' : {}, 'score' : {}} 
        self._regex = re.compile(
            r'^((?:http|ftp)s?://)?' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        # test data
        self._store['url']['#spixytestblah'] = {}
        self._store['url']['#spixytestblah']['www.apa.se'] = [("mts", datetime.now()), ("bjz", datetime.now())]
        
        super(OldUrlPlugin, self).__init__(config)

    def _handle_url(self, nick, target, message, **rest):
        if not target.startswith("#"):
            return 

        parts = message.split(" ")
        for p in parts:
            m = self._regex.match(p)
            if m is None: continue
            self.send_command(nick=nick, target=target, message=p)

    def _handle_command(self, command):
        chan = command['target']
        url = command['message']
        nick = command['nick']
        urldb = self._store['url']
        sdb = self._store['score']

        if chan not in urldb:
            urldb[chan] = {}

        if url not in urldb[chan]:
            urldb[chan][url] = [(nick, datetime.now())]
            print("added url: " + url)
            if nick in sdb:
                sdb[nick] += 1
            else:
                sdb[nick] = 1
        else:
            urldb[chan][url].append((nick, datetime.now()))
            times = len(urldb[chan][url])
            if nick in sdb:
                sdb[nick] -= times
            else:
                sdb[nick] = -times
            self._client.privmsg(target=chan, message="{nick}: {url} is old as fuck and has been posted {times} times, your score is: {score}".format(url=url, nick=nick, times=times, score=sdb[nick]))
            


