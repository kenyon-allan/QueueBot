import discord
import os
from dotenv import load_dotenv
from discord import ApplicationContext
import commands.queue as queue

# import commands.game as game
from role_ids import *
from exceptions import *

# Load environment variables
load_dotenv()
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


# # QUEUE COMMANDS
@bot.slash_command(name="join", description="Join the queue for a game")
async def slash_join_queue(ctx: ApplicationContext):
    try:
        user_id, queue_length = queue.join_queue(ctx)
    except AlreadyInQueueException as e:
        await ctx.respond(f"<@{e.user.id}> is already in the queue!")
        return
    if queue_length == 1:
        await ctx.respond(
            f"<@{user_id}> has joined the queue! There is now {queue_length} player in the queue."
        )
    else:
        await ctx.respond(
            f"<@{user_id}> has joined the queue! There are now {queue_length} players in the queue."
        )


@bot.slash_command(name="list", description="List the players in the queue")
async def slash_list_queue(ctx: ApplicationContext):
    await ctx.respond(queue.list_queue(ctx))


@bot.slash_command(name="leave", description="Leave the queue for a game")
async def slash_leave_queue(ctx: ApplicationContext):
    try:
        user_id, queue_length = queue.leave_queue(ctx)
    except NotInQueueException as e:
        await ctx.respond(f"<@{e.user.id}> is not in the queue!")
        return
    if queue_length == 1:
        await ctx.respond(
            f"<@{user_id}> has left the queue! There is now {queue_length} player in the queue."
        )
    else:
        await ctx.respond(
            f"<@{user_id}> has left the queue! There are now {queue_length} players in the queue."
        )


@bot.slash_command(name="clear", description="Clear the queue")
async def slash_clear_queue(ctx: ApplicationContext):
    if (
        ADMIN_ID in [role.id for role in ctx.user.roles]
        or ctx.user.guild_permissions.administrator
    ):
        queue.clear_queue()
        await ctx.respond("Queue cleared!")
    else:
        await ctx.respond("Only Bot Engineers or Administrators can clear the queue!")


# # GAME COMMANDS


if __name__ == "__main__":
    bot.run(AUTH_TOKEN)
