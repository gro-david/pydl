# type: ignore
from rich.prompt import Confirm
from rich.table import Table
from rich.console import Group
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

import rich_click as rclick

from pytube import YouTube as YT
from pytube import Playlist


import pydl
from pydl import console
from libraries import read_conf

queue = []
# this can be something like "Downloading" or "Converting"
status_text = ""
live_running = False
queue_progress = 0
live = Live()

table = Table(title="Queue", expand=True)
table.add_column("Index")
table.add_column("Title")
table.add_column("Playlist")
table.add_column("Path")
table.add_column("URL")


def add_to_queue(
    url,
    path,
    playlist,
    limit,
    index,
):
    if index == None:
        queue.append(QueueItem(url, path, playlist, limit))
    else:
        queue.insert(int(index), QueueItem(url, path, playlist, limit))


def get_queue():
    for i, _ in enumerate(queue):
        table.add_row(
            str(i),
            queue[i].title,
            "Yes" if queue[i].is_playlist == True else "No",
            queue[i].path,
            queue[i].url,
        )
    console.print(Panel(table))
    create_table()


# removes a queue item based on either index, title, or url, using find_queue_items
def remove_from_queue(index=None, url=None, title=None):
    if (index is None) and (url is None) and (title is None):
        console.print(
            "[bold red]Error: At least one parameter must be specified.[/bold red]"
        )
        return
    elif sum(p is not None for p in (index, url, title)) > 1:
        console.print(
            "[bold red]Error: Only one parameter can be specified.[/bold red]"
        )
        return
    else:
        if index != None:
            if Confirm.ask(f"Remove [bold]{queue[int(index)].title}[/bold]?"):
                queue.pop(int(index))
        else:
            index = find_queue_item(title, url)
            if index == None:
                console.print(
                    "[bold red]Error: No queue item with the specified criteria found.[/bold red]"
                )
            elif Confirm.ask(f"Remove [bold]{queue[int(index)].title}[/bold]?"):
                queue.pop(int(index))


# returns the first occurence of the QueueItem based on title/url,
# returns None if the input is invalid or there are no items with the specified criteria
def find_queue_item(title=None, url=None):
    if title != None and url != None:
        console.print(
            "[bold red]Do not specify 'title' and 'url' at the same time![/bold red]"
        )
        return None
    elif title == None and url == None:
        console.print("[bold red]Specify either 'title' or 'url'![/bold red]")
        return None
    for queue_item in queue:
        if queue_item.title == title or queue_item.url == url:
            return queue.index(queue_item)
    return None


def start_queue():
    global live_running
    global live
    global queue_progress
    live_running = True
    with Live(
        create_table_with_status(0),
        auto_refresh=True,
        transient=True,
        refresh_per_second=5,
        console=console,
    ) as _live:
        live = _live
        if not live_running:
            _live.stop()
        for i, item in enumerate(queue):
            queue_progress = i
            _live.update(create_table_with_status(i))
            pydl.download_logic(
                input=item.url,
                path=item.path,
                playlist=item.playlist,
                limit=item.limit,
                status=False,
            )
    live_running = False


def create_table_with_status(i) -> Panel:
    _table = Table(title="Queue", expand=True)
    _table.add_column("Index")
    _table.add_column("Title")
    _table.add_column("Playlist")
    _table.add_column("Path")
    _table.add_column("URL")
    for j, _ in enumerate(queue):
        _table.add_row(
            f"[bold green]► {j}[/bold green]" if i == j else str(j),
            queue[j].title,
            "Yes" if queue[i].is_playlist == True else "No",
            queue[j].path,
            queue[j].url,
        )

    _text = Text(status_text, style="bold green")
    _group = Group(_table, Panel(_text))
    return Panel(_group)


def clear_queue():
    if Confirm.ask(
        "[bold red]You are about to clear the queue! [/bold red][bold]Are you sure?[/bold]"
    ):
        queue.clear()


# reset the table
def create_table():
    global table
    table = Table(title="Queue")
    table.add_column("Index")
    table.add_column("Title")
    table.add_column("Path")
    table.add_column("URL")
    return table


def set_status_text(text):
    global status_text
    status_text = text
    update_live()


def update_live():
    global live
    global queue_progress
    live.update(create_table_with_status(queue_progress))


# stop the live display
def error():
    global live_running
    live_running = False


class QueueItem:
    def __init__(
        self,
        url,
        path,
        playlist=read_conf.main()["Flags"]["playlist"],
        limit=read_conf.main()["General"]["dl-limit"],
    ):
        self.url = url
        self.path = path
        self.title = YT(url).title if not "playlist?" in url else Playlist(url).title
        self.is_playlist = True if "list=" in url and playlist else False
        self.playlist = playlist
        self.limit = limit
