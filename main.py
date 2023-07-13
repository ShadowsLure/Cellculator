import interactions as i
import asyncio
import time
import random
from mongo import create_user_data, get_user_data, update_user_data, get_user_history
from mongo import time_retrieve, time_update, time_memory
import mongo as m  # I got tired of importing all the functions directly
from logic import core, thread  # these are kept private
from reasons import gain_activity_check, lost_activity_check 
from updates import update_embed
from promts import positive_prompt_title, negative_prompt_title

bot = i.Client(
    intents=i.Intents.DEFAULT, send_command_tracebacks=False
    )  # send_command_tracebacks is set to True by default, so watch out!


@i.listen()  # Setting up bot's Activity, 
async def on_startup() -> None:
    print('Cellculator is Live!')

    activity = i.Activity.create(
        name='v1.1 RELEASED!!',
        type=i.ActivityType.PLAYING  # ActivityType.CUSTOM is not avaliable for bots
    )
    await bot.change_presence(activity=activity)


@i.slash_command(name='status',
                 description='Check the connectivity of the bot!'
                 ) # the famous ping command, renamed 
async def ping(ctx: i.InteractionContext) -> None:
    await bot.wait_until_ready()
    # Embed creation
    embed = i.Embed(title='Online!',
                    description='Latency: **{0}** ms\n Cellculator is operating normally!'.format(
                        round(bot.latency * 1000, 2)),
                    color=i.Color.from_hex(value='#fea4b7'))
    embed.add_field(
        name='Upcoming Features',
        value='RELEASED : Cellculator will send an alert whenever someone in a conversation looses/gains braincells! '\
              '\n1. Brain Quiz : A quiz based on absurd word-play based questions and theory of braincells. ETA : 30 days'
                
    )
    await ctx.defer()  # this makes "bot is thinking" animation for the described time below
    await asyncio.sleep(1.69) 
    await ctx.send(embeds=embed)


@i.slash_command(name='vote-invite',
                 description='Vote Cellculator or Invite Cellculator to your server!!'
                 )  # Voting and invite links, because people hardly check the description of the bot
# Button creation
async def invite(ctx: i.ComponentContext) -> None:
    # Action row is just a way to add more buttons
    components: list[i.ActionRow] = [i.ActionRow(i.Button(
        style=i.ButtonStyle.LINK,
        label='Invite Cellculator',
        url='https://discord.com/api/oauth2/authorize?client_id=1070301334517055518&permissions=275280948288&scope=bot%20applications.commands'
    ),
        i.Button(
            style=i.ButtonStyle.LINK,
            label='Vote me!',
            url='https://top.gg/bot/1070301334517055518?s=041b6d7bac6a4'
        ),
        i.Button(
            style=i.ButtonStyle.LINK,
            label='Join BCHQ!',
            url='https://dsc.gg/braincellshq' # For some reason the vanilla server invite link doesn't work
        )
    )]

    await ctx.defer() # the thinking animation
    # Embed Creation 
    embed = i.Embed(color=i.Color.from_hex(value='#fea4b7'))
    embed.add_field(name='Invite Cellculator!',
                    value="Want this awesome bot in your server too? Click the button 'Invite Cellculator'!!")
    embed.add_field(name='Vote me!',
                    value='Help Cellculator grow and reach every corner of the world! Each braincells is to be counted!')
    embed.add_field(name='Join BCHQ!',
                    value="Braincells HQ (BCHQ) is home to the Theory of Braincells! It's also a pseudo-support "
                          "server for Cellculator! Click the button 'Join BCHQ' to join! ")
    await ctx.send(embeds=embed, components=components)


@i.slash_command(name='brain',
                 group_name= 'cell',
                 sub_cmd_name= "count",
                 sub_cmd_description= "Get your numbers!") 
