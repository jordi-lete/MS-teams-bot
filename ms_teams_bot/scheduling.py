import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scraping import get_fixture
from botbuilder.schema import Activity
from botframework.connector.auth import ClaimsIdentity
from botbuilder.core import TurnContext

conversation_reference = None

def save_conversation_reference(reference):
    global conversation_reference
    conversation_reference = reference
    print("reference saved")

def get_conversation_reference():
    return conversation_reference

async def compose_message(adapter, app_id):
    date, opponent, pitch = await get_fixture()
    message = f"scheduled message: {date}, {opponent}, {pitch}"
    print(message)
    
    conversation_reference = get_conversation_reference()
    if not conversation_reference:
        print("No conversation reference yet")
        return
    
    async def send_callback(turn_context: TurnContext):
        await turn_context.send_activity(Activity(type="message", text=message))

    if app_id:
        # If app_id is set, assume we're running with auth
        await adapter.continue_conversation(
            conversation_reference,
            send_callback,
            bot_id=app_id
        )
    else:
        # Running without auth (e.g., with Emulator)
        identity = ClaimsIdentity({}, is_authenticated=False)
        await adapter.continue_conversation(
            conversation_reference,
            send_callback,
            claims_identity=identity
        )

async def schedule_message(adapter, app_id):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(compose_message, "cron", day_of_week="mon", hour=9, minute=0, args=[adapter, app_id])
    # scheduler.add_job(compose_message, "interval", seconds=30, args=[adapter, app_id])
    scheduler.start()
    # For testing without bot framework
    # while True:
    #     await asyncio.sleep(60)

# asyncio.run(schedule_message())