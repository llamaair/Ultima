from quart import Quart

class MyAsyncApp(Quart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

app = MyAsyncApp(__name__)

@app.route('/')
async def main():
    return "Hello world!"

async def startapp():
    await app.run_task(host="0.0.0.0", port=25214)
