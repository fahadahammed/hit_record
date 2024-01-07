#  Copyright (c) Fahad Ahammed 2024.
from src import app

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST"),
        port=app.config.get("PORT")
    )