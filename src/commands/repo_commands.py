from telegram import Update
from telegram.ext import ContextTypes
from src.database import add_repo, remove_repo, list_repos


async def add_repo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "✏️ Uso: `/add_repo <owner/repo>`\nEj: `/add_repo diego/mi-app`",
            parse_mode="Markdown",
        )
        return

    arg = context.args[0]
    if "/" not in arg or arg.count("/") != 1:
        await update.message.reply_text(
            "❌ Formato inválido. Usa: `owner/repo`", parse_mode="Markdown"
        )
        return

    owner, repo = arg.split("/", 1)
    chat_id = update.effective_chat.id

    success = await add_repo(chat_id, owner, repo)
    if success:
        await update.message.reply_text(
            f"✅ Ahora monitoreo `{owner}/{repo}`\n\n"
            "Configura el webhook en GitHub:\n"
            "Settings → Webhooks → Payload URL",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            f"⚠️ Ya estás monitoreando `{owner}/{repo}`", parse_mode="Markdown"
        )


async def list_repos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    repos = await list_repos(chat_id)

    if not repos:
        await update.message.reply_text(
            "📭 No monitoreas ningún repo todavía.\n"
            "Usa `/add_repo <owner/repo>` para agregar uno.",
            parse_mode="Markdown",
        )
        return

    lines = ["📋 *Repos monitoreados:*"]
    for r in repos:
        lines.append(f"• `{r['owner']}/{r['repo']}`")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def remove_repo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "✏️ Uso: `/remove_repo <owner/repo>`", parse_mode="Markdown"
        )
        return

    arg = context.args[0]
    if "/" not in arg or arg.count("/") != 1:
        await update.message.reply_text(
            "❌ Formato inválido. Usa: `owner/repo`", parse_mode="Markdown"
        )
        return

    owner, repo = arg.split("/", 1)
    chat_id = update.effective_chat.id

    success = await remove_repo(chat_id, owner, repo)
    if success:
        await update.message.reply_text(
            f"🗑️ Dejé de monitorear `{owner}/{repo}`", parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            f"⚠️ No estabas monitoreando `{owner}/{repo}`", parse_mode="Markdown"
        )
