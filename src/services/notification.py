from datetime import datetime


def format_push_notification(owner: str, repo: str, branch: str, commits: list) -> str:
    lines = [f"🔔 Nuevo push a `{owner}/{repo}`"]

    for commit in commits:
        author = commit.get("author", {}).get("name", "Desconocido")
        ts = commit.get("timestamp", "")
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            date_str = dt.strftime("%d %b %Y, %H:%M")
        except (ValueError, AttributeError):
            date_str = ts

        message = commit.get("message", "").split("\n")[0]

        lines.append("")
        lines.append(f"📝 {message}")
        lines.append(f"👤 {author}")
        lines.append(f"📅 {date_str}")
        lines.append(f"🌿 {branch}")

        added = commit.get("added", [])
        modified = commit.get("modified", [])
        removed = commit.get("removed", [])

        file_lines = []
        for f in added:
            file_lines.append(f"  + {f}")
        for f in modified:
            file_lines.append(f"  M {f}")
        for f in removed:
            file_lines.append(f"  - {f}")

        if file_lines:
            total = len(added) + len(modified) + len(removed)
            lines.append(f"📄 Archivos ({total}):")
            lines.extend(file_lines)

    return "\n".join(lines)
