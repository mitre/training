1. Ensure that before starting up agent, type `sudo su` in your server terminal to run as root user. Proceed to starting up agent under Blue user.
1. In the left-hand side navigation, select `CAMPAIGNS > agents`.
1. Press the button `+Deploy an agent`.
1. Choose `Sandcat` agent.
1. Under Platform, choose the remote host's Operating System: Linux
1. Update the `app.contact.http` value to specify an IP address of the Caldera server that is reachable from the remote system (e.g. `10.0.2.2`). Keep the port value unchanged.
1. In the `sh` text area click the `Copy` button to copy the displayed shell command to your clipboard. This command will instruct the agent to communicate over a HTTP channel.
1. On the Linux remote system, paste copied command into the shell. Before executing, change `-group red -v`` TO -group blue -v` and then execute it. For example, your pasted command should look something like this: `server="http://0.0.0.0:8888";curl -s -X POST -H "file:sandcat.go" -H "platform:linux" $server/file/download > splunkd;chmod +x splunkd;./splunkd -server $server -group blue -v`
1. Go back to Caldera and close the agent options window.
1. Wait for the agent to appear in the `Agents` table.
1. Task completed.