# MITRE Caldera Plugin: Training

## Overview:

The Training plugin provides interactive training and certification content. This plugin allows a user to gain a “User Certificate” which proves their ability to use Caldera. This is the first of several certificates planned in the future. The plugin takes you through a capture-the-flag style certification course, covering all parts Caldera.

### Context:
Training content and certification

<!-- ### Known Limitations: -->

## Installation:

This is a core CALDERA plugin and is loaded by default via the plugin loader. Ensure it is present in the `plugins/` directory and listed as enabled in your active configuration file (e.g., `conf/default.yml`).

## Dependencies/Requirements:

This plugin uses `eslint` for javascript linting and requires the following dependencies:

* `node >= 15.9.0`
* `npm >= 7.5.0`

Linting is performed automatically when changes are pushed to a branch in github via a github
action.

To run locally, perform the following commands:

```
> cd /path/to/training/repo
> npm ci
> npm run lint
```

To fix issues automatically run the following (note: not all violations can be fixed automatically):

```
> npm run lint -- --fix
```

For information about rule violations, see the [eslint rules](https://eslint.org/docs/rules/) page.

## Getting Started:

To begin using the Training plugin, navigate to the Training section in the CALDERA UI after starting the server. From there, select a training module or certification track and start with the first flag. The flags are designed to build progressively, so it’s recommended to complete them in order.

If you get stuck, solution guides are available for each flag and can be used to help clarify necessary steps.

**Important**: When running CALDERA during completion of a training module, do not start the server with the --fresh flag. Doing so will reset the environment and result in loss of progress.