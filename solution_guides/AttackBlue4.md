1. Ensure compass plugin is enabled
1. Select `PLUGINS > compass`.
1. Click the `Create New Layer > Enterprise ATT&CK` button to open a new navigator layer.
1. Select the technique that best matches the procedure: `net /y use \\#{remote.host.name} & copy /y sandcat.go-windows \\#{remote.host.name}\Users\Public`. When the technique is selected (Lateral Tool Transfer), give it a score of `1`. Rename the layer `blue_quiz_5` and then download the layer in json format.
1. Navigate back to the Compass plugin home page and click `Create Operation` under `Generate Adversary`. Select the json named `blue_quiz_5` and open to upload.
1. Task completed.
