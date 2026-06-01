from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Bot Supervisor Git*\n\n"
        "Monitoreo pushes de GitHub y te notifico al instante.\n\n"
        "*Comandos:*\n"
        "`/add_repo <owner/repo>` — Agregar repo\n"
        "`/list_repos` — Ver repos monitoreados\n"
        "`/remove_repo <owner/repo>` — Dejar de monitorear\n\n"
        "*Configuración en GitHub:*\n"
        "Ve a Settings → Webhooks de tu repo y agrega:\n"
        "URL: `https://tu-dominio.com/webhook`\n"
        "Content Type: `application/json`",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*/add_repo <owner/repo>* — Monitorear un repo\n"
        "*/list_repos* — Listar repos monitoreados\n"
        "*/remove_repo <owner/repo>* — Dejar de monitorear\n\n"
        "Configura el webhook en Settings → Webhooks de tu repo de GitHub.",
        parse_mode="Markdown",
    )
