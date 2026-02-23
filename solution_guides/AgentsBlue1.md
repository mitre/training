1. Ensure that before starting up agent, type `sudo su` in your server terminal to run as root user. Proceed to starting up agent under Blue user.
1. In the left-hand side navigation, select `CAMPAIGNS > agents`.
1. Press the button `+Deploy an agent`.
1. Choose `Sandcat` agent.
1. Under Platform, choose the remote host's Operating System: Linux
1. Update the `app.contact.http` value to specify an IP address of the Caldera server that is reachable from the remote system (e.g. `10.0.2.2`). Keep the port value unchanged.
1. In the `sh` text area click the `Copy` button to copy the displayed shell command to your clipboard. This command will instruct the agent to communicate over a HTTP channel.
1. Scroll down on the deployment options until you see the one labeled "Deploy as a blue-team agent instead of red". Click the `Copy` button to copy the displayed bash command to your clipboard. This command will execute the agent in the `blue` group in the background.
1. On the Linux remote system, paste copied command into the shell and execute it.
1. Go back to Caldera and close the agent options window.
1. Wait for the agent to appear in the `Agents` table.
1. Task completed.