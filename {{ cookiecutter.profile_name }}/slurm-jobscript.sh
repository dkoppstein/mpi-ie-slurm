#!/bin/bash

scratch=$(mktemp -p {{ cookiecutter.default_tmpdir }} -d -t tmp.XXXXXXXXXXXXXXXX);
export TMPDIR=$scratch;
export TEMP=$scratch;
export TMP=$scratch;
function cleanup {% raw %}{{ rm -rf $TMPDIR; }}{% endraw %}
trap cleanup EXIT SIGTERM SIGKILL SIGUSR2
{exec_job}
