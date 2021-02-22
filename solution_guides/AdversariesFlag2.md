1. Open the Navigate menu.
1. Select `Campaigns > adversaries`.
1. In the _Adversary Profiles_ window that opens, ensure that the toggle button says `View`.
1. In the drop-down, select the `Certifiable` adversary profile.
1. Press the `+ add ability` button on the right side of the window.
1. In the window that appears, enter the following information:
    1. Press the `generate new id` button.
    1. Enter `My test ability` in the `name` text box.
    1. Enter `discovery` in the `tactic` text box.
1. Press the `add executor` button on the right and enter/select the following information:
    1. Select `darwin` as the platform from the drop-down.
    1. Select `sh` as the executor from the drop-down.
    1. Select `sandcat.go-darwin` from the payloads box.
    1. Enter `whoami` in the command text box.
    1. Enter `ifconfig -a` in the cleanup command text box.
1. Press the `Add to Adversary` button
1. Press the `Save` button on the left side of the _Adversary Profiles_ window.
1. Task completed.