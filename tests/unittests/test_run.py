""" Unit tests for run.py/Command Line Interface """

import pytest
import run

################################## CMD SETUP ################################
app = run.replShell()

################################ TEST COMMANDS ##############################
# Test list and maybe save/load

################################### CLASS ###################################
################################## TEST ADD #################################
def test_do_add_empty():
    app.do_add("TestAddEmpty")
    assert app.do_list() == "TestAddEmpty"

def test_do_add_dup():
    app.do_add("TestAddEmpty")
    assert app.do_list() == "TestAddEmpty"

def test_do_add_more():
    app.do_add("TestAddMore")
    app.do_add("TestAdd1More")
    assert app.do_list() == "TestAddEmpty, TestAddMore, TestAdd1More"

def test_do_add_none():
    app.do_add("")
    assert app.do_list() == "TestAddEmpty, TestAddMore, TestAdd1More"

def test_do_add_multi():
    app.do_add("Multi1, Multi2, Multi3")
    assert app.do_list() == "TestAddEmpty, TestAddMore, TestAdd1More, Multi1, Multi2, Multi3"

################################ TEST DELETE ################################

################################# TEST EDIT #################################

################################# ATTRIBUTES ################################
################################ TEST addAttr ###############################

################################ TEST delAttr ###############################

############################### TEST editAttr ###############################

############################### RELATIONSHIPS ###############################
################################ TEST addRel ################################

################################ TEST delRel ################################