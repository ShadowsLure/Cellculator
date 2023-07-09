import interactions as i

version = 1.1

fixes = ''

v1_0 = 'This is the first official release of Cellculator!' \
      f'\n\n v{version} comes with three major features:' \
      f'\n\n1. Getting your braincells counted - This feature can be experienced by using a dedicated command for it' \
      f', `/braincells-count`!' \
      f'\n\n2. Knowing the reason as to why you lost/gained braincells - This feature is bundled along with the' \
      f' the previous feature in a single command, `/braincells-count`. Reasons will only be shown after the command ' \
      f'is executed for the 2nd time by the user.' \
      f'\n\n3. Recording the highest and lowest number of braincells a user had - This feature can be accessed by using' \
      f' the command `/brain-profile`!' \
      f'\n\nThere are multiple other required commands, use `/help` for more details on them.'\
      '06 May 2023'

new = 'Feature update 1.1!'\
    f'\n\n v{version} is a feature update of cellculator! It brings in the following feature and some minor changes!'\
    f'\n\n1. Cellculator sends an alert whenever someone in a conversation looses/gains braincells!'\
    ' You will need to enable this feature, by defualt it is turned off for every server, you can enable it'\
    ' by using the command `/modify alerts`!'\
    f'\n\n2. Minor changes:'\
    f'\n    - Changed command name for `/braincells-count` and `/brain-profile` to `/brain cell count` and `/brain profile`.'\
    f'\n    - Adjusted to new username system'


update_embed = i.Embed(
    title='UPDATES!',
    description=f'Cellculator v{version} release notes',
    color=i.Color.from_hex(value='#fea4b7')
)
update_embed.add_field(name="What's New!",
                       value=f"{new}"
                       )
update_embed.set_footer(text='Release date: 18 June 2023')
if len(fixes) > 1:
    update_embed.add_field(name="Bug Fixes",
                           value=f'{fixes}')
