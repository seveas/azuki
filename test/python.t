#!/bin/sh

test_description="Test python and django API's"

. ./setup.sh

test_expect_success "Python API" '
    echo "Hello, world" >expected
    test_python t_plain &&
    azuki daemon $test_tube >actual &&
    sed "/^INFO/d" -i actual &&
    test_cmp expected actual
'

test_expect_success DJANGO "Django API" '
    ( cd $SHARNESS_TEST_DIRECTORY/python/azk && python manage.py syncdb --noinput ) &&
    test_python t_django &&
    azuki daemon $test_tube >actual &&
    sed "/^INFO/d" -i actual &&
    test_cmp expected actual
'

clean_tubes
test_done

# vim: set syntax=sh:
