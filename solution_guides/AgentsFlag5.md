1. Open a shell in a terminal outside of CALDERA
1. In that shell, navigate to your caldera folder: `cd /path/to/caldera`
1. Run `grep -R 'command: whoami' plugins/stockpile/data/abilities` at look for matching files.
1. Open `plugins/stockpile/data/abilities/discovery/c0da588f-79f0-4263-8998-7496b1a40596.yml`
  in a text editor and confirm that it runs `whoami` as a command.
1. Copy the UUID portion of the filename to your clipboard: `c0da588f-79f0-4263-8998-7496b1a40596`
1. Open the Navigate menu.
1. Select `Campaigns > agents`.
1. On the left side of the window, click on `BOOTSTRAP ABILITIES`
1. Paste the UUID into the text box
1. Press the `Save` button.
1. Task completed