from fastapi import FastAPI,WebSocket, BackgroundTasks
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config import settings



templates = Jinja2Templates(directory="templates")


app=FastAPI()

@app.get("/")
async def home(request: Request):
	return templates.TemplateResponse("general_pages/homepage.html",{"request":request})




websocket_list=[]
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
	await websocket.accept()
	if websocket not in websocket_list:
		websocket_list.append(websocket)
	while True:
		data = await websocket.receive_text()
		for web in websocket_list:
			if web!=websocket:
				await web.send_text(f"{data}")
    
async def background_tasks(email: str, message = ""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
        
@app.post("/send-notification/{email}", status_code=202)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    breakpoint()
    background_tasks.add_task(background_tasks, email, message="some notification")
    return {"message": "Notification sent in the background"}







