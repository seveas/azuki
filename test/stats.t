#!/bin/sh

test_description="Test stats commands"

. ./setup.sh

test_expect_success "Basic stats" '
    azuki stats &&
    azuki stats | grep ^Commands:
'

test_expect_success "Tube stats" '
    azuki stats default | grep ^Jobs:
'

test_expect_success "Nonexistent tube" '
    test_must_fail azuki stats $test_tube-nonexistent 2>err &&
    test_must_fail grep Traceback err
'

test_expect_success "Job stats" '
    submit_test_job &&
    jid=$(azuki peek-ready $test_tube | sed -ne "s/Job //p") &&
    azuki stats $jid | grep ^TTR
'

clean_tubes
test_done

# vim: set syntax=sh:
