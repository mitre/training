1. Ensure that the blue agent from the previous flag is running on a remote system
   and can communicate with the CALDERA server.
1. On your local system, open a shell in a terminal.
1. Using `netcat`, open a listening TCP socket on port 7011: `nc -l -p 7011`
1. On the remote system running the blue agent, connect to the netcat listener created in the previous step
   and leave it running:
    1. Open a shell in a terminal.
    1. Connect to the netcat listener: `nc <ip address> -p 7011` (insert the correct IP address).
1. In CALDERA and logged in as the blue user, open the Navigate Menu.
1. Click on `Campaigns > operations`.
1. In the Operations window, click on the `View` toggle button so it changes to `Add`.
1. Enter `Response Training` as the operation name.
1. Expand the `Basic Options` section.
   1. Select `blue` for the group.
   1. Select `Incident Responder` as the adversary.
   1. Select `Auto-close operation` as the operation termination option.
1. Expand the `Autonomous` section.
   1. Select `Use batch planner` from the planners dropdown.
   1. Ensure `Use response facts` is selected in the facts dropdown.
1. Press the `Start` button.
1. Wait for the operation to complete.
1. Task completed.