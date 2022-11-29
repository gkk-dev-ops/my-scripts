# my-scripts

Scripts improving daily workflows.

## Usage

```bash
cd ~/
git clone git@github.com:gkk-dev-ops/my-scripts.git bin
```

Then add following lines to your .profile or .bashrc

```bash

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

```
