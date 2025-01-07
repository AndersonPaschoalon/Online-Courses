from fastapi import FastAPI

print("=====================================================")
print("Initializing FastAPI Application")
print("=====================================================")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}