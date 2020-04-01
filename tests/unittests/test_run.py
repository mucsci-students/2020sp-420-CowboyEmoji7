""" Unit tests for run.py/Command Line Interface 

    Tests:
    [X] add             [] redo
    [X] delete          [X] fields
    [X] edit            [X] methods
    [X] relationships   [] save
    [] undo             [] load
"""

import run

#################################### SETUP ##################################
app = run.replShell()

# lazy mans way of capturing list
def captureList(capsys):
    app.do_list("")
    captured = capsys.readouterr()
    return captured

# builds an editor frame for testing attributes
# so I don't have to retype the same thing over and over again
# also captures the add output for me
def attribute_frame(capsys):
    app.do_add("test, morestuff")
    captured = capsys.readouterr()
    return captured

################################ TEST COMMANDS ##############################
# Test list and maybe save/load

################################### CLASS ###################################
################################## TEST add #################################
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

################################ TEST delete ################################
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

# Tests deleting many using MULTI DELETE
def test_do_delete_all_many(capsys):
    # Once again, get rid of the add output
    app.do_add("one, two, three, four")
    captured = capsys.readouterr()
    
    app.do_delete("one, two, three, four")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted class 'one'\nSuccessfully deleted class 'two'\nSuccessfully deleted class 'three'\nSuccessfully deleted class 'four'\n"

    captured = captureList(capsys)
    assert captured.out == "No Classes\n\n"

################################# TEST edit #################################
def test_do_edit(capsys):
    #Capture add class
    app.do_add("test")
    captured = capsys.readouterr()

    app.do_edit("test, newtest")
    captured = capsys.readouterr()
    assert captured.out == "Successfully updated class 'test' to 'newtest'\n"

    captured = captureList(capsys)
    assert captured.out == "newtest\n\n"

def test_do_edit_none(capsys):
    app.do_edit("test")
    captured = capsys.readouterr()
    assert captured.out == "Usage: edit <old_name>, <new_name>\n"

def test_do_edit_deleted_class(capsys):
    #Capture add class
    app.do_add("test, ooga, booga")
    captured = capsys.readouterr()

    #Capture delete
    app.do_delete("test")
    captured = capsys.readouterr()

    app.do_edit("test, thisshouldntexist")
    app.do_edit("ooga, thisexists")
    captured = capsys.readouterr()
    assert captured.out == "ERROR: Unable to update class 'test' to 'thisshouldntexist'\nSuccessfully updated class 'ooga' to 'thisexists'\n"

    captured = captureList(capsys)
    assert captured.out == "thisexists\nbooga\n\n"

############################### FIELDS/METHODS ##############################
################################ TEST addAttr ###############################

