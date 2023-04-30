import discord
from discord.ext import commands
import openai
import re
import os

openai.api_key = "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"

class OpenAICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            # Remove bot mention from the message
            message_text = message.content.replace(f"<@!{self.bot.user.id}>", "")

            # Check if the message contains a dot for teaching
            if "." in message_text:
                # Extract the message before and after the dot
                message_parts = message_text.split(".")
                if len(message_parts) == 2:
                    prompt = message_parts[0].strip()
                    response = message_parts[1].strip()

                    # Teach the bot
                    self.chat_history.append((prompt, response))

                    # Send confirmation message
                    await message.channel.send(f"Thanks for teaching me that, {message.author.mention}!")

            else:
                # Generate response from OpenAI
                response = openai.Completion.create(
                    engine="davinci",
                    prompt=message_text,
                    temperature=0.5,
                    max_tokens=60,
                    n=1,
                    stop=None,
                    presence=None,
                    frequency_penalty=1,
                    best_of=None,
                    logprobs=None,
                )

                # Store the prompt and response in chat history
                self.chat_history.append((message_text, response.choices[0].text))

                # Send the response to the channel
                await message.channel.send(response.choices[0].text)

def setup(bot):
    bot.add_cog(OpenAICog(bot))
