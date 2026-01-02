from fastapi import FastAPI
from .database import engine, Base
from .routers import product, seller, login
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Products API written by Patrick Yip",
    description="Get details for all the products on my website",
    terms_of_service="https://www.wisecrackr.com/terms",
    contact={
        "Developer name": "Patrick Yip",
        "website": "https://www.wisecrackr.com",
        "email": "support@wisecrackr.com"
    },
    # docs_url = "/documentation",
    # redoc_url = None
)

app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

Base.metadata.create_all(engine)

