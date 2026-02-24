1. Ensure that logged in user is Blue.
1. In the left-hand side navigation, select `CAMPAIGNS > agents`.
1. Press the button `+Deploy an agent`.
1. Choose `Sandcat` agent.
1. Under Platform, choose the remote host's Operating System: Windows
1. Update the `app.contact.http` value to specify an IP address of the Caldera server that is reachable from the remote system (e.g. `10.0.2.2`). Keep the port value unchanged.
1. Scroll down the deployment options until you see the one labeled "Deploy as a blue-team agent instead of red". Click the `Copy` button to copy the displayed PowerShell command to your clipboard. This command will execute the agent in the `blue` group in the background.
1. On the Windows remote system, open a PowerShell terminal session.
1. Paste the copied command into the PowerShell session and execute it.
1. Go back to Caldera and close the agent options window.
1. Wait for the agent to appear in the `Agents` table.
1. Task completed.
