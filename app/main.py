from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
import sqlite3


app = FastAPI()

# Database setup (SQLite for simplicity, switch to PostgreSQL for deployment)
conn = sqlite3.connect("orders.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    price REAL,
                    quantity INTEGER,
                    order_type TEXT)''')
conn.commit()

# Pydantic Model for Request Body
class Order(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

# Endpoint to place an order
@app.post("/orders")
def create_order(order: Order):
    cursor.execute("INSERT INTO orders (symbol, price, quantity, order_type) VALUES (?, ?, ?, ?)",
                   (order.symbol, order.price, order.quantity, order.order_type))
    conn.commit()
    return {"message": "Order placed successfully"}

# Endpoint to get all orders
@app.get("/orders")
def get_orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return {"orders": orders}

# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text("New order update available")


