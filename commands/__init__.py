from .memory import setup as setup_memory
from .bye import setup as setup_bye
from .stats import setup as setup_stats
from .web_cmd import setup as setup_web
from .help import setup as setup_help
from .context import setup as setup_context
from .auto import setup as setup_auto
from .limits import setup as setup_limits

def setup_all_commands(bot):
    setup_memory(bot)
    setup_bye(bot)
    setup_stats(bot)
    setup_web(bot)
    setup_help(bot)
    setup_context(bot)
    setup_auto(bot)
    setup_limits(bot)