# Fields
def test_addAttr_one_field(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, field, onefield")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added field 'onefield'\n"

    captured = captureList(capsys)
    assert captured.out == "test\n  > Fields: onefield\nmorestuff\n\n"

def test_addAttr_multi_fields(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("morestuff, field, onefield, twofields, redfield, bluefield")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added field 'onefield'\nSuccessfully added field 'twofields'\nSuccessfully added field 'redfield'\nSuccessfully added field 'bluefield'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n  > Fields: onefield, twofields, redfield, bluefield\n\n"

def test_addAttr_no_fields(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, field, ")
    captured = capsys.readouterr()
    assert captured.out == "Usage: addAttr <class_name>, <field/method>, <attribute1>, <attribute2>, ... , <attributeN>\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n\n"

def test_addAttr_dup_field(capsys):
    captured = attribute_frame(capsys)
    # first add a duplicate using multi add
    app.do_addAttr("morestuff, field, dup, dup")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added field 'dup'\nERROR: Unable to add field 'dup'\n"

    app.do_addAttr("morestuff, field, dup")
    captured = capsys.readouterr()
    assert captured.out == "ERROR: Unable to add field 'dup'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n  > Fields: dup\n\n"

# Methods
def test_addAttr_one_method(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, method, onemethod")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added method 'onemethod'\n"

    captured = captureList(capsys)
    assert captured.out == "test\n  > Methods: onemethod\nmorestuff\n\n"

def test_addAttr_multi_methods(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("morestuff, method, onemethod, twomethods, redmethod, bluemethod")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added method 'onemethod'\nSuccessfully added method 'twomethods'\nSuccessfully added method 'redmethod'\nSuccessfully added method 'bluemethod'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n  > Methods: onemethod, twomethods, redmethod, bluemethod\n\n"

def test_addAttr_no_method(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, method, ")
    captured = capsys.readouterr()
    assert captured.out == "Usage: addAttr <class_name>, <field/method>, <attribute1>, <attribute2>, ... , <attributeN>\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n\n"

def test_addAttr_dup_method(capsys):
    captured = attribute_frame(capsys)
    # first add a duplicate using multi add
    app.do_addAttr("morestuff, method, dup, dup")
    captured = capsys.readouterr()
    assert captured.out == "Successfully added method 'dup'\nERROR: Unable to add method 'dup'\n"

    app.do_addAttr("morestuff, method, dup")
    captured = capsys.readouterr()
    assert captured.out == "ERROR: Unable to add method 'dup'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n  > Methods: dup\n\n"

################################ TEST delAttr ###############################
def test_delAttr_one_field(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, field, onefield")
    captured = capsys.readouterr()

    app.do_delAttr("test, onefield")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted attribute 'onefield'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n\n"

def test_delAttr_one_method(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, method, onemethod")
    captured = capsys.readouterr()

    app.do_delAttr("test, onemethod")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted attribute 'onemethod'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n\n"

def test_delAttr_multi_fields(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, field, onefield, twofields, redfield, bluefield")
    captured = capsys.readouterr()

    app.do_delAttr("test, onefield, twofields, redfield, bluefield")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted attribute 'onefield'\nSuccessfully deleted attribute 'twofields'\nSuccessfully deleted attribute 'redfield'\nSuccessfully deleted attribute 'bluefield'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n\n"

def test_delAttr_multi_methods(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, method, onemethod, twomethods, redmethod, bluemethod")
    captured = capsys.readouterr()

    app.do_delAttr("test, onemethod, twomethods, redmethod, bluemethod")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted attribute 'onemethod'\nSuccessfully deleted attribute 'twomethods'\nSuccessfully deleted attribute 'redmethod'\nSuccessfully deleted attribute 'bluemethod'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n\n"

def test_delAttr_both_same_class(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, field, onemethod")
    app.do_addAttr("test, method, onefield")
    captured = capsys.readouterr()

    app.do_delAttr("test, onemethod, onefield")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted attribute 'onemethod'\nSuccessfully deleted attribute 'onefield'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n\n"

def test_delAttr_both_diff_class(capsys):
    captured = attribute_frame(capsys)
    app.do_addAttr("test, field, onefield, twofields")
    app.do_addAttr("morestuff, method, onemethod, twomethods")
    captured = capsys.readouterr()

    app.do_delAttr("test, onefield, twofields")
    app.do_delAttr("morestuff, onemethod, twomethods")
    captured = capsys.readouterr()
    assert captured.out == "Successfully deleted attribute 'onefield'\nSuccessfully deleted attribute 'twofields'\nSuccessfully deleted attribute 'onemethod'\nSuccessfully deleted attribute 'twomethods'\n"

    captured = captureList(capsys)
    assert captured.out == "test\nmorestuff\n\n"

def test_delAttr_none(capsys):
    captured = attribute_frame(capsys)

    # first start when theres no attributes
    app.do_delAttr("test, onefield")
    captured = capsys.readouterr()
    assert captured.out == "ERROR: Unable to delete attribute 'onefield'\n"

    # now add an attribute and try to delete nothing
    app.do_addAttr("test, field, onefield")
    captured = capsys.readouterr()

    app.do_delAttr("test, ")
    captured = capsys.readouterr()
    assert captured.out == "Usage: delAttr <class_name>, <attribute1>, <attribute2>, ... , <attributeN>\n"

    captured = captureList(capsys)
    assert captured.out == "test\n  > Fields: onefield\nmorestuff\n\n"

############################### RELATIONSHIPS ###############################
################################ TEST addRel ################################

################################ TEST delRel ################################

################################# UNDO/REDO #################################