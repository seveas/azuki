#!/bin/sh

test_description="Test connection"

. ./setup.sh

test_expect_success "connection to default daemon" '
    azuki stats
'

test_expect_success "connection to non-standard daemon" '
    beanstalkd -p 11301 &
    pid=$!
    azuki --host localhost --port 11301 stats &&
    kill $pid
'

test_done

# vim: set syntax=sh:
