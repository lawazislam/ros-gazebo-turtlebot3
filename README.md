# ROS Noetic + Gazebo: TurtleBot3 Waffle Simulation

Setting up a full ROS robotics simulation environment from scratch and getting a TurtleBot3 Waffle model running in Gazebo, inside an Ubuntu VirtualBox VM.

## What's actually mine here, and what isn't

The TurtleBot3 Waffle model and its Gazebo simulation packages (`turtlebot3_simulations`) are open source, built and maintained by [ROBOTIS](https://github.com/ROBOTIS-GIT/turtlebot3_simulations), not my own code. What's genuinely mine is the environment work: installing ROS Noetic, setting up and building a catkin workspace, resolving dependencies, and getting the full simulation stack, Gazebo physics, the camera plugin, the laser plugin, and the differential drive plugin, running cleanly end to end.

There's also a custom node, `test/scripts/testnode.py`, visible in one of the workspace photos below, that I wrote myself back then. The original file didn't survive anywhere recoverable, only its filename, seen in a folder listing screenshot. **The version of `testnode.py` in this repo is a 2026 recreation, not the original file.** It's a new node, written from scratch to do something a TurtleBot3 test node would plausibly do (drive the robot through a square path as a first smoke test), clearly labeled as such in its own header comment. It has not been run against a live ROS/Gazebo instance, only checked for valid Python syntax and correct use of the standard ROS `cmd_vel` interface. Treat the photos below as the real, original evidence, and the code as a good-faith stand-in, not a recovered original.

## What's documented

Photos from the actual build and run, not staged, taken straight off the VM screen during setup. Hosted on my site since GitHub's folder upload wasn't cooperating, embedded here directly.

### ROS Noetic installation

Installing ROS Noetic, running `rosdep update` to resolve package dependencies, and starting `roscore` successfully (ROS Master URI live, ros_comm 1.15.14).

![rosdep update resolving package dependencies](https://lawazislam.com/assets/img/ros-gazebo/ros-installation-1.jpg)
![ROS installation step](https://lawazislam.com/assets/img/ros-gazebo/ros-installation-2.jpg)
![roscore starting successfully with ROS Master URI live](https://lawazislam.com/assets/img/ros-gazebo/ros-installation-3-roscore.jpg)
![rosdep update completing, dependency cache updated](https://lawazislam.com/assets/img/ros-gazebo/ros-installation-4.jpg)

### Catkin workspace

Building the catkin workspace with `catkin_make` (Python 3.8.10, gtest/gmock built from source, shared libs on), sourcing `devel/setup.bash`, and the workspace's folder structure including the custom `testnode.py`.

![catkin_make building the workspace successfully](https://lawazislam.com/assets/img/ros-gazebo/catkin-workspace-1-build.jpg)
![Catkin workspace step](https://lawazislam.com/assets/img/ros-gazebo/catkin-workspace-2.jpg)
![Catkin workspace step](https://lawazislam.com/assets/img/ros-gazebo/catkin-workspace-3.jpg)
![Workspace folder listing showing testnode.py](https://lawazislam.com/assets/img/ros-gazebo/catkin-workspace-4.jpg)
![Catkin workspace step](https://lawazislam.com/assets/img/ros-gazebo/catkin-workspace-5.jpg)

### Gazebo + TurtleBot3

The TurtleBot3 Waffle model spawning successfully in Gazebo, with the camera plugin, laser plugin, and differential drive plugin all initializing and advertising their topics (`cmd_vel`, `odom`, `joint_states`), and the spawn process finishing cleanly.

![TurtleBot3 spawn log showing camera, laser, and diff-drive plugins initializing cleanly](https://lawazislam.com/assets/img/ros-gazebo/gazebo-turtlebot3-1-simulation-log.jpg)
![Gazebo TurtleBot3 simulation step](https://lawazislam.com/assets/img/ros-gazebo/gazebo-turtlebot3-2.jpg)

## Setup reference

For anyone wanting to reproduce this: ROS Noetic on Ubuntu 20.04, catkin workspace at `~/catkin_ws`, TurtleBot3 packages from ROBOTIS's official repos ([turtlebot3](https://github.com/ROBOTIS-GIT/turtlebot3), [turtlebot3_simulations](https://github.com/ROBOTIS-GIT/turtlebot3_simulations)), launched with `roslaunch turtlebot3_gazebo turtlebot3_world.launch` (model set to `waffle` via the `TURTLEBOT3_MODEL` environment variable).
