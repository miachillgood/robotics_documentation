# Use Workshop and git worktree for ROS 2 development

Oftentimes, a ROS 2 repository supports multiple ROS 2 distributions.
Switching from one branch to another, say from `jazzy` to `lyrical`,
implies not only changing the ROS 2 distribution but also the underlying operating system, in the case from Ubuntu 24.04 to 26.04.
As reinstalling the host machine to port a simple git patch is obviously unpractical,
ROS 2 developers rely on virtualization to carry their daily work.

We showcase hereafter how Workshop alleviates this task using [git worktree](https://git-scm.com/docs/git-worktree).

## Prerequisites

This how-to guide assumes you are familiar with:

- ROS 2 development and git workflows
- [Workshop basics](https://canonical-robotics.readthedocs-hosted.com/en/latest/tutorials/workshop/ros2-dev-workshop/) for creating and launching development environments
- Git fundamentals

Additionally, you will need:

- Workshop installed and configured (see [Workshop documentation](https://canonical-workshop.readthedocs-hosted.com/) for setup instructions)
- LXD 6.3+ and ZFS support enabled
- A ROS 2 repository with support for multiple branches/distributions

## What is git worktree?

`git worktree` is a Git feature that allows you to have multiple working trees attached to the same repository.
This means you can work on different branches simultaneously without switching branches in a single directory.
Each worktree is an independent working directory with its own `HEAD` and staging area,
but they all share the same Git object database.

## Why use git worktree with Workshop?

When developing ROS 2 applications that support multiple distributions,
git worktree combined with Workshop offers several advantages:

- **Parallel development**: Work on multiple ROS 2 distributions without switching branches
- **Isolated environments**: Each distribution runs in its own Workshop container with the correct OS and dependencies
- **Fast switching**: No need to rebuild or reinstall dependencies when switching between distributions
- **Clean separation**: Each worktree can have its own Workshop configuration tailored to the distribution

## Set up git worktree for multiple distributions

Let's demonstrate this with the [ROS 2 demos](https://github.com/ros2/demos) repository,
which supports both ROS 2 Jazzy (Ubuntu 24.04) and ROS 2 Lyrical (Ubuntu 26.04).

First, clone the repository:

```bash
git clone https://github.com/ros2/demos.git
cd demos
```

Next, create separate git worktrees for each distribution you want to work on.
For the Jazzy branch:

```bash
git worktree add -b jazzy-work ../demos-jazzy origin/jazzy
```

For the Lyrical branch:

```bash
git worktree add -b lyrical-work ../demos-lyrical origin/lyrical
```

Now you have three directories:

- `demos/` (original, main branch)
- `demos-jazzy/` (Jazzy worktree)
- `demos-lyrical/` (Lyrical worktree)

## Create Workshop definitions for each distribution

In each worktree directory, use the `workshop init` command to create a tailored `workshop.yaml` file.

For the Jazzy worktree:

```bash
cd ../demos-jazzy
workshop init --name demos-jazzy-dev --base ubuntu@24.04 --sdk ros2-desktop:jazzy/stable
```

For the Lyrical worktree:

```bash
cd ../demos-lyrical
workshop init --name demos-lyrical-dev --base ubuntu@26.04 --sdk ros2-desktop:lyrical/stable
```

This will create a `workshop.yaml` file in each directory with the appropriate configuration for the respective distribution.

## Launch and use the Workshop environments

Navigate to the Jazzy worktree and launch its Workshop:

```bash
cd ../demos-jazzy
workshop launch
```

Verify the workshop is ready:

```bash
$ workshop list
Workshop           Status  Notes
demos-jazzy-dev    Ready   -
```

You can now open a shell and develop for ROS 2 Jazzy:

```bash
workshop shell
```

Similarly, for the Lyrical worktree, in another terminal:

```bash
cd ../demos-lyrical
workshop launch
workshop shell
```

Now you have two independent Workshop environments running simultaneously,
each with the correct OS and ROS 2 distribution.
You can work on both distributions in parallel without any conflicts.

## Switch between worktrees

To work on a different distribution,
simply navigate to the corresponding worktree directory
and open a new Workshop shell:

```bash
cd ../demos-lyrical
workshop shell
```

The Workshop environment for Lyrical will be ready to use immediately,
as each worktree maintains its own Workshop container with all necessary dependencies.

## Clean up worktrees

When you no longer need a worktree,
you can remove it along with its Workshop container.

First, list your active worktrees:

```bash
git worktree list
```

Stop the corresponding Workshop:

```bash
workshop stop demos-jazzy-dev
```

Then remove the worktree:

```bash
git worktree remove ../demos-jazzy
```

This removes the worktree directory and cleans up the Git internal references,
while the original repository in `demos/` remains unaffected.
