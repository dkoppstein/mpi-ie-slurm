#!/bin/bash
function cleanup {{ rm -rf $TMPDIR; }} 
trap cleanup SIGTERM SIGKILL SIGUSR2
{exec_job}
cleanup