# all this name create the command "/brain cell count", no spaces are allowed in command names, so this is how you add it!
async def cbc(ctx: i.InteractionContext) -> None:
    # Initial status change
    await bot.change_presence(activity=i.Activity.create(
        name=f"{ctx.author.display_name}'s Brain Cells!",
        type=i.ActivityType.WATCHING))

    # Command cooldown (15 mins)     
    if time_memory(f'{ctx.author.id}') is False:
        # Get the stored time data and user data value
        user_dat = get_user_data(f'{ctx.author.id}')
        time_dat = time_retrieve(f'{ctx.author.id}')
        current_time = time.time()
        last_time = time_dat['curr_time']
        time_since_last_use = current_time - last_time
        time_remaining = round((900 - time_since_last_use) / 60, 0)

        # Embed for sending the message
        embed = i.Embed(
            title='Anti-Spam System',
            description=
            f'Would you find mind waiting for around {int(time_remaining)} minutes before sending another '
            f'counting request? Thank you!',
            color=i.Color.from_hex(value='#fea4b7'))

        embed.add_field(
            name='Previous Count',
            value=f"\nNet brain cells: {user_dat['random_int']}\nNormal cells: "
                  f"{user_dat['int1']}\n Corrupt cells: {-1 * user_dat['int2']}")

        await ctx.defer()
        await asyncio.sleep(1)

        await ctx.send('UPDATE! v1.1 is OUT! Use `/updates` for more info!',embeds=embed)

    else:
        # After cooldown
        await ctx.defer()

        # Checking whether user_id already exists in database
        if get_user_data(f'{ctx.author.id}') is not None:
            # Getting the required user data
            user_data = get_user_data(f'{ctx.author.id}')
            normal = user_data['int1']
            curr = user_data['int2']
            # Re-counting braincells (thread is a function)
            updated_cells = thread(normal, curr)
            reason_val = None

            # Code logic for providing reasons
            if curr != updated_cells[2] and normal != updated_cells[1]:
                if normal < updated_cells[1] and curr > updated_cells[2]:
                    reason_val = f'You gained normal and corrupt braincells!\nReason for Normal: `{gain_activity_check()[0]}`\nReason for Corrupt: `{lost_activity_check()[0]}`'
                elif normal > updated_cells[1] and curr < updated_cells[2]:
                    reason_val = f'You lost normal and corrupt braincells!\nReason for Normal: `{lost_activity_check()[0]}`\nReason for Corrupt: `{gain_activity_check()[0]}`'

                elif normal < updated_cells[1] and curr < updated_cells[2]:
                    reason_val = f'You gained normal braincells and lost your corrupt braincell!\nReason for Normal: ' \
                                 f'`{gain_activity_check()[0]}`\nReason for Corrupt: `{gain_activity_check()[0]}`'
                elif normal > updated_cells[1] and curr > updated_cells[2]:
                    reason_val = f'You lost your normal braincell and gained corrupt braincells!\nReason for Normal:' \
                                 f' `{lost_activity_check()[0]}`\nReason for Corrupt: `{lost_activity_check()[0]}`'

            elif curr - updated_cells[2] == 0:
                if normal > updated_cells[1]:
                    reason_val = f'You lost normal braincells!\nReason: `{lost_activity_check()[0]}`'
                if normal < updated_cells[1]:
                    reason_val = f'You gained normal braincells!\nReason: `{gain_activity_check()[0]}`'

            elif normal - updated_cells[1] == 0:
                if curr > updated_cells[2]:
                    reason_val = f'You gained corrupt braincells!\nReason: `{lost_activity_check()[0]}`'
                elif curr < updated_cells[2]:
                    reason_val = f'You lost corrupt braincells!\nReason: `{gain_activity_check()[0]}`'

            # Creating an Embed to send
            embed = i.Embed(
                title='CELLCULATOR',
                description='Here, I have counted your brain cells again!',
                color=i.Color.from_hex(value='#fea4b7'))

            embed.add_field(
                name='Current Count',
                value=
                f"Net Brain cells: {updated_cells[0]}\nNormal Brain cells: {updated_cells[1]}\n"
                f"Corrupt Brain cells: {-1 * updated_cells[2]}")

            embed.add_field(
                name='Previous Count',
                value=f"Net Brain cells: {normal + curr}\nNormal Brain cells: {normal}\n "
                      f"Corrupt Brain cells: {-1 * curr}")

            embed.add_field(
                name='Review',
                value=f'{reason_val}'
            )

            embed.set_footer(
                text='The reason mentioned above is absolutely true, no matter what the user says!'
            )

            new_net = updated_cells[0]
            user_history = get_user_history(f'{ctx.author.id}')
            past_high = user_history['high']
            past_low = user_history['low']
            # Checking for new records in highest or lowest count
            if updated_cells[0] > past_high:
                past_high = new_net
            elif updated_cells[0] < past_low:
                past_low = new_net
                # Updating the databse with new braincell count and time values
            update_user_data(f'{ctx.author.id}', updated_cells[0], updated_cells[1],
                             updated_cells[2], past_high, past_low)
            time_update(f'{ctx.author.id}', time.time())

            await asyncio.sleep(6.9)
            await ctx.send('UPDATE! v1.1 is OUT! Use `/updates` for more info!',embeds=embed)
            

        # If user's USER_ID in not in the database
        else:
            # core() function counts braincells
            cells = core()
            
            # Embed creation
            embed = i.Embed(
                title=f'Successfully initialized for {ctx.author.display_name}',
                description=
                'Hey! This will be your first time getting your brain cell counted! Hope it goes well!',
                color=i.Color.from_hex(value='#fea4b7'))

            embed.add_field(
                name='Current Count',
                value=
                f'Net Brain cells: {cells[0]} \nNormal Brain cells: {cells[1]}\nCorrupt Brain cells:'
                f' {-1 * cells[2]}')

            embed.set_footer(
                text='Your Brain Profile has been formed! Use `/brain-profile` to view it!\nYou will also be able to '
                     'view reasons as to why you gained/lost brain cells the next time you use this command!')

            await asyncio.sleep(6.9)
            
            await ctx.send('UPDATE! v1.1 is OUT! Use `/updates` for more info!',embeds=embed)

            create_user_data(f'{ctx.author.id}', cells[0], cells[1], cells[2])

            time_update(f'{ctx.author.id}', time.time())

    # the status updated back to original
    activity = i.Activity.create(
        name='v1.1 RELEASED!',
        type=i.ActivityType.PLAYING
    )
    await bot.change_presence(activity=activity)


