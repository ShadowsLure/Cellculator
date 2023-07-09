import discord
import topgg
import asyncio

intents = discord.Intents.default()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"We have logged in as {self.user}")
        
    async def setup(self):
        dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEwNzAzMDEzMzQ1MTcwNTU1MTgiLCJib3QiOnRydWUsImlhdCI6MTY4MjQ1NDQ1NX0.rL8UwgpvR-bPylqDgVNs6U_PUp7ZUIvif8dGr3XUQWk"
        self.topggpy = topgg.DBLClient(self, dbl_token, autopost=True, post_shard_count=True)
        
        await self.topggpy.post_guild_count()

client = MyClient(intents=intents)

@client.event
async def on_autopost_success():
    print(f"Posted server count ({client.topggpy.guild_count}), shard count ({client.shard_count})")

# Call the setup() function using await keyword
async def run():
    await client.setup()

# Run the client
async def main():
    await client.start("MTA3MDMwMTMzNDUxNzA1NTUxOA.GBwY0z.4qijJ0VRxdqRd4WsGklVnvjMuOgvKun-4NlwPQ")
    await run()

asyncio.run(main())
