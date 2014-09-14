#!/bin/sh

test_description="Test tubes"

. ./setup.sh

test_expect_success "tubes" '
    azuki tubes | grep default
'

test_done

# vim: set syntax=sh:
