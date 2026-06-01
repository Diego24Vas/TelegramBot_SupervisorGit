import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException
from src.config import WEBHOOK_SECRET
from src.database import get_chats_for_repo, is_commit_processed, mark_commit_processed
from src.services.notification import format_push_notification

app = FastAPI(title="GitHub Webhook")
bot_app = None


def _verify_signature(payload: bytes, signature_header: str) -> bool:
    if not WEBHOOK_SECRET:
        return True
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()

    sig = request.headers.get("X-Hub-Signature-256", "")
    if not _verify_signature(body, sig):
        raise HTTPException(403, "Invalid signature")

    event = request.headers.get("X-GitHub-Event", "")
    if event != "push":
        return {"status": "ignored", "event": event}

    payload = await request.json()

    owner = payload["repository"]["owner"]["name"]
    repo = payload["repository"]["name"]
    branch = payload["ref"].replace("refs/heads/", "")

    chat_ids = await get_chats_for_repo(owner, repo)
    if not chat_ids:
        return {"status": "no_subscribers"}

    commits = payload.get("commits", [])
    new_commits = []
    for commit in commits:
        sha = commit.get("id", "")
        if sha and not await is_commit_processed(owner, repo, sha):
            new_commits.append(commit)
            await mark_commit_processed(owner, repo, sha)

    if not new_commits:
        return {"status": "no_new_commits"}

    message = format_push_notification(owner, repo, branch, new_commits)

    for chat_id in chat_ids:
        try:
            await bot_app.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Error sending to {chat_id}: {e}")

    return {"status": "ok", "commits": len(new_commits), "chats": len(chat_ids)}


@app.get("/health")
async def health():
    return {"status": "ok"}
