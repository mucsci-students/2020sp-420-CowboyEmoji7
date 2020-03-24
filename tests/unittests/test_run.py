""" Unit tests for run.py/Command Line Interface """

import pytest
import run

################################## CMD SETUP ################################
app = run.replShell()

################################ TEST COMMANDS ##############################
# Test list and maybe save/load

################################### CLASS ###################################
################################## TEST ADD #################################
def test_do_add(capsys):
    ##### TEST EMPTY #####
    app.do_add("TestAddEmpty")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'TestAddEmpty'\n"
    app.do_list("")
    captured = capsys.readouterr()
    assert captured.out == "TestAddEmpty\n"

def test_do_add_duplicate(capsys):
    app.do_add("TestAddEmpty")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'TestAddEmpty'\n"
    app.do_add("TestAddEmpty")
    captured = capsys.readouterr()
    assert captured.out == "ERROR: Unable to add class 'TestAddEmpty'\n"
    app.do_list("")
    captured = capsys.readouterr()
    assert captured.out == "TestAddEmpty\n"

def test_do_add_more(capsys):
    app.do_add("TestAddMore")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'TestAddMore'\n"
    app.do_add("TestAdd1More")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'TestAdd1More'\n"
    app.do_list("")
    captured = capsys.readouterr()
    assert captured.out == "TestAddMore, TestAdd1More\n"

def test_do_add_none(capsys):
    app.do_add("")
    

def test_do_add_multi(capsys):
    app.do_add("Multi1, Multi2, Multi3")
    assert app.do_list("") == "TestAddEmpty, TestAddMore, TestAdd1More, Multi1, Multi2, Multi3"

################################ TEST DELETE ################################

################################# TEST EDIT #################################

################################# ATTRIBUTES ################################
################################ TEST addAttr ###############################

################################ TEST delAttr ###############################

############################### TEST editAttr ###############################

############################### RELATIONSHIPS ###############################
################################ TEST addRel ################################

################################ TEST delRel ################################