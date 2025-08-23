from .on_message import setup as setup_on_message

def setup_all_events(bot):
    setup_on_message(bot)