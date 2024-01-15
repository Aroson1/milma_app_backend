# Install all the dependencies using: `pip install -r requirements.txt`
# To start server run: `uvicorn --port 1234 main:app --reload`
from App.app import app 
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app)
