#!/bin/sh

test_description="Test python and django API's"

. ./setup.sh

test_expect_success "Python API" '
    test_when_finished clean_tubes &&
    echo "Hello, important world" >expected &&
    echo "Hello, world" >>expected &&
    test_python t_plain &&
    azuki daemon $test_tube >actual &&
    sed "/^INFO/d" -i actual &&
    test_cmp expected actual
'

test_expect_success "Python API from __main__" '
    test_when_finished clean_tubes &&
    echo "Hello, main" >expected &&
    $PYTHON $SHARNESS_TEST_DIRECTORY/python/t_main &&
    azuki daemon $test_tube >actual &&
    sed "/^INFO/d" -i actual &&
    test_cmp expected actual
'

test_expect_success "Python API with rescheduling" '
    test_when_finished clean_tubes &&
    echo "1" > expected &&
    echo "3" >> expected &&
    echo "2" >> expected &&
    test_python t_reschedule &&
    azuki daemon $test_tube >actual &&
    sed "/^INFO/d" -i actual &&
    test_cmp expected actual
'

test_expect_success DJANGO "Django API" '
    echo "Hello, django" >expected &&
    ( cd $SHARNESS_TEST_DIRECTORY/python/azk && python manage.py syncdb --noinput ) &&
    test_python t_django &&
    DJANGO_SETTINGS_MODULE=azk.settings azuki daemon $test_tube >actual &&
    sed "/^INFO/d" -i actual &&
    sed "/^DEBUG/d" -i actual &&
    test_cmp expected actual
'

clean_tubes
test_done

# vim: set syntax=sh:
