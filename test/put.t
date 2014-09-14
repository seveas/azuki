#!/bin/sh

test_description="Test put"

. ./setup.sh

test_expect_success "put" '
    echo "test put" | azuki put $test_tube &&
    azuki stats $test_tube | grep "^ *Ready: *1$"
'

test_expect_success "put --ttr" '
    azuki foreach $test_tube /bin/true &&
    echo "test put" | azuki put --ttr 600 $test_tube &&
    azuki peek-ready $test_tube &&
    azuki peek-ready $test_tube | grep "^TTR: *600$"
'

test_expect_success "put --delay" '
    echo "test put" | azuki put --delay 60 $test_tube &&
    azuki stats $test_tube | grep "^ *Delayed: *1$"
'

clean_tubes
test_done

# vim: set syntax=sh:
