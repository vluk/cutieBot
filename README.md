# cutieBot

A bot for the messaging service Discord written in Python that retrieves various math contest problems, among other things.

## Getting Started

If you have a Discord server, you can invite the bot using [this invite link.](https://discordapp.com/oauth2/authorize?client_id=334159122041929738&scope=bot). This is the recommended course of action. If you want to run the bot on your own Linux server, here are the instructions.

### Prerequisites

Aside from the Python packages listed in `requirements.txt`, you will need:
```
Python >= 3.5
latexmk >= 4.55
Asymptote >= 2.44
ImageMagick >= 7.0
```
[Downloading Python](https://wiki.python.org/moin/BeginnersGuide/Download)

[Downloading latexmk](https://mg.readthedocs.io/latexmk.html)

[Downloading Asymptote](http://asymptote.sourceforge.net/)

[Downloading ImageMagick](https://www.imagemagick.org/script/download.php)

### Installing

First, clone the repository.
```
git clone git@github.com:vluk/cutieBot.git
```
Next, go into the directory.
```
cd cutieBot
```
Next, download all the necessary Python packages.
```
pip3 install -r requirements.txt
```
Make a `config.ini` file in the root directory and put a [Discord bot token.](https://discordapp.com/developers/docs/intro).
Example:
```
[tokens]
DISCORD_TOKEN_0: [your token here]
```
The bot should now be ready.

### Usage

To run the bot, just type in the root directory
```
python3 bot.py
```

Invite the bot to a [server](https://github.com/jagrosh/MusicBot/wiki/Adding-Your-Bot-To-Your-Server), then type in ?help for a list of the functions the bot has.


