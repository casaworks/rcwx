# coding:utf-8

from message import *

class Command:
    def __init__(self, app, desc):
        self.app = app
        self.desc = desc
    
    def respond_to(self, msg):
        if isinstance(msg, TextMessage):
            content = msg.content.strip()
            if content == 'x' or content == 'X':
                userid = msg.from_user
                self.app.quit_command(userid)
                curcmd = self.app.get_user_curcmd(userid)
                return curcmd.prompt_help(msg)
            elif content == '?' or content == u'？':
                return self.prompt_help(msg)
        response = self.respond_to_message(msg)
        return response if response else self.prompt_error(msg)
        
    def respond_to_message(self, msg):
        pass
            
    def prompt_error(self, msg):
        return self.prompt_help(msg)
        
    def append_exit_prompt(self, text):
        return u'%s\n(发送x退出此功能)' % (text)
    
class SelectionCommand(Command):
    def __init__(self, app, desc, prompt_prefix=None):
        Command.__init__(self, app, desc)
        self.prompt_prefix = prompt_prefix
        self.subcmds = []
        
    def append_command(self, cmd):
        self.subcmds.append(cmd)
        
    def insert_command(self, index, cmd):
        self.subcmds.insert(index, cmd)
        
    def get_command(self, index):
        return self.subcmds[index]
        
    def get_command_codes(self):
        codes = []
        codes.extend([str(i) for i in xrange(1, len(self.subcmds) + 1)])
        if not self.app.is_root_command(self):
            codes.append('x')
        return codes
        
    def make_prompt_text(self, key, text):
        return '%s  %s' % (key, text)
    
    def respond_to_message(self, msg):
        if isinstance(msg, TextMessage):
            content = msg.content.strip()
            if content.isdigit():
                index = int(content) - 1
                if index in xrange(0, len(self.subcmds)):
                    cmd = self.subcmds[index]
                    self.app.enter_command(msg.from_user, index)
                    return cmd.prompt_help(msg)
        
    def prompt_help(self, msg):
        prompt_lines = []
        if self.prompt_prefix:
            prompt_lines.insert(0, self.prompt_prefix)
        for i, subcmd in enumerate(self.subcmds):
            prompt_lines.append(self.make_prompt_text(str(i + 1), subcmd.desc))
        if not self.app.is_root_command(self):
            prompt_lines.append(self.make_prompt_text('x', u'返回上级菜单'))
        prompt_text = '\n'.join(prompt_lines)
        return TextMessage(msg.to_user, msg.from_user, prompt_text)
    