@i.slash_command(name='brain', sub_cmd_name='profile',
                 sub_cmd_description="Get to know about brain profile!"
                 ) # creates the command as "/brain profile"
@i.slash_option(
    name='user',
    description='Whose profile do you want to see?',
    required=False,
    opt_type=i.OptionType.USER # option type is USER
) # this creates options
async def profile(ctx: i.InteractionContext, user: i.User = None):
    person = user
    # If person a user is not specified
    if person is not None:
        await ctx.defer()
        user_history = get_user_history(f'{person.id}')
        # Checking if user exists using error handling
        try:
            high_latest = user_history['high']
            low_latest = user_history['low']
            net_latest = user_history['random_int']
            embed = i.Embed(title='BRAIN PROFILE',
                            description=f"Here is {person.display_name}'s profile!",
                            color=i.Color.from_hex(value='#fea4b7'))
            embed.set_thumbnail(f'{person.avatar.url}')
            embed.add_field(
                name='BIO DATA',
                value=f'Name: {person.username} \nNickname: {person.display_name} \nJoined Discord: {person.created_at}'
            )
            embed.add_field(
                name='BRAIN DATA',
                value=f'Highest recorded brain cells : {high_latest} \nLowest recorded brain cells: {low_latest} \nCurrent brain cells: {net_latest}'
            )
            embed.set_footer(text='NOTE : The records are based on the data stored\nfrom 14th April 2023 till present')
            await asyncio.sleep(2)
            await ctx.send('UPDATE! v1.1 is OUT! Use `/updates` for more info!',embeds=embed)
        except TypeError:
            await ctx.send(
                f"{person.mention} doesn't have a profile yet! Use `/braincells-count` to register for a profile!")
    else:
        # this time a user is mentioned 
        await ctx.defer()
        user_history = get_user_history(f'{ctx.author.id}')
        # same error handling
        try:
            high_latest = user_history['high']
            low_latest = user_history['low']
            net_latest = user_history['random_int']
            embed = i.Embed(title='BRAIN PROFILE',
                            description=f"Here is {ctx.author.display_name}'s profile!",
                            color=i.Color.from_hex(value='#fea4b7'))
            embed.set_thumbnail(f'{ctx.author.avatar.url}')
            embed.add_field(
                name='BIO DATA',
                value=f'Name: {ctx.author.username} \nNickname: {ctx.author.display_name} \nJoined Discord: {ctx.author.created_at}'
            )
            embed.add_field(
                name='BRAIN DATA',
                value=f'Highest recorded brain cells : {high_latest} \nLowest recorded brain cells: {low_latest} \nCurrent brain cells: {net_latest}'
            )
            embed.set_footer(text='NOTE : The records are based on the data stored\nfrom 14th April 2023 till present')
            await asyncio.sleep(2)
            await ctx.send('UPDATE! v1.1 is OUT! Use `/updates` for more info!',embeds=embed)
        except TypeError:
            await ctx.send(
                f"{ctx.author.mention} doesn't have a profile yet! Use `/braincells-count` to register for a profile!")


