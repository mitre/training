1. Log into CALDERA as a `blue` group user (by default, the username is `blue`).
1. Open the Navigate menu.
1. Select `Campaigns > agents`.
1. Press the button to deploy an agent.
1. Choose 54ndc47 (Sandcat) agent.
1. Choose Linux platform.
1. Update the `app.contact.http` value to specify an ip address (keep the port) that is reachable from a remote system (i.e., not `0.0.0.0`).
1. Select and copy the second command ("Deploy as a blue-team agent") to your clipboard. This command will instruct the agent to communicate over an HTTP channel.
1. On a remote system, open a terminal window with a shell.
1. Paste the copied command into the shell and execute it.
1. Go back to CALDERA and close the agent options window.
1. Wait for the agent to appear in the agents table.
1. Task completed.