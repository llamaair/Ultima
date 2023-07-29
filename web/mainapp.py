from quart import Quart, render_template_string

class MyAsyncApp(Quart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

app = MyAsyncApp(__name__)

@app.route('/')
async def main():

    template = """
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bot Dashboard</title>
        <style>
            /* Add custom CSS styles here */
        </style>
    </head>
    <body>
        <h1>Bot Dashboard</h1>
    </body>
    </html>
"""

    return await render_template_string(template)

async def startapp():
    await app.run_task(host="0.0.0.0", port=25512)
