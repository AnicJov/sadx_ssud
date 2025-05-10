# SADX Small Story Ultimate Draft Manager

This is a Python & PyQt6 program as well as a Discord bot for use in managing and displaying the Draft phase for the Small Story Ultimate Draft Sonic Adventure DX tournament.

The details of the tournament itself can be found [here](https://docs.google.com/document/d/1ISBdXpmEOfCOtP3HH7BlhTRYK97nQbVvK2tPNjKH2P4/edit?usp=sharing).

The program consists of a main QT application window that displays the current status of the Draft and provides controls for interaction/management (`display.py`), and a discord bot that provides a convenient interface to manage the draft by authorized Discord users, and prompting the runners themselves during the Draft phase with choices in the form of clickable buttons (`dc_bot.py`). 

LiveSplit split files are also automatically generated based on the choices (`splits.py`).

The two parts of the program (QT app and Discord bot) are connected and synchronized by a shared `DraftManager` object and a shared main event loop. (`draft.py`, `main.py`)

This repository also includes some statistics calculations based on [SRC SADX leaderboards](https://www.speedrun.com/sadx) found in `stats.py`. This is not part of the main program and can be run separately by invoking the script directly. (`python src/stats.py`)

# Usage

## Running from binary release

1. Download the archive appropriate for your operating system from the [releases section](https://github.com/AnicJov/sadx_ssud/releases/latest) of this repository.
1. Extract the archive.
1. If using the Discord bot part [configure a new application](https://discord.com/developers/docs/quick-start/getting-started) in [Discord's developer portal](https://discord.com/developers).
1. Configure settings in the extracted `config.txt` file.
    ```
    DISCORD_TOKEN=<Your Discord bot token>

    AUTHORIZED_USERS=<Comma separated list of Discord user IDs>

    PACEKEEPING_CHANNEL=<Channel ID>

    COMMAND_PREFIX=<Prefix for commands e.g. !>
    ```
1. Run `ssud.exe` on Windows or `ssud` on other systems.

## Running from source

### Linux & MacOS

Prerequisites: git, python3.13+

1. Open a Terminal window
1. Clone the repository and enter the cloned directory
    ```sh
    git clone https://github.com/AnicJov/sadx_ssud.git && cd sadx_ssud
    ```
1. Create a Python virtual environment
    ```sh
    python -m venv venv
    ```
1. Activate the virtual environment
    ```sh
    chmod +x venv/Scripts/activate && venv/Scripts/activate
    ```
1. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
1. Run the program
    ```sh
    python src/main.py
    ```
1. (Optional) Run other scripts
    ```sh
    python src/stats.py
    ```
    ```sh
    python src/splits.py
    ```
1. (Optional) Build executable
    ```sh
    pyinstaller ssud.spec
    ```

### Windows

Prerequisites: [Git](https://git-scm.com/downloads/win), [Python 3.13+](https://www.python.org/downloads/windows/), [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

1. Open a PowerShell window
1. Clone the repository and enter the cloned directory
    ```ps1
    git clone https://github.com/AnicJov/sadx_ssud.git && cd sadx_ssud
    ```
1. Create a Python virtual environment and activate it
    ```ps1
    python -m venv venv && .\venv\Scripts\Activate.ps1
    ```
    > Note:
    > It may be required to change the execution policy on your system in order to activate the virtual environment
    >
    > `PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
1. Install dependencies
    ```ps1
    pip install -r requirements.txt
    ```
1. Run the program
    ```ps1
    python src/main.py
    ```
1. (Optional) Run other scripts
    ```ps1
    python src/stats.py
    ```
    ```ps1
    python src/splits.py
    ```
1. (Optional) Build executable
    ```ps1
    pyinstaller ssud.spec
    ```

## Using the Discord bot

1. Invite the Discord bot to your server.
1. Make sure that the bot has access to read and write messages to your desired channels.
1. Make sure the desired users are assigned to be authorized to manage the draft by adding their Discord user IDs to `config.txt`.
    (Additional authorized users can be added/removed using `!auth` commands. Note that these changes currently don't persist between program runs.)
1. Start the program (Either run `ssud.exe`/`ssud` or run from source `python src/main.py`)
1. Start a match by issuing the `!start` command, specifying the user IDs of the two runners.
    ```
    !start <Player 1 ID> <Player 2 ID>
    ```
1. Use the `!spin` command to spin the random choice wheel.
1. Players are then prompted for their ban/pick choices. Manual choices can be made by authorized users using the `!choice` command.
    ```
    !choice <Name of Story>
    ```
1. After all choices have been made the bot sends splits files to the same channel and sends pacekeeping splits to a channel specified by the `PACEKEEPING_CHANNEL` setting inside `config.txt`
1. Use the `!countdown` command to count the players down once they're ready to start the race.
    ```
    !countdown <(Optional) number of seconds (Default is 5)>
    ```
1. Then once the race is over you can use `!reset` to reset the draft. Then you can start another match with the `!start` command again.

For other commands and additional help you can issue the `!help` command.

# Help & Contributing

If you need help with anything feel free to reach out to me on Discord `_anic`.

If you want to contribute to the project you can submit issues or pull requests on this repository.

# Credits & Legal

The code inside the `src/` directory is written by me ([Anic](https://github.com/AnicJov)) with great help from the SAESR Events team, especially Labrys and Drum, and is licensed under the [GPLv3 software license](https://github.com/AnicJov/sadx_ssud/blob/main/LICENSE). Huge thanks to the entirety of the SAESR team for the continued help on this project. :^)

The logos under the `res/logo/` directory are commissioned by me (Anic) and are created by Mimmeil for the use in this project and the tournament as a whole, and all rights for them are reserved by Mimmeil.

Sonic the Hedgehog and the assets in the root of the `res/` directory are property of Sega.