# eco (Explain Cli Options)
eco is a no-further-dependency python script that explains any cli options you throw at it <3 (hopefully!)

```sh
$ eco rsync -rlptgoD --progress
--archive, -a            archive mode is -rlptgoD (no -A,-X,-U,-N,-H)
--recursive, -r          recurse into directories
--links, -l              copy symlinks as symlinks
--perms, -p              preserve permissions
--times, -t              preserve modification times
--group, -g              preserve group
--owner, -o              preserve owner (super-user only)
-D                       same as --devices --specials
--progress               show progress during transfer
-P                       same as --partial --progress

$ eco cargo add --dev
Results main command
    add         Add dependencies to a manifest file

Results subcommand
      --dev
          Add as development dependency
```

## How-to
### Install
Optional requirements\*: [man](http://man-db.nongnu.org/)
```sh
# Download to .local/bin/eco (user-scoped) 
curl https://raw.githubusercontent.com/Denperidge/explain-cli-options/refs/heads/main/eco.py -o ~/.local/bin/eco
chmod +x ~/.local/bin/eco
```

\*: if man is not installed, only the default --help mode will be used

### Usage
Minimum required Python version: 3.6

```sh
usage: eco.py [+h] [++debug] [++man] [++line] command args [args ...]

eco is a no-further-dependency python script that explains any cli options you
throw at it <3 (hopefully!)

positional arguments:
  command      command which needs explaining (for example, tar)
  args         args for the command you want explained (for example, -cvzf)

options:
  +h, ++help   show this help message and exit
  ++debug, +d  show debug output
  ++man, +m    prioritise searching man contents over --help output
  ++line, +l   add line index to output

```

### Development
#### Repo setup
Requirements: [bash](https://www.gnu.org/software/bash/), [uv](https://docs.astral.sh/uv)
```sh
git clone https://github.com/Denperidge/explain-cli-options.git
cd explain-cli-options/development/

nix-shell  # For non-nix users, instead ensure the listed requirements are available in PATH

chmod +x dev.sh  # Make dev.sh executable
./dev.sh --help  # Show help
```

#### Generate documentation
```sh
./dev.sh -r  # or --readme
```

#### Run tests
Extra requirements: [rsync](https://github.com/RsyncProject/rsync), [tar](https://www.gnu.org/software/tar/), [cargo](https://crates.io/), [docker-compose](https://github.com/docker/compose)

```sh
./dev.sh -t  # or --test
```

## Explanation
### Terminology
- **docs**: list of lines from `{command} --help` or `man {command}`
- **command**: an executable command. For example: `npm`, `cargo`...
- **subcommand**: a command within a command. For example: `npm install` `cargo add`

### eco +h/++help instead of eco -h/--help
This makes sure that eco's args don't get mixed up with regular CLI arguments

### EXPECTED_ variables in tests
The EXPECTED_ variables are global for readability & writeability; no messing with any indenting aside from the actual command output

## License
While credit and contributions are appreciated, this project is released into the public domain under [the Unlicense](LICENSE).
