""" Unit tests for run.py/Command Line Interface """

import pytest
import run

################################## CMD SETUP ################################
app = run.replShell()
################################ TEST COMMANDS ##############################
################################## TEST ADD #################################
def test_do_add_empty():
    assert app.do_add("TestAddEmpty") == "Successfully added class \'' + name + '\'"

def test_do_add_dup():
    assert app.do_add("TestAddEmpty") == "ERROR: Unable to add class \'' + name + '\'"

def test_do_add_more():
    assert app.do_add("TestAddMore") == "Successfully added class \'' + name + '\'"
    assert app.do_add("TestAdd1More") == "Successfully added class \'' + name + '\'"

def test_do_add_none():
    assert app.do_add("") == "Please provide a class name"

# write a test for adding multiple classes at a time (use list once its finished)
################################ TEST DELETE ################################