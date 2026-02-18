1. Ensure that logged in user is Blue.
1. In the left-hand side navigation, select `CAMPAIGNS > agents`.
1. Press the button `+Deploy an agent`.
1. Choose `Sandcat` agent.
1. Under Platform, choose the remote host's Operating System: Windows
1. Update the `app.contact.http` value to specify an IP address of the Caldera server that is reachable from the remote system (e.g. `10.0.2.2`). Keep the port value unchanged.
1. In the `psh` text area click the `Copy` button to copy the displayed PowerShell command to your clipboard. This command will instruct the agent to communicate over a HTTP channel.
1. On the Windows remote system, open a terminal with a shell.
1. Paste the copied command into the shell, manually change group name to `blue` and execute it.
1. Go back to Caldera and close the agent options window.
1. Wait for the agent to appear in the `Agents` table.
1. Change the group name from `blue` to `cert-win`, click save settings if needed.
1. Task completed.