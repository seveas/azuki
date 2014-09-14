#!/bin/sh

test_description="Test kick"

. ./setup.sh

test_expect_success "kick job" '
    submit_test_job
    azuki foreach $test_tube /bin/false &&
    jid=$(azuki peek-buried $test_tube | sed -ne "s/Job //p") &&
    azuki kick $jid &&
    azuki stats $test_tube | grep "Buried: *0"
'

test_expect_success "kick tube" '
    for i in 1 2 3; do submit_test_job; done &&
    azuki foreach $test_tube /bin/false &&
    azuki kick 4 $test_tube &&
    azuki stats $test_tube | grep "Buried: *0"
'

clean_tubes
test_done

# vim: set syntax=sh:
