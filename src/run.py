import os

import uvicorn
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    host = os.getenv("APP_HOST", "0.0.0.0")
    port = os.getenv("APP_PORT", 8000)
    log_level = os.getenv("LOG_LEVEL", "info")
    auto_reload = os.getenv("AUTO_RELOAD", "False")

    uvicorn.run(
        app="main:app",
        host=host,
        port=int(port),
        log_level=log_level,
        reload=auto_reload.lower() == "true",
    )
