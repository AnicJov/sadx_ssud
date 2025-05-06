import sys
from qasync import QEventLoop, asyncSlot, QApplication
import asyncio
from discord.ext import commands

from display import MainWindow
from draft import DraftController
from dc_bot import create_bot


if __name__ == "__main__":
    controller = DraftController()

    # Create Qt application and event loop
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    # Create main window
    window = MainWindow(controller)
    window.show()

    # Create bot
    dc_bot = create_bot(controller)

    # Slot to connect to the signal — Qt slots must be regular functions
    def on_draft_updated():
        # Schedule the async version using the event loop
        loop.create_task(dc_bot.on_draft_updated())

    # Connect the signal to the Qt app and the Discord async callback
    controller.draft_updated.connect(on_draft_updated)

    # Run everything
    with loop:
        loop.create_task(dc_bot.start("<REDACTED>"))
        loop.run_until_complete(app_close_event.wait())
