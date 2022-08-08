1. In the left-handside navigation, select `CONFIGURATION > configuration`.
1. At the top of the page, press `Plugins` button (the one next to `Settings`) to show the list of plugins.
1. Locate `mock` plugin in the list and press `Enable` button in that row.
1. Terminate the CALDERA server.
1. Re-run the server. Ensure the `--fresh` flag is not used.
1. Re-login into the CALDERA application in your browser window.
1. Next, ensure that an agent is deployed and is responsive.
1. Select `CAMPAIGNS > operations`.
1. Click the `+ Create Operation` button to open the `Start New Operation` menu.
1. Give the operation a name.
1. In the `Group`, select `simulation`.
1. Select the `Check` adversary from the `Adversary` dropdown.
1. Select `basic` from the `Fact source` menu.
1. Press `ADVANCED` to open the advanced options dialog.
1. Select `Auto close operation` from the `Auto-close`radio group.
1. Press `Start` to run the operation.
1. Wait for the operation to complete.
1. If the `Auto close operation` option was not selected, press the stop button to finish the operation.
1. Task completed.