from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import ShoppingCart, Course
from parser import parse_shopping_cart

app = FastAPI()

# Allow frontend on localhost to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_schedule", response_model=List[Course])
def generate_schedule(cart: ShoppingCart):
    # Parse raw shopping cart text into structured courses
    all_courses = parse_shopping_cart(cart.pasted_text)
    
    # Filter by time preferences (optional but useful)
    filtered = [
        c for c in all_courses
        if cart.preferences.earliest_time <= c.start_time <= cart.preferences.latest_time
    ]

    return filtered
