from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

# HTML client to test notifications
@app.get("/", response_class=HTMLResponse)
async def get():
    return """
    <html>
        <body>
            <h1>Notification Stream</h1>
            <ul id="events"></ul>
            <script>
                const evtSource = new EventSource("/notifications");
                evtSource.onmessage = function(event) {
                    const newElement = document.createElement("li");
                    newElement.textContent = "🔔 " + event.data;
                    document.getElementById("events").appendChild(newElement);
                };
            </script>
        </body>
    </html>
    """

# SSE endpoint
@app.get("/notifications")
async def notifications():
    async def event_generator():
        counter = 0
        while True:
            await asyncio.sleep(2)
            counter += 1
            yield f"data: Notification #{counter}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
