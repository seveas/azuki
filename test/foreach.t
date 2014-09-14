#!/bin/sh

test_description="Test tubes"

. ./setup.sh

test_expect_success "foreach /bin/false" '
    for i in 1 2 3 4 5; do submit_test_job; done &&
    azuki stats $test_tube | grep "^ *Ready: *5$" &&
    azuki foreach $test_tube /bin/false &&
    azuki stats $test_tube | grep "^ *Ready: *0$" &&
    azuki stats $test_tube | grep "^ *Buried: *5$"
'

test_expect_success "foreach /bin/true" '
    azuki kick 5 $test_tube &&
    azuki stats $test_tube | grep "^ *Ready: *5$" &&
    azuki foreach $test_tube /bin/true &&
    test_must_fail azuki stats $test_tube
'

test_expect_success "foreach content" '
    for i in 1 2 3 4 5; do submit_test_job; done &&
    azuki stats $test_tube | grep "^ *Ready: *5$" &&
    azuki foreach $test_tube grep "[24680]$" &&
    azuki stats $test_tube | grep "^ *Ready: *0$" &&
    azuki stats $test_tube | grep "^ *Buried: *2$" '

clean_tubes
test_done

# vim: set syntax=sh:
