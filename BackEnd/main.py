import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from models import SchedulePreferences, ShoppingCart, Course

class Fruit(BaseModel):
    name:str

class Fruits(BaseModel):
    fruits: List[Fruit]

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )
"""
@app.post("/generate_schedule", response_model=List[Course])
def generate_schedule(cart: ShoppingCart):
    parsed_courses = parse_shopping_cart(cart.pasted_text)
    optimized = optimize_schedule(parsed_courses, cart.preferences)
    return optimized
"""



memory_db = {"fruits": []}

@app.get("/fruits", response_model=Fruits)
def get_fruits():
    return Fruits(fruits = memory_db["fruits"])


@app.post("/fruits")
def add_fruits(fruit: Fruit):
    memory_db["fruits"].append(fruit)
    return fruit

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)