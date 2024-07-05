import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.models import createTables
from routes import books, auth, category

app = FastAPI()
createTables()

origins=[
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"]
)

app.include_router(auth.route)
app.include_router(books.route)
app.include_router(category.route)