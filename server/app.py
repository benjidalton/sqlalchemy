from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# ----- custom imports ------ +
from routers import user_router

app = FastAPI(
	title="My FastAPI App",
	debug=True if os.getenv("DEBUG").lower() == "true" else False,
	description="API for testing SQLAlchemy + MySQL + Pydantic integration",  
	contact={
		"name": "Ben Dalton",
		"url": "https://github.com/benjidalton"
	}
)
 
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_PORT")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)