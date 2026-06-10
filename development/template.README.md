# eco (Explain Cli Options)
eco is a no-further-dependency python script that explains any cli options you throw at it <3 (hopefully!)

```sh
{usage}
```

## How-to
### Install
```sh
# Download to .local/bin/eco (user-scoped) 
curl https://raw.githubusercontent.com/Denperidge/explain-cli-options/refs/heads/main/eco.py -o ~/.local/bin/eco
chmod +x ~/.local/bin/eco
```

### Usage
{vermin}

```sh
{help}
```

### Development
#### Clone
```sh
git clone https://github.com/Denperidge/explain-cli-options.git
cd explain-cli-options
```

#### Generate documentation
Extra requirements: [vermin](https://github.com/netromdk/vermin)

```sh
cd development
nix-shell  # For non-nix users, ensure vermin is available in PATH
python main.py -r  # or --readme
```

#### Run tests
Extra requirements: [uv](https://docs.astral.sh/uv), [passwd](https://github.com/shadow-maint/shadow), [rsync](https://github.com/RsyncProject/rsync) [man](http://man-db.nongnu.org/)

```sh
cd development
nix-shell  # For non-nix users, ensure uv is available in PATH
uv run pytest
python main.py -t  # or --test
# The python version is an alternative notation, which relaunches using uv & invokes pytest from code
```

## Explanation
### eco +h/++help instead of eco -h/--help
This makes sure that eco's args don't get mixed up with regular CLI arguments

## License
While credit and contributions are appreciated, this project is released into the public domain under [the Unlicense](LICENSE).
