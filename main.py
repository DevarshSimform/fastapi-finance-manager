import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.configurations.database import Base, engine
from src.configurations.settings import settings
from src.routers import auth_route, category_route, transaction_route

app = FastAPI(title="Finance Manager API", root_path="/api")

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

app.include_router(auth_route.router, prefix="/auth", tags=["Auth"])
app.include_router(category_route.router, prefix="/category", tags=["Category"])
app.include_router(
    transaction_route.router, prefix="/transaction", tags=["Transaction"]
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


def main():
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    main()
