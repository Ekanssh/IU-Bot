"""
Currently a weak implementation, aiming for a working prototype.
Needs to be completed ASAP.
"""
import imp
import traceback
import os
import asyncio
from bisect import bisect
from datetime import datetime
from discord import Client
from Context import Context, CommandContext, MessageContext

from collections import namedtuple
import enum

class WaitForNewType(enum.Enum):
    message_edit = 2

WaitedEdit = namedtuple("WaitedEdit", "before after")

class Bot(Client):
    def __init__(self, data, bot_conf, log_file="bot.log", DEBUG=0, prefix="", prefix_func=None):
        super().__init__()
        self.data = data
        self.objects = {}
        self.bot_conf = bot_conf
        self.log_file = log_file
        self.DEBUG = DEBUG
        self.LOGFILE = log_file
        self.prefix = prefix
        self.get_prefixes = prefix_func
        self.loading_leader = ""

        self._new_listeners = []

        self.extra_message_handlers = []

        if prefix_func is not None:
            self.add_to_ctx(prefix_func, "get_prefixes")

        self.cmd_cache = {}
        self.cmds = []
        self.handlers = []

        self.scheduled = []
        self.loop_delay = 10

        self.modules_loaded = 0

        self.loop.create_task(self.loopy())

    # Handling system for event message_edit outside of event
    # Method taken from discord.py, credit to Rapptz
    def handle_message_edit(self, before_message, after_message):
        removed = []
        for i, (condition, future, event_type) in enumerate(self._new_listeners):
            if event_type is not WaitForNewType.message_edit:
                continue

            if future.cancelled():
                removed.append(i)
                continue

            try:
                result = condition(before_message, after_message)
            except Exception as e:
                future.set_exception(e)
                removed.append(i)
            else:
                if result:
                    future.set_result(WaitedEdit(before_message, after_message))
                    removed.append(i)


            for idx in reversed(removed):
                del self._new_listeners[idx]

    async def wait_for_message_edit(self, message=None, timeout=None, *, check=None):
        def predicate(before_message, after_message):
            result = True
            if message is not None:
                result = result and before_message.id == message.id
            if callable(check):
                result = result and check(before_message, after_message)
            return result

        future = asyncio.Future(loop=self.loop)
        self._new_listeners.append((predicate, future, WaitForNewType.message_edit))
        try:
            return (await  asyncio.wait_for(future, timeout, loop=self.loop))
        except asyncio.TimeoutError:
            return None

    # Not using the caching system for now, just straight up checking.
    async def on_message(self, message):
        """
        Do basic interp, check the message against the provided caches.
        TODO: Actually curently done with a raw check on the data.
        """
        prefix = 0
        msgctx = MessageContext(bot=self, message=message)
        if self.DEBUG > 10:
            await self.log("Available prefixes are:" + str(await msgctx.get_prefixes()))
        for prfx in (await msgctx.get_prefixes()):
            if message.content.startswith(prfx):
                prefix = prfx
                break
        if not prefix and message.content.split('>')[0].strip(' <!@>') == self.user.id:
                prefix = message.content.split('>')[0] + '>'
        if prefix:
            msgctx = await self.parse_cmd(prefix, msgctx)
        if msgctx is not None:
            for handler in self.extra_message_handlers:
                asyncio.ensure_future(handler[0](msgctx), loop=self.loop)

    async def parse_cmd(self, used_prefix, ctx):
        cmd_msg = ctx.cntnt[len(used_prefix):].strip()
        cmd_name = cmd_msg.split()[0]
        cmd_name = cmd_name.strip().lower()

        if cmd_name not in self.cmd_cache:
            return ctx

        arg_str = cmd_msg[len(cmd_name):].strip()

        cmds = await ctx.get_cmds(CH=self.cmd_cache[cmd_name])
        if cmd_name not in cmds:
            return ctx

        if self.DEBUG > 0:
            asyncio.ensure_future(self.log("Got the command \n{}\nfrom \"{}\" with id \"{}\""
                           .format(ctx.cntnt, ctx.author, ctx.authid)))
        cmd = cmds[cmd_name]
        # Very ugly, want a way to instantiate commandContext using Message context
        cmdCtx = CommandContext(bot=self,
                                message=ctx.msg,
                                cmd=cmd,
                                arg_str=arg_str,
                                used_prefix=used_prefix)
        try:
            await cmd.run(cmdCtx)
            return cmdCtx
        except Exception:
            traceback.print_exc()
            try:
                await cmdCtx.reply("Something went wrong internally.. The error has been logged and should be fixed soon!")
            except Exception:
                await self.log("Something unexpected happened and I can't print the error. Dying now.")
            return None

    async def log(self, logMessage):
        '''
        Logs logMessage in some nice way.
        '''
        # TODO: Some nicer logging, timestamps, a little bit of context
        # For now just print it.
        print(logMessage)
        with open(self.LOGFILE, 'a+') as logfile:
            logfile.write(logMessage + "\n")
        return

    def sync_log(self, logMessage):
        '''
        Logs logMessage synchronously
        '''
        print(logMessage)
        with open(self.LOGFILE, 'a+') as logfile:
            logfile.write(logMessage + '\n')
        return

    def load(self, *argv, depth=0, ignore=[]):
        """
        Intelligently loads modules from the given filepath(s).
        If given a directory, iterates over each file.
        Looks for cmds and load_into, treats them as expected.
        """
        leader = ">.."
        if len(argv) > 1:
            for fp in argv:
                self.load(fp, depth=depth, ignore=ignore)
            return

        fp = argv[0]
        if self.DEBUG > 0:
            self.sync_log("\n"+self.loading_leader+"Loading modules from path: " + fp)
        for ignored in ignore:
            if fp.endswith("/"+ignored):
                self.sync_log(self.loading_leader+"-Path was in ignored list, skipping")
                return

        if os.path.isdir(fp):
            self.sync_log(self.loading_leader+">Path appears to be a directory, going in")
            for fn in os.listdir(fp):
                old_leader = self.loading_leader
                self.loading_leader += leader
                self.load(os.path.join(fp,fn), depth=depth+1, ignore=ignore)
                self.loading_leader = old_leader
            self.sync_log(leader*depth+">Going out of {}\n".format(fp))
            return
        if os.path.isfile(fp):
            if fp.endswith(".py"):
                self.modules_loaded += 1
                module = imp.load_source("bot_module_" + str(self.modules_loaded), fp)
                attrs = dir(module)
                is_module = 0
                old_leader = self.loading_leader
                if "cmds" in attrs:
                    is_module += 1
                    self.loading_leader += "++"
                    self.sync_log(self.loading_leader+" Found \"cmds\" object in file, loading as commands.")
                    self.loading_leader += "+ "
                    module.cmds.load_into(self)
                if "load_into" in attrs:
                    is_module += 1
                    self.loading_leader += "++"
                    self.sync_log(self.loading_leader+" Found \"load_into\" method in file, loading as a module.")
                    self.loading_leader += "+ "
                    module.load_into(self)
                if not is_module:
                    self.loading_leader += "--"
                    self.sync_log(self.loading_leader+" File does not appear to be a valid module. Moving on.")
                self.loading_loader = old_leader



            else:
                self.sync_log(leader*depth+">File was not a python file, skipping")
            return
        else:
            self.sync_log(leader*depth+">File could not be found, skipping")


    def load_cmds(self, filepath):
        """
        Loads commands from a provided command file. Command loading logic is handled by the CH.
        Hopefully the CH is sane.
        TODO: Not really sure how to dynamically import, may need to redo this.
        Also want to be able to handle directories here
        """
        if self.DEBUG > 0:
            self.sync_log("Loading command file from path: " + filepath)
        module = imp.load_source("cmds", filepath)
        module.cmds.load_into(self)

    def load_module(self, filepath):
        """
        Loads a module from the provided file path.
        (E.g. for loading event handlers)

        Expects the module to have a method load_into(bot).
        """
        if self.DEBUG > 0:
            self.sync_log("Loading module from path: " + filepath)
        module = imp.load_source("load_into", filepath)
        module.load_into(self)

    def util(self, func):
        """
        Decorator to make a util method available as a method of Context.
        """
        self.add_to_ctx(func)
        return func

    def add_to_ctx(self, attr, name=None):
        if self.DEBUG:
            self.sync_log(self.loading_leader+"Adding context attribute: {}".format(name if name else attr.__name__))
        setattr(Context, name if name else attr.__name__, attr)



    async def schedule(self, timestamp, event_func, repeat=0):
        event = (timestamp, event_func, repeat)
        scheduled = self.scheduled
        keys=[]
        for i in range(0, len(scheduled)):
            keys.append(scheduled[-i][0])
        scheduled.insert(len(scheduled) - 1 - bisect(keys, timestamp), (timestamp, event_func, repeat))

    async def scheduler(self):
        now = datetime.utcnow().timestamp()
        n = len(self.scheduled)
        for i in range(0, n):
            event = self.scheduled[-1]
            if self.DEBUG > 5:
                await self.log("Checking scheduled event\n{}".format(event))
            if event[0] <= now:
                if self.DEBUG > 1:
                    await self.log("Running scheduled event\n{}".format(event))
                try:
                    output = event[1](self)
                    if asyncio.iscoroutine(output):
                        await output
                    if event[2]:
                        await self.schedule(now + event[2], event[1], event[2])
                except Exception:
                    await self.log("Exception encountered executing scheduled event\n\"{}\"\nTraceback:\n{}".format(event, traceback.format_exc()))
                self.scheduled.pop()
            else:
                break

    async def loopy(self):
        await self.wait_until_ready()
        while not self.is_closed:
            await self.scheduler()
            await asyncio.sleep(self.loop_delay)

    def add_after_event(self, event, func, priority=0):
        after_handler = "after_" + event
        if not hasattr(self, after_handler):
            setattr(self, after_handler, [])
        handlers = getattr(self, after_handler)
        handlers.insert(bisect([handler[1] for handler in handlers], priority), (func, priority))
        self.sync_log(self.loading_leader+"Adding after_event handler \"{}\" for event \"{}\" with priority \"{}\"".format(func.__name__, event, priority))

    def after_ctx_message(self, func, priority=0):
        handlers = self.extra_message_handlers
        handlers.insert(bisect([handler[1] for handler in handlers], priority), (func, priority))
        self.sync_log(self.loading_leader+"Adding after_ctx_message handler \"{}\" with priority \"{}\"".format(func.__name__, priority))

    def dispatch(self, event, *args, **kwargs):
        super().dispatch(event, *args, **kwargs)
        after_handler = "after_"+event
        if hasattr(self, after_handler):
            for handler in getattr(self, after_handler):
                asyncio.ensure_future(handler[0](self, *args, **kwargs), loop=self.loop)

    def make_ctx(self, *args, **kwargs):
        """
        Constructs a context out of the given args and kwargs and passes it back.
        """
        return Context(*args, bot=self, **kwargs)


