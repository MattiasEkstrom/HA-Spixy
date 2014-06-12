import re

from datetime import datetime

from .plugin import Plugin


class OldUrlPlugin(Plugin):
    def __init__(self, config, client):
        client.register_listener("PRIVMSG", self._handle_url)
        self._client = client
		self._store = {url : {}, score : {}} 
		self._regex = re.compile(
            r'^((?:http|ftp)s?://)?' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        super(OldUrlPlugin, self).__init__(config)

		# test data
		self._store["url"]["www.apa.se"] = [("mts", datetime.now()), ("bjz", datetime.now())]

    def _handle_url(self, nick, target, message, **rest):
        if not target.startswith("#"):
			return 

		parts = message.split(" ")
		for p in parts:
			m = self._regex.match(p)
		    
			if m is None: continue

			print("bajs")

			if p not in self._store["url"]:
				self._store["url"][p] = (nick, datetime.now())
				print("added url: " + p)
			else
				print("this url is old: " + p)
				
		        #self.send_command(nick=nick, target=target, message=message)

    def _handle_command(self, command):
        """choices = self._partition(command['message'])

        if len(choices) == 1:
            answer = choice(self._config['choices'])
        else:
            answer = choice(choices)

        if command['target'].startswith("#"):
            self._client.privmsg(target=command['target'],
                                 message="{nick}: {answer}".format(answer=answer), **command)
        else:
            self._client.privmsg(target=command['nick'], message=answer)"""

		pass

