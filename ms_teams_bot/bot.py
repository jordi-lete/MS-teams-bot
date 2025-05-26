# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
import scraping
import scheduling


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        conversation_reference = TurnContext.get_conversation_reference(turn_context.activity)
        scheduling.save_conversation_reference(conversation_reference)
        text = turn_context.activity.text.strip().lower()
        if "?fixture" in  text:
            date, opponent, pitch = scraping.get_fixture()
            await turn_context.send_activity(f"Our next fixture is against {opponent} on {date}, {pitch}")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        bot_id = turn_context.activity.recipient.id
        for member_added in members_added:
            if member_added.id == bot_id:
                await turn_context.send_activity("Hi, I'm a chatbot! I'll notify you of upcoming fixtures and results.")
