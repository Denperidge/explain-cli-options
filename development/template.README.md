# eco (Explain Cli Options)
eco is a no-further-dependency python script that explains any cli options you throw at it <3 (hopefully!)

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
```sh
cd development
nix-shell  # For non-nix users, ensure vermin is available in PATH
python mkdocs.py
```
