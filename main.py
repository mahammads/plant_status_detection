import os
import uvicorn
from app import config

if __name__ == "__main__":
    hostip = "127.0.0.1"
    # hostip = config.SERVER_IP
    uvicorn.run("app.api:detect_cat", 
                # host=hostip, port=config.SERVER_PORT, reload=True)
                host=hostip, port=8000, reload=True)
    