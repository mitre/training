1. Open a shell in a terminal outside of CALDERA
2. In that shell, navigate to your caldera folder: `cd /path/to/caldera`
3. Run `grep -R 'command: whoami' plugins/stockpile/data/abilities` at look for matching files.
4. Open `plugins/stockpile/data/abilities/discovery/c0da588f-79f0-4263-8998-7496b1a40596.yml`
  in a text editor and confirm that it runs `whoami` as a command.
5. Copy the Name portion of the yml ability file to your clipboard: `Identify active user`
6. Open the Navigate menu.
7. Select `Campaigns > agents`.
8. Select Configuration and click the '+' next to Bootstrap Abilities
9. Paste the ability name in the text search box, and select the found ability
10. Press the `Save` button.
11. Task completed