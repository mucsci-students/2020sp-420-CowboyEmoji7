""" Unit tests for run.py/Command Line Interface """

import pytest
import run

#################################### SETUP ##################################
app = run.replShell()

# lazy mans way of capturing list
def captureList(capsys):
    app.do_list("")
    captured = capsys.readouterr()
    return captured

################################ TEST COMMANDS ##############################
# Test list and maybe save/load

################################### CLASS ###################################
################################## TEST ADD #################################
def test_do_add(capsys): 
    app.do_add("TestAddEmpty")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'TestAddEmpty'\n"

    captured = captureList(capsys)
    assert captured.out == "TestAddEmpty\n\n"

def test_do_add_duplicate(capsys):
    app.do_add("TestAddEmpty")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'TestAddEmpty'\n"

    app.do_add("TestAddEmpty")
    captured = capsys.readouterr()
    assert captured.out == "ERROR: Unable to add class 'TestAddEmpty'\n"

    captured = captureList(capsys)
    assert captured.out == "TestAddEmpty\n\n"

def test_do_add_more(capsys):
    app.do_add("TestAddMore")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'TestAddMore'\n"

    app.do_add("TestAdd1More")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'TestAdd1More'\n"

    captured = captureList(capsys)
    assert captured.out == "TestAddMore\nTestAdd1More\n\n"

def test_do_add_none(capsys):
    app.do_add("")
    captured = capsys.readouterr()
    assert captured.out == "Usage: add <class_name1>, <class_name2>, ... , <class_nameN>\n"
    
    

def test_do_add_multi(capsys):
    app.do_add("Multi1, Multi2, Multi3")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added class 'Multi1'\nSuccessfully added class 'Multi2'\nSuccessfully added class 'Multi3'\n"

    captured = captureList(capsys)
    assert captured.out == "Multi1\nMulti2\nMulti3\n\n"

################################ TEST DELETE ################################
def test_do_delete(capsys):
    #Need to capture the add text first to isolate only the delete output
    app.do_add("TestDelete")
    captured = capsys.readouterr()

    app.do_delete("TestDelete")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted class 'TestDelete'\n"

    captured = captureList(capsys)
    assert captured.out == "No Classes\n\n"

def test_do_delete_none(capsys):
    app.do_delete("")
    captured = capsys.readouterr()
    assert captured.out == "Usage: delete <class_name1>, <class_name2>, ... , <class_nameN>\n"

def test_do_delete_nonexistant(capsys):
    app.do_delete("test")
    captured = capsys.readouterr()
    assert captured.out == "ERROR: Unable to delete class 'test'\n"

def test_do_delete_some(capsys):
    #Need to capture adding messages before delete message
    app.do_add("test1, test2, test3")
    captured = capsys.readouterr()

    app.do_delete("test2")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted class 'test2'\n"

    captured = captureList(capsys)
    assert captured.out == "test1\ntest3\n\n"

# TESTS DELETING ONE AT A TIME !!! NOT USING MULTI DELETE !!!
def test_do_delete_all_1(capsys):
    app.do_add("test1, test2, test3")
    captured = capsys.readouterr()

    app.do_delete("test1")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted class 'test1'\n"

    captured = captureList(capsys)
    assert captured.out == "test2\ntest3\n\n"

    app.do_delete("test2")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted class 'test2'\n"

    captured = captureList(capsys)
    assert captured.out == "test3\n\n"

    app.do_delete("test3")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted class 'test3'\n"

    captured = captureList(capsys)
    assert captured.out == "No Classes\n\n"

def test_do_delete_all_many(capsys):
    # Once again, get rid of the add output
    app.do_add("one, two, three, four")
    captured = capsys.readouterr()
    
    app.do_delete("one, two, three, four")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted class 'one'\nSuccessfully deleted class 'two'\nSuccessfully deleted class 'three'\nSuccessfully deleted class 'four'\n"

    captured = captureList(capsys)
    assert captured.out == "No Classes\n\n"
################################# TEST EDIT #################################

################################# ATTRIBUTES ################################
################################ TEST addAttr ###############################

################################ TEST delAttr ###############################

############################### TEST editAttr ###############################

############################### RELATIONSHIPS ###############################
################################ TEST addRel ################################

################################ TEST delRel ################################
