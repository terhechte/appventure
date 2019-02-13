[frontMatter]
description = "An interactive Git Status client, written in C"
title = "An interactive Git Status client, written in C"
created = "2019-01-24"
published = true
keywords = ["c", "linux", "macos", "ncurses", "git", "libgit"]
slug = "2019-01-24-interactive-git-status-written-in-c.html"
tags = ["c", "linux"]
---

<https://j.gifs.com/JyDPZy.gif>

<a href="https://github.com/terhechte/gitsi" class="button round small">
<i class="fi-social-github"></i>
Gitsi On GitHub</a>

<a href="https://www.youtube.com/watch?v=pAxquqis56I&feature=youtu.be" class="button round small">
Youtube Video</a>

Over Christmas I decided on a whim to solve a workflow-related problem
that I\'ve had for some time and to also go back and write a small-scale
project in C. The result is `Gitsi` a small, lightweight, interactive
git status client that offers fast shortcuts to quickly manage the git
status output. Let me go back to the actual problem I had.

# Using Git on the Commandline

Over the years I\'ve tried and used many different git clients.
`SourceTree`, `GitUp`, `Gitk`, `Magit`, to name a few. `Magit` (a Git
client build into Emacs) is the one I still use the most, but over the
years I\'ve more and more moved towards plain git on the terminal for
most of my daily activities. However, one thing always bugged me: If I
have an output from git status (say the following one):

``` bash
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

    modified:   Readme.md

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   component_stats.db
        modified:   q.sql

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        documentation/README.md
        api_design/design_draft.md
```

Then if I want to add the two untracked files and the q.sql to the index
(in order to commit them) I\'d have to write:

``` bash
git add documentation/README.md
git add pi_design/design_draft.md
git add q.sql
```

That\'s a lot of typing. Usually I go about copy pasting with the mouse.
That also takes forever. Surely using a git GUI tool (like SourceTree)
is much faster but as I don\'t need it for any of the other tasks I
usually do, I\'d need to start it first, which also takes forever. What
I envisioned was an easy way to add, stage, unstage files in the git
index, workspace and untracked files. Bonus points for also allowing
`git checkout --` to remove changes to a specific file.

I know there\'re tools for that (such as `tig`) but I wanted something
that only did one thing, status management. No logging, no pushing or
pulling, etc. This felt to me like a great opportunity to write a small
scale C project, something I hadn\'t done for at least more than 10
years.

# Gitsi

<img src="/cimg/logo_gitsi.svg" height="150" />

This is how gitsi was born. Have a [look at the project if you\'re
interested](https://github.com/terhechte/gitsi), it offers a nice
handful of features such as all of the above plus: VIM Keybindings,
filtering, diffing, interactive `git add` and more.

[Here\'s a short video that shows it in
action](https://www.youtube.com/watch?v=pAxquqis56I&feature=youtu.be)

# Writing in C

As a iOS developer I\'ve had my fair share of Objective-C, however all
the nice abstractions that Apple put in place actually mean that usually
I don\'t really touch C code. So, writing something bigger in C was
really interesting when comparing it to developing something in Swift
(doh, obviously).

It relies on two libraries:

-   [libgit2](https://libgit2.org/): The interface to `git`.
    Interestingly `git` (the commandline tool) and `libgit2` are
    separate entities. Meaning `git` does not use libgit. This means
    that for some things that git does, there is no easy equivalent in
    libgit. This makes some things very hard.
-   [ncurses](https://en.wikipedia.org/wiki/Ncurses): This is *the*
    library to use when developing TUI (terminal UI) applications. It
    allows you to move the cursor around in the terminal, color it, draw
    windows, etc.

## The fun parts

-   Compile times were beyond beautiful
-   The limited featureset of the language made it surprisingly fun to
    work on a project of this size. There\'s no questioning which
    abstraction to use, there\'s usually only one that fits. If
    there\'re more, they require more indepth knowledge of the language.
-   This is not particular to C, but the reactive approach of writing a
    TUI app by just rendering over a mainloop (also like most games)
    feels very refreshing compared to *normal* iOS work (obvious
    comparison to React, etc)
-   Getting it to work on a different platform (Linux) was also kinda
    easy, though I struggled more with it than I would have expected. In
    particular there\'re several useful functions that are not part of
    C99 (the 99 C standard). Using them requires the correct compile
    flag (`-std=gnu11`). However, some functions are also not part of
    the C standard, but specific GNU extensions, though they\'re also
    supported on all the platforms I care about. Using these requires
    adding a `#define _GNU_SOURCE` at the top of your source file.
    However, not on macOS, but on Linux. This was tricky to figure out.

## The less fun parts

-   Memory management. This was totally expected, but it consumed more
    time than I\'d have expected. Thankfully, `valgrind` is a great tool
    to find these issues. Sadly, valgrind seems to not run on macOS
    right now, so I ran it via Docker. That worked great though. I had a
    lot of small issues that seem to be (mostly) fixed now. This
    experience alone makes me so grateful for Swift\'s Arc and Rust\'s
    Borrow Checker.
-   Documentation. This was terrible. The `libgit` documentation is
    mostly ok, but for the C `stdlib` and epecially `ncurses`, the
    documentation is just awful. Since they all differ platform by
    platform, implementation by implementation, there\'s no *one*
    reference. Sometimes it would take me forever to just figure out
    what the parameters to a certain function would do. Getting this
    done involved a lot of googling.
-   Lack of tooling suite. Sure, almost every editor supports C, but
    almost everything in tooling requires choices, research and pain.
    There\'s no one package manager / ecosystem. How to handle building,
    there\'re a ton of build systems, how to handle tests, there\'re a
    ton of solutions. Since everything is so free and open, everything
    is also a mess. It is probably much easier when you\'re working on a
    pre-existing, pre-defined project, but there\'s a huge overhead of
    things just to get started. I tried to keep it as simple as
    possible. System Package Manager (`homebrew` / `apt-get`), `vim`,
    `cmake` and no tests.

# Using it with Xcode

Working on a project like this from `Xcode` works surprisingly well. I
set up an Xcode project, added the required libraries (`ncurses` and
`libgit`) imported the `main.c` file and I could compile it. Debugging
was a wee bit more work. Since Xcode can\'t run ncurses executables
(i.e. it can\'t run them in a terminal) we have to tell Xcode to compile
the app and then wait for the process to start and then to attach to it.
After that, I can head to a terminal and run the just-compiled app and
then Xcode will attach to it and all the breakpoints etc work. It is a
wee bit more cumbersome but works fine. I had to introduce a particular
command line flag though that makes sure that attaching via Xcode
doesn\'t break things.

# Testing

There\'re no tests. Yet. I\'ve started on the necessary prerequisites to
run integration tests but I wanted to release it first. The idea is to
start the binary in a special mode and give it a string of tasks (i.e.
go down 2 lines, do a git add, go up one line, etc) and then make sure
that the end result is what\'s expected.

# Recap

This was a fun project, but now I\'m also done with C for the rest of
this year (except for small additions to gitsi, of course). I\'m already
longing to do something in Swift or Rust again.
