from errbot import BotPlugin, botcmd, re_botcmd
from itertools import chain
import os
import re
import subprocess


class HelloWorld(BotPlugin):
    """Example 'Hello, world!' plugin for Errbot"""

    @botcmd
    def hello(self, msg, args):
        """Say hello to the world"""
        return self.hello_helper()

    @botcmd
    def hello_another(self, msg, args):
        """Say hello to the world"""
        return self.hello_another_helper()

    @re_botcmd(pattern=r"^(([Cc]an|[Mm]ay) I have a )?cookie please\?$")
    def hand_out_cookies(self, msg, match):
        """
        Gives cookies to people who ask me nicely.

        This command works especially nice if you have the following in
        your `config.py`:

        BOT_ALT_PREFIXES = ('Err',)
        BOT_ALT_PREFIX_SEPARATORS = (':', ',', ';')

        People are then able to say one of the following:

        Err, can I have a cookie please?
        Err: May I have a cookie please?
        Err; cookie please?
        """
        yield "Here's a cookie for you, {}".format(msg.frm)
        yield "/me hands out a cookie."

    @re_botcmd(
        pattern=r"(^| )cookies?( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_talk_of_cookies(self, msg, match):
        """Talk of cookies gives Errbot a craving..."""
        return "Somebody mentioned cookies? Om nom nom!"

    @botcmd(admin_only=True)
    def cmd(self, msg, args):
        """whoami"""
        try:
            command = 'whoami'
            if args:
                re_quotation = re.compile(r'("[^"]+")|(\'[^\']+\')|([^ ]+)')
                command = list(
                    filter(lambda x: x != "",
                           chain.from_iterable(re_quotation.findall(args))))
            cmd_call = subprocess.Popen(
                command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        except Exception as _err:
            return _err
        tags, _err = cmd_call.communicate()
        return_code = cmd_call.returncode
        return f"{command}\treturn_code={return_code}\n{tags.decode('utf-8')}\n"

    @staticmethod
    def hello_helper():
        return "Hello world!"

    def hello_another_helper(self):
        return "HELLO WORLD!"