@i.slash_command(name='help', description='An arranged lists of cellculator commands!'
                 ) # A weird help command
# this is how we create a drop down menu for options
async def helps(ctx: i.ComponentContext):
    options = [
        i.StringSelectOption(label="/brain cell count", value="1"),
        i.StringSelectOption(label="/brain profile", value="2"),
        i.StringSelectOption(label="/vote-invite", value="3"),
        i.StringSelectOption(label="/cellculator", value="4"),
        i.StringSelectOption(label="/modify alerts", value='5'),
        i.StringSelectOption(label="/status", value='6'),
        i.StringSelectOption(label="/support", value='7'),
        i.StringSelectOption(label="/updates", value='8')]
    help_menu = i.StringSelectMenu(
        *options,
        custom_id='help_list',
        placeholder='Select a command!',
        max_values=1, min_values=1)
    await ctx.send(
        "Lost? Here is a list of all the currently available commands! Select one for detailed information!",
        components=help_menu)

# and this is how we make those options get a job
@i.component_callback("help_list")
async def help_callback(ctx: i.ComponentContext):
    selected_option = ctx.values[0] # retrive the option value
    # should be obvious 
    if selected_option == "1": 
        embed = i.Embed(
            title="/braincells-count",
            description="This command will count your current braincells!\n\nThis also contains a review section, which will holds the reason as to why your normal/corrupt braincells increased/decreased."
                        "\n\nThe reason provided is absolutely true, no matter what the user says! \n\nCommand cooldown for a user : 15 minutes\n"
                        "Don't know what the values mean? Here is a brief description:",
            color=i.Color.from_hex(value='#fea4b7')
        )
        embed.add_field(
            name='Net Brain Cells',
            value='Essentially the effective amount of brain cells, sum of normal brain cells and corrupt braincells. '
                  "For comparing one's brain cells with others, only net brain cells is used."
        )
        embed.add_field(
            name='Normal Brain Cells',
            value="Alias: Positive Brain cells \nAs per the theory of Braincells, there are essentially two types of brain cells. One of them is termed as "
                  "'Normal Brain cell'. This brain cell is responsible for all the sensible and successful stuff you do! "
                  "Basically, the more you have these, the better. Represented by positive integer values."
        )
        embed.add_field(
            name='Corrupt Brain Cells',
            value="Alias: Negative Brain cells \nThe contrary of a Normal Brain cell is a 'Corrupt Brain Cell'. These are brain cells that are responsible for all your dumb and chaotic actions."
                  "The less you have them, the better. Represented by negative integer values."
        )
        embed.set_footer(text='What is Theory of Brain cells?\nJoin BRAINCELLS HQ to know more! Use /invite to join!'
                              "\nPS: Check the bot's status whenever you use this command!")
        await ctx.send(embeds=embed, ephemeral=True)

    elif selected_option == "2":
        embed = i.Embed(
            title='/brain-profile',
            description='Your brain profile! This contains two sections:',
            color=i.Color.from_hex(value='#fea4b7')
        )
        embed.add_field(
            name='BIO DATA',
            value='This contains your name, your nickname in this server and your date of joining'
        )
        embed.add_field(
            name='BRAIN DATA',
            value='This is the important section. BRAIN DATA contains your highest and lowest recorded **net brain cell** amount. It also contains the current amount as well.'
        )
        embed.set_footer(
            text='You cannot access your brain profile without using the command /braincells-count at least once!'
        )
        await ctx.send(embeds=embed, ephemeral=True)

    elif selected_option == '3':
        embed = i.Embed(
            title='/vote-invite',
            description='Provides a link (linked buttons) to invite Cellculator and a server invite to join Braincells HQ. Also contains a button to vote Cellculator!'
            , color=i.Color.from_hex(value='#fea4b7')
        )
        embed.set_footer('Theory of Braincells is Awesome!')
        await ctx.send(embeds=embed, ephemeral=True)

    elif selected_option == '4':
        embed = i.Embed(
            title='/cellculator',
            description='If you are curious about me, then this command will provide all the details you need to know!!'
            , color=i.Color.from_hex(value='#fea4b7')
        )
        embed.set_footer(
            text='Ever heard Autocell?'
        )
        await ctx.send(embeds=embed, ephemeral=True)

    elif selected_option == '5':
        await ctx.send('Coming soon', ephemeral=True)

    elif selected_option == '6':
        embed = i.Embed(
            title='/status',
            description='Provides multiple pieces of information!\n'
                        "This will tell whether I am online or under maintenance/update. This also tells about the new features/commands that are being worked on!"
            , color=i.Color.from_hex(value='#fea4b7')
        )
        embed.set_footer("Yes, even the easter eggs if you use this at the right time!")
        await ctx.send(embeds=embed, ephemeral=True)

    elif selected_option == '7':
        embed = i.Embed(
            title='/support',
            description='Provides links and contact information for support and updates!',
            color=i.Color.from_hex(value='#fea4b7')
        )
        embed.set_footer("Discord links didn't work with buttons so, we used vanity links!")
        await ctx.send(embeds=embed, ephemeral=True)

    elif selected_option == '8':
        embed = i.Embed(
            title='/updates',
            description='Contains released notes of new features and bug fixes of the current version of the bot.',
            color=i.Color.from_hex(value='#fea4b7')
        )
        embed.set_footer('Join the support server if you want to refer previous releases!')
        await ctx.send(embeds=embed, ephemeral=True)


