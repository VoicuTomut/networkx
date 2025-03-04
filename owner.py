from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from pyngrok import ngrok

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the API"}

@app.get("/redirect")
def redirect_order_complete():
    return RedirectResponse(url="/order-complete")

@app.get("/order-complete")
def order_complete():
    return {"message": "Order completed successfully!"}

if __name__ == "__main__":
    # Open an ngrok tunnel to the port your FastAPI app runs on
    public_url = ngrok.connect(8000).public_url
    print(f"Public URL: {public_url}")

    # Run FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
