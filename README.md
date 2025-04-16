# acsl_package

"main" branch shows a template.

"package" is a set of programs and settings consisting of a standalone container.

Each package may consist of the following contents.

| file name | description |
| ---- | ---- |
|1_launcher|launch shell scripts exec in docker container|
||launch_PACKAGE.sh|
|2_ros_packages|ros package build and run in docker container|
||PACKAGE/|
|3_dockerfiles|dockerfile to build a docker image|
||dockerfile.PACKAGE|
|PACKAGE.rules| udev rule|

## How to

### Install an existing package

These packages are expected to use in the project by ["acsl"](https://github.com/acsl-tcu/acsl) command.

```bash
acsl install package_name
```
### Remove a package from your project

```bash
acsl remove package_name
```

### Create a new package

```bash
acsl make_package package_name
```

Then clone acsl_package using GitHub desktop and switch the branch to "package_name" you set above.