@i.slash_command(name='cellculator', description='Curious about me?'
                 ) # another about me, as if the description was not enough!
async def cellculator(ctx: i.InteractionContext):
    embed = i.Embed(
        title='ABOUT CELLCULATOR',
        description='I see you, you are a curious one! Get ready for lots of information!'
        , color=i.Color.from_hex(value='#fea4b7')
    )
    embed.add_field(
        name='What am I?'
        ,
        value="'I am Cellculator, a discord bot!'\nCellculator is an automatic cell, dedicated to 'Theory of Braincells'. Cellculator can count the number of brain cells a person has! It watches over everyone and is able to record when one lost/gained braincells. Unfortunately, cellculator is very busy with counting and recording braincells. Hence, it cannot perform moderation! Cellculator comes with lots of easter eggs, keep looking for them!"
    )
    embed.add_field(
        name='Origins'
        ,
        value="Cellculator, originally known as 'Autocell', was created to count the number of brain cells a person has based on the 'Theory of Brain cells'. It was initially designed to be used only in the BRAINCELLS HQ community. In its early version, Autocell used simple code that relied on randomly generated numbers to provide values. Later, beta versions of the bot called 'Brain Tork' were released, which were more complex and relied on actual user behavior. However, there were many issues with Autocell, one of which was that it used prefixed commands instead of slash commands. To solve this, the development of Autocell with slash commands began. After being renamed to Cellculator, the bot's first command, '/calculatebraincells', was released. This command was eventually renamed to '/braincells-count' and has been thoroughly debugged. Despite the bot's improvements, we cannot disclose the secrets of how cellculator works."
        , inline=True)
    embed.add_field(
        name='Contributors'
        , value="Developer: Shadow's Lure#9799 and alt"
                "\nTesters: Arafluch#9781, rainy#9495, Mustiyayeet#9974, IMPERIAL#6959, Maniac#2469, QuantomStudios👑#2889"
                "\nAlso, thank you to all who provided valuable feedbacks!"
    )
    embed.set_footer('PS: Thank you testers for putting up with my mess!')
    await ctx.send(embeds=embed)


@i.slash_command(name='support', description='A little too lost? Contact us directly and stay UPDATED!!'
                 ) # Just another normal simple command with buttons
async def support(ctx: i.ComponentContext):
    embed = i.Embed(
        title='SUPPORT',
        color=i.Color.from_hex(value='#fea4b7')
    )
    embed.add_field(name='Contact',
                    value='We are here to help! Reach us directly via email : `sh4dowslure@gmail.com`\nOR by joining our support server!')
    embed.add_field(name='Updates',
                    value='Stay up to date with the development of Cellculator! Join the Support server and follow the channel `#cellculator-status`!')
    embed.set_footer(text='Vanity URL through "dsc.gg" (not a Discord domain, be careful with external links).')

    components: list[i.ActionRow] = [i.ActionRow(
        i.Button(
            style=i.ButtonStyle.URL,
            label='Join the support server!',
            url='https://dsc.gg/braincellshq'
        ),
        i.Button(
            style=i.ButtonStyle.URL,
            label='Follow the channel and stay updated!',
            url='https://dsc.gg/bchqupdate'
        )
    )]

    await ctx.send(embeds=embed, components=components)


