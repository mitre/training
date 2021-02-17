### Launching the agent
1. Open the Navigate menu.
1. Select `Campaigns > agents`.
1. Press the button to deploy an agent.
1. Choose Manx agent.
1. Choose Linux platform.
1. Update the `app.contact.http` value to specify an ip address of `127.0.0.1` (keep the port). This is for downloading the agent binary.
1. Update the `app.contact.tcp` value to specify an ip address of `127.0.0.1` (keep the port). This is for the agent-C2 communication channel.
1. Select and copy the first command to your clipboard. This command will instruct the agent to communicate over a TCP channel.

### Running two remote shell commands
1. On your local system and outside of CALDERA, open a shell in a terminal.
1. Paste the copied command and execute it.
1. Wait for the agent to appear in the agent table.
1. Open the Navigate menu.
1. Select `Plugins > manx`
1. Select the Agent session from the first drop-down. This should populate the remote shell window with a prompt.
1. In the remote shell, type `whoami` and press enter.
1. In the remote shell, type `uname -a` and press enter.

### Running Hunter operation
1. Open the Navigate menu.
1. Select `Campaigns > operations`.
1. Press the toggle button so that it changes from View to Add
1. Enter an operation name of `Manx Flag 0`
1. Click on `Basic Options`
1. Select `red` from the groups list
1. Select `Hunter` from the adversary list
1. Select `Auto-close operation` from the close options list.
1. Press the `Start` button.
1. Wait for the operation to complete. The operation status will change to `FINISHED`. This may take several minutes.
1. Task completed.