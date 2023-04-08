from rich.prompt import Confirm
from rich.prompt import IntPrompt

def main():
    playlist = Confirm.ask('Enable playlist downloading by default?')
    tag = Confirm.ask('Enable automatic tagging by default?')
    experimental_tag = Confirm.ask('Enable experimental tagging by default?')
    manual_tag = Confirm.ask('Enable manual tagging by default?')

    # the limit needs to be more than 0
    limit_input = IntPrompt.ask('Set the maximum songs to download at once:', default=20)
    if limit_input > 0:
        dl_limit = limit_input

    conf = {'playlist': playlist, 'tag': tag, 'experimental': experimental_tag, 'manual-tag': manual_tag, 'dl-limit': dl_limit}
    return conf