@i.slash_command(name='updates', description='All the new updates info are here!'
                 ) # A very basic embed send command which retireves the mebd details from another file
async def updates(ctx: i.InteractionContext):
    await ctx.send(embeds=update_embed)


# The following code was made possible by my agony, yes my agony is the sponser of this project!

@i.slash_command(name = 'modify',
                sub_cmd_name= "alerts",
                sub_cmd_description= "Enable/disable alerts whenever a person looses/gains braincells",
                default_member_permissions= i.Permissions.MANAGE_MESSAGES
                ) # Command name "/modify alerts"

# Now this command is a little unique, it just asks a simple question "DO YOU WANT TO BE NOTIFIED WHEN YOU GET DUMB?".

@i.slash_option(
   name = 'value', 
   description = 'Disabled or Enable this feature!',
   required = True, 
   opt_type = i.OptionType.INTEGER,
   choices=[
      i.SlashCommandChoice(name='Enable', value=0),
      i.SlashCommandChoice(name='Disable', value=1)
   ]
)
# Options REEEEE
@i.slash_option(
   name='channel',
   description='You can limit the alerts to one channel if you want to',
   required=False,
   opt_type=i.OptionType.CHANNEL
)
# keep in mind that the OptionType.CHANNEL includes categories
async def chlevels(ctx: i.SlashContext, value:int, channel:i.ChannelType.GUILD_TEXT = None): # 'value' is option values

   # checking if the channel id alrdy exists in the database or not
   if m.retrieve_server_value_channel_random_time(server_id=int(ctx.guild.id)) is None:
      m.add_server_value_and_channel(server_id=int(ctx.guild.id), value=1)
      # I know the function sounds like it adds channel too, but trust me we are only adding the server_id at the moment
      # This reduces the database size by not keeping every server ID until the command is used
   else:
      pass

   if value == 1:  # 1 is true and 0 is false, but not HERE!
      m.update_value_and_channel(server_id=int(ctx.guild_id),value=1, channel_id=None)
      await ctx.send('Disabled Change in Brain Cells alerts!')
      return
   
   # checking if the given channel is actually a text channel and not a category by sending a message 
   try:
      await channel.send(f'This channel has been specifically set up to recive change in Brain Cells alerts!')
   except Exception:
      if not channel:
         pass
      else:
         await ctx.send('Please select an actual `TEXT CHANNEL` with `SEND MESSAGES` permission enabled for Cellculator.')
         return

   if value == 0:
      if not channel:
         m.update_value_and_channel(server_id=int(ctx.guild.id), value=0)
         await ctx.send('Enabled change in Brain Cells alerts everywhere!')
         return
      else:
         m.update_value_and_channel(server_id=int(ctx.guild.id),value=0, channel_id=int(channel.id))
         await ctx.send(f'Enabled change in Brain Cells alerts in {channel.mention}!')

# this is what enabling chaos does
def randomise():
   random_msg_no = random.randint(22,69)
   return random_msg_no
    # I created a raomise function since I was too lazy to type one line of code
random_no = randomise() # now we have a random no

