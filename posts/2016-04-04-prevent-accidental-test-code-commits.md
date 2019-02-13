[frontMatter]
description = "A quick hack to prevent you from accidentally commiting test code"
title = "Using Git Hooks to prevent commiting test code"
created = "2016-04-04"
published = true
keywords = ["git", "hook", "commit", "debug", "test", "code"]
slug = "2016-04-04-prevent-accidental-test-code-commits.html"
tags = ["git"]
---

Today I\'d like to share a quick setup which I\'m using in most of my
local **Git** repositories nowadays to prevent me from accidentally
commiting certain exploratory lines of code which fall neither in
between the `debug` / `release` flags nor unit tests.

Here\'s a quick example: Imagine you\'re writing an app that shows the
current trending links out of Hacker News, Reddit, and Product Hunt
combined. For each source, you\'re setting up an importer:

``` Swift
let importers = [
  importerHackerNews()
  importerReddit(),
  importerProductHunt()
] 
```

However, while you\'re working on a new feature, Hacker News is down.
This isn\'t a problem in itself, but each time you start up the app
you\'re greeted with a popup reminding you that your app can\'t
currently import from Hacker News.

So, in order to be productive again, you quickly comment out the
HackerNews importer, making a mental note to uncomment it before you
commit todays changes:

``` Swift
let importers = [
  // REMEMBER: Only temporary
  // importerHackerNews()
  importerReddit(),
  importerProductHunt()
] 
```

Later on, when you collect all the change hunks of the new feature into
your Git staging area, you\'re obviously performing due dilligence and
carefully examining each change to make sure that there\'re no unwanted
lines.

However, sometimes something slips through, and that\'s when your Hacker
News importer suddenly doesn\'t work anymore. There\'re of course
multiple ways to prevent this:

-   In a perfect world you\'d have a unit test set up which catches this
    on your CI server (or even before that on your local system).
-   You can add `FIXME` lines and generate warnings or errors during
    building (if you\'re working in a compiled language)
-   You can write notes or todos on your system

My problem with all the above approaches is that they\'re a bit
indirect, oftentimes requiring the setup or housekeeping of a secondary
system just to make sure nothing slips through.

### Using Git Hooks as a solution

I\'d rather play it safe here. Whether or not I have unit tests for
small temporary changes like these, whatever happens, under no
circumstances should I be allowed to commit this. My solution is the
addition of a commented tag which will be picked up by a Git Hook in
order to tell Git that it is not safe to commit the project in its
current state. You can chose any tag you want, I decided to use the tag
`#BABOON#`. The only requirement here is that the chance is very
unlikely that you\'d write this tag somewhere else in your codebase as
part of the actual source code.

When that tag has been added to the staging area like so:

``` Swift
let importers = [
  // #BABOON#(comment out again)
  // importerHackerNews()
  importerReddit(),
  importerProductHunt()
] 
```

And I\'m trying to commit this, Git will fail with an exception. It does
that because I\'ve added the following hook to my Git repository:

``` bash
#!/bin/sh
if git rev-parse --verify HEAD >/dev/null 2>&1
then
    against=HEAD
else
    # Initial commit: diff against an empty tree object
    against=4b825dc642cb6eb9a060e54bf8d69288fbee4904
fi

# The special marker tag to mark things which we still need to change
marker="#BABOON#"

# Redirect output to stderr.
exec 1>&2

if test $(git diff --cached -z $against | grep $marker | wc -c) != 0 
then
    cat <<\EOF
    Error: Still has invalid debug markers in code:
EOF
    echo `git diff --cached -z $against -G $marker`
    exit 1
fi
```

This file has to be stored within your Git repository at the following
place:

``` bash
.git/hooks/pre-commit
```

What that script does is whenever you\'re trying to commit, it will run
a grep search against all currently staged changes
(`git diff --cached -z $against | grep $marker | wc -c`) and will test
if there\'re more than zero results. If that\'s the case, the script
will exit with a `1` which signifies to Git that it should not continue
running.

As outlined above, there\'re several other solutions for the above
problem, but I like having this one in my Git repo as the first line of
defense.
