from telegram.ext import Application, CommandHandler
from src.config import BOT_TOKEN
from src.commands.start import start, help_command
from src.commands.repo_commands import add_repo_command, list_repos_command, remove_repo_command


def create_app() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add_repo", add_repo_command))
    app.add_handler(CommandHandler("list_repos", list_repos_command))
    app.add_handler(CommandHandler("remove_repo", remove_repo_command))

    app.add_error_handler(error_handler)

    return app


async def error_handler(update, context):
    print(f"Error: {context.error}")