@i.listen()
async def on_message_create(event):
   # checking if message is sent by a bot
   if event.message.author.bot:
      return 
   
   # adding a new variable retriev for future use (wrong spelling ik)
   try:
      retriev = m.retrieve_server_value_channel_random_time(server_id = event.message.guild.id)
   except TypeError:
      return

   # checking if the server exists in database
   if m.retrieve_server_value_channel_random_time(server_id = event.message.guild.id) is None:
      return

    # Yes, I realize that I could have made the above two checks in a single check

   # getting stuff from database
   random_msg_no = retriev['random_no']
   last_message_time = retriev['last_sent_time']
   message_no = retriev['message_no']

    # the following mess works on two variables, random_msg_no and last_message_time.
    # A random no is generated which is basically the target, then the bots counts the number of messages
    # if no of messages equals random generated number then it may be said that a person's brain cell count has changed.

   global random_no
   if random_msg_no == 0:
      random_msg_no = random_no # what I said at line 596
      m.update_random_no(server_id = event.message.guild.id, random_no= random_msg_no)
      

   if  last_message_time==0: # if time still has the default value of 0
      m.update_last_time(server_id= event.message.guild.id, last_sent_time=time.time())

   # checking wether alerts are even enabled or not (I should have put this earlier)
   if retriev['value'] == 1:
      return

   current_time = time.time() # noting time
   elapsed_time = current_time - last_message_time

   if elapsed_time > 120:
      m.update_message_no(server_id=event.message.guild.id, message_no=0)
   else:
      message_no +=1
      m.update_message_no(server_id=event.message.guild.id, message_no=message_no)

   m.update_last_time(server_id=event.message.guild.id, last_sent_time=current_time)


   if message_no == random_msg_no: # What I said at line 597
      m.update_message_no(server_id=event.message.guild.id, message_no=0)
      random_no = randomise()
      m.update_random_no(server_id = event.message.guild.id, random_no= random_no)
      
      # defining some stuff else python will sue me
      user_id = event.message.author.id
      net=0
      normal=0
      corrupt=0
      high=0
      low = 0
    
      # getting data
      if get_user_data(user_id=f'{user_id}') is not None:
         user_data = get_user_data(user_id=f'{user_id}')
         user_history = get_user_history(user_id=f'{user_id}')
         net = user_data['random_int']
         normal = user_data['int1']
         corrupt = user_data['int2']
         high = user_history['high']
         low = user_history['low']
         existence = 1
      else:
         existence = 0

      # doing prior calculation considering user exists
      luck = random.randint(0,1) 
      if luck == 1:
         net +=1
         if random.randint(0,1) == 0:
            normal += 1
            prompt = f"{positive_prompt_title()[0]}"
            desc = f'{event.message.author.mention} gained a normal brain cell!'
         else:
            corrupt += 1
            prompt = f"{positive_prompt_title()[0]}"
            desc = f'{event.message.author.mention} lost a corrupt brain cell!'

      else:
         net = net - 1
         if random.randint(0,1) == 0:
            normal = normal - 1
            prompt = f"{negative_prompt_title()[0]}"
            desc = f'{event.message.author.mention} lost a normal brain cell!'

         else:
            corrupt -= 1
            prompt = f"{negative_prompt_title()[0]}"
            desc = f'{event.message.author.mention} gained a corrupt brain cell!'

      # if user doesn't exists      
      if existence == 0:
         if random.randint(0,1) == 1:
            title = f"{positive_prompt_title()[0]}"
            descr = f"{event.message.author.mention}Your net brain cell did go up! But it seems you don't have a brain profile! Please use `/braincell-count` to create a brain profile!"
         else:
            title = f"{negative_prompt_title()[0]}"
            descr = f"{event.message.author.mention}Your net brain cells went down! But don't fret! You can always know when it goes up and you don't have a brain profile yet! Please use `/braincell-count` to create a brain profile!"
         
         embed = i.Embed(
            title= title,
            description= descr,
            color=i.Color.from_hex(value = '#fea4b7')
         )
      
      # if user exists and adjusting calculation for invalid values
      elif existence == 1:
         if normal < 0:
             net = net + 2
             normal = normal + 2
             desc = f'{event.message.author.mention} gained a normal brain cell!'
         if corrupt > 0:
             net = net - 2
             corrupt = net - 2
             desc = f'{event.message.author.mention} gained a corrupt brain cell!'
         if net > high:
            high = net
         if net < low:
            low = net
         update_user_data(user_id=f'{event.message.author.id}', random_int= net, int1=normal, int2=corrupt, high=high, low=low)
         embed = i.Embed(
            title= prompt,
            description=f'{desc}\nNow your net brain cell count is `{net}`!',
            color = i.Color.from_hex(value = '#fea4b7')
         )
      
      channel_id = retriev['channel_id'] # this is where we use retriev

      if channel_id is None:
         await event.message.channel.send(embed=embed)
      else:
         channel = bot.get_channel(channel_id=channel_id)
         await channel.send(embed=embed)


bot.start('MY_BOT_TOKEN_NOT_YOURS')

# Cellculator v1.0.0 brought to you by my agony