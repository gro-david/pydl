from pydl import console


def main(tags_in):
    tags_in["artist"] = console.input(
        "Enter the [bold cyan]ARTIST[/bold cyan] name. [italic][Leave empty to skip][/italic]"
    )
    tags_in["album"] = console.input(
        "Enter the [bold cyan]ALBUM[/bold cyan] name. [italic][Leave empty to skip][/italic]"
    )
    tags_in["title"] = console.input(
        "Enter the [bold cyan]TITLE[/bold cyan] of the song. [italic][Leave empty to skip][/italic]"
    )
    tags_in["genre"] = console.input(
        "Enter the [bold cyan]GENRE[/bold cyan] of the song. [italic][Leave empty to skip][/italic]"
    )

    # loop over each value in the dictionary and add it to the topop list if empty
    topop = []
    for key in tags_in.keys():
        if tags_in[key] == "":
            topop.append(key)

    # we only want to prompt the user if there is something to complete
    if len(topop) > 0:
        # ask the user until they deliver a valid input if that is the case we break out of the loop
        while True:
            complete = console.input(
                "Should the empty fields be automatically filled in? [italic][Y/n][italic]"
            )

            if complete.lower() == "y" or complete == "":
                for key in topop:
                    tags_in[key] = None
                break

            elif complete.lower() == "n":
                # pop empty items
                for key in topop:
                    tags_in.pop(key)
                break

            else:
                console.print("Invalid input", style="bold red")
