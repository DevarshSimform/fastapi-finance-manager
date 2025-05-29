import uvicorn
from fastapi import FastAPI
from src.configurations.database import engine

from src.routers import auth_route, category_route, transaction_route
from src.configurations.database import Base

app = FastAPI()

app.include_router(auth_route.router, prefix="/auth", tags=["Auth"])
app.include_router(category_route.router, prefix="/category", tags=["Category"])
app.include_router(transaction_route.router, prefix="/transaction", tags=["Transaction"])

@app.on_event("startup")    
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)

def main():
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    main()
