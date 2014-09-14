#!/bin/sh

test_description="Test pause"

. ./setup.sh

test_expect_success "Pause tube" '
    submit_test_job &&
    azuki pause 100 $test_tube &&
    azuki stats $test_tube | grep "paused until"
'

test_expect_success "Unpause tube" '
    azuki pause 0 $test_tube &&
    azuki stats $test_tube >out &&
    test_must_fail grep paused out
'

test_done

# vim: set syntax=sh:
