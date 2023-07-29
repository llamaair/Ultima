from quart import Quart, render_template

class MyAsyncApp(Quart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

app = MyAsyncApp(__name__)

@app.route('/')
async def main():
    return await render_template('dashboard.html')

async def startapp():
    await app.run_task(host="0.0.0.0", port=25512)
