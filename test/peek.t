#!/bin/sh

test_description="Test peek commands"

. ./setup.sh

test_expect_success "setup" '
    submit_test_job &&
    azuki foreach $test_tube /bin/false &&
    submit_test_job --delay=60 &&
    submit_test_job
'

test_expect_success "peek-buried" '
    azuki peek-buried $test_tube | grep "test job 1"
'

test_expect_success "peek-delayed" '
    azuki peek-delayed $test_tube | grep "test job 2" &&
    echo delete | azuki peek-delayed --ask $test_tube &&
    test_must_fail azuki peek-delayed
'

test_expect_success "peek-ready" '
    azuki peek-ready $test_tube | grep "test job 3"
'

test_expect_success "peek-buried --ask kick" '
    echo kick | azuki peek-buried $test_tube --ask &&
    test_must_fail azuki peek-buried
'

test_expect_success "peek" '
    azuki peek-ready $test_tube >peek-ready &&
    jid=$(sed -ne "s/Job //p" peek-ready) &&
    azuki peek $jid >peek-jid &&
    sed /^Age/d -i peek-jid peek-ready &&
    test_cmp peek-ready peek-jid
'

test_expect_success "peek nonexistent job" '
    test_must_fail azuki peek 0
'

test_expect_success "peek nonexistent tube" '
    test_must_fail azuki peek-ready azuki-test-nonexistent 2>err &&
    test_must_fail azuki peek-buried azuki-test-nonexistent 2>>err &&
    test_must_fail azuki peek-delayed azuki-test-nonexistent 2>>err &&
    test_must_fail grep Traceback err
'

clean_tubes

test_expect_success "peek empty tube" '
    test_must_fail azuki peek-ready $test_tube 2>err &&
    test_must_fail azuki peek-buried $test_tube 2>>err &&
    test_must_fail azuki peek-delayed $test_tube 2>>err &&
    test_must_fail grep Traceback err
'

clean_tubes
test_done

# vim: set syntax=sh:
