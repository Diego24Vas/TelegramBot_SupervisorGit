import asyncio
import uvicorn
from src.bot import create_app
from src.server import app as fastapi_app
from src.config import WEBHOOK_PORT
from src.database import init_db


async def main():
    await init_db()

    bot_app = create_app()
    import src.server
    src.server.bot_app = bot_app

    await bot_app.initialize()
    await bot_app.updater.start_polling()
    await bot_app.start()

    print(f"🤖 Bot iniciado. Webhook escuchando en puerto {WEBHOOK_PORT}")

    config = uvicorn.Config(
        fastapi_app, host="0.0.0.0", port=WEBHOOK_PORT, log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
