"""Unit tests for core route functionality (GUI)."""

import io
################################ TEST INDEX ################################
def test_empty_base_index(test_client, init_database):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"No Classes Added" in response.data

################################ TEST ADD ################################
def test_add_empty(test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestAddEmpty'), follow_redirects=True)
    assert response.status_code == 200
    assert b"TestAddEmpty" in response.data

def test_add_dupes(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestAddDupe'), follow_redirects=True)
    response = test_client.post('/', data=dict(class_name='TestAddDupe'), follow_redirects=True)
    assert b"Unable to add class TestAddDupe" in response.data

def test_add_nondupes(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestAddDerp0'), follow_redirects=True)
    response = test_client.post('/', data=dict(class_name='TestAddDerp1'), follow_redirects=True)
    assert response.status_code == 200
    assert b"TestAddDerp0" in response.data
    assert b"TestAddDerp1" in response.data

def test_add_nondupesbutwithaspace(test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestAddDerp2() , TestAddDerp3'), follow_redirects=True)
    assert response.status_code == 200
    assert b"TestAddDerp2" in response.data
    assert b"TestAddDerp3" in response.data

def test_add_no_name(test_client, init_database):
    response = test_client.post('/', data=dict(class_name=''), follow_redirects=True)
    assert not b'id=""' in response.data

def test_add_quotes(test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestAddQuote"'), follow_redirects=True)
    assert response.status_code == 200
    assert b'ERROR: Unable to add class TestAddQuote' in response.data

################################ TEST UPDATE ################################
def test_update (test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestOriginal'), follow_redirects=True)
    assert b'TestOriginal' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]":"TestOriginal", "field[ super ][new_name]":"TestUpdate", "field[ super ][action]":"RenameClass"}, follow_redirects=True)
    assert b'TestUpdate' in response.data
    assert not b'TestOriginal' in response.data

def test_update_quotes(test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestOriginal'), follow_redirects=True)
    assert response.status_code == 200
    assert b'TestOriginal' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]":"TestOriginal", "field[ super ][new_name]":"TestUpdate'", "field[ super ][action]":"RenameClass"}, follow_redirects=True)
    assert b'TestOriginal' in response.data
    assert b'ERROR: Unable to update class TestOriginal to TestUpdate' in response.data

def test_update_to_existo (test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestOriginal, TestUpdate'), follow_redirects=True)
    assert b'TestOriginal' in response.data
    assert b'TestUpdate' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]":"TestOriginal", "field[ super ][new_name]":"TestUpdate", "field[ super ][action]":"RenameClass"}, follow_redirects=True)
    assert b'Unable to update class TestOriginal to TestUpdate'
    assert b'TestOriginal' in response.data
    assert b'TestUpdate' in response.data

def test_update_invalid_args (test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestOriginal'), follow_redirects=True)
    assert b'TestOriginal' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]":None, "field[ super ][new_name]":"TestUpdate", "field[ super ][action]":"RenameClass"}, follow_redirects=True)
    assert b'Invalid arguments, try again.'
    assert b'TestOriginal' in response.data

def test_update_with_characteristics (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass, TestClass2'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestClass" in response.data
    assert b"TestClass2" in response.data
    assert b"TestAttr" in response.data

    test_client.post('/addRelationship/', data=dict(class_name='TestClass', to='TestClass2', rel_type='agg'), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass", "rel_type": "agg", "to_name": "TestClass2"}' in response.data

    test_client.post('/addRelationship/', data=dict(class_name='TestClass2', to='TestClass', rel_type='gen'), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass2", "rel_type": "gen", "to_name": "TestClass"}' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]":"TestClass", "field[ super ][new_name]":"TestUpdate", "field[ super ][action]":"RenameClass"}, follow_redirects=True)
    assert b"TestClass2" in response.data
    assert b"TestAttr" in response.data
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert b'{"from_name": "TestClass2", "rel_type": "gen", "to_name": "TestUpdate"}' in response.data
    assert b'{"from_name": "TestUpdate", "rel_type": "agg", "to_name": "TestClass2"}' in response.data

################################ TEST DELETE ################################
def test_delete (test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestAddToDelete'), follow_redirects=True)
    assert b"TestAddToDelete" in response.data
    response = test_client.post('/delete/', data=dict(delete='TestAddToDelete'), follow_redirects=True)
    assert b"No Classes Added" in response.data

def test_delete_no_existo (test_client, init_database):
    response = test_client.post('/delete/', data=dict(delete='TestDelete'), follow_redirects=True)
    assert b"Unable to delete class TestDelete" in response.data

def test_delete_no_name (test_client, init_database):
    response = test_client.post('/delete/', data=dict(delete=None), follow_redirects=True)
    assert b"Invalid name" in response.data

def test_delete_with_characteristics (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass, TestClass2'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestClass" in response.data
    assert b"TestClass2" in response.data
    assert b"TestAttr" in response.data

    test_client.post('/addRelationship/', data=dict(class_name='TestClass', to='TestClass2', rel_type='agg'), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass", "rel_type": "agg", "to_name": "TestClass2"}' in response.data

    test_client.post('/addRelationship/', data=dict(class_name='TestClass2', to='TestClass', rel_type='gen'), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass2", "rel_type": "gen", "to_name": "TestClass"}' in response.data

    response = test_client.post('/delete/', data=dict(delete='TestClass'), follow_redirects=True)
    assert b"TestClass2" in response.data
    assert not b"TestAttr" in response.data
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert not b'{"from_name": "TestClass2", "rel_type": "gen", "to_name": "TestClass"}' in response.data
    assert not b'{"from_name": "TestClass", "rel_type": "agg", "to_name": "TestClass2"}' in response.data


################################ TEST LOAD ################################

def test_load_good (test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestAddEmpty'), follow_redirects=True)
    assert response.status_code == 200
    assert b"TestAddEmpty" in response.data

    jFile = io.BytesIO(b"""[
    {
        "class_attributes": [
            {
                "attr_type": "field",
                "attribute": "please help",
                "class_name": "Friendship ended with SQLALCHEMY-MARSHMALLOW",
                "date_created": "2020-04-03T03:10:40.883665"
            }
        ],
        "class_relationships": [
            {
                "from_name": "Friendship ended with SQLALCHEMY-MARSHMALLOW",
                "rel_type": "agg",
                "to_name": "Now DEPRESSION is my best friend"
            }
        ],
        "date_created": "2020-04-03T03:09:38.770317",
        "name": "Friendship ended with SQLALCHEMY-MARSHMALLOW",
        "x": 675,
        "y": 42
    },
    {
        "class_attributes": [
            {
                "attr_type": "method",
                "attribute": "seriously though",
                "class_name": "Now DEPRESSION is my best friend",
                "date_created": "2020-04-03T03:11:00.813333"
            }
        ],
        "class_relationships": [],
        "date_created": "2020-04-03T03:09:38.790341",
        "name": "Now DEPRESSION is my best friend",
        "x": 100,
        "y": 74
    }
]""")
    response = test_client.post('/load/', data=dict(file=(jFile, 'temp.json')), content_type='multipart/form-data', follow_redirects=True)
    assert b"Friendship ended" in response.data
    assert b"please help" in response.data
    assert b"DEPRESSION" in response.data
    assert not b"TestAddEmpty" in response.data
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert b'{"from_name": "Friendship ended with SQLALCHEMY-MARSHMALLOW", "rel_type": "agg", "to_name": "Now DEPRESSION is my best friend"}' in response.data

def test_load_invalid_json_attributes (test_client, init_database):
    jFile = io.BytesIO(b"""[
    {
        "derp_create": "2020-02-13T15:36:32.536751",
        "nama": "Howdy",
        "ex": 2799,
        "why": 1595
    },
    {
        "date_create": "2020-02-13T15:36:36.205104",
        "name": "Plane",
        "x": 2542,
        "y": 1534
    },
    {
        "date_created": "2020-02-13T15:37:06.798737",
        "gnome": "pardner",
        "x": 3293,
        "y": 1540
    }
    ]""")
    response = test_client.post('/load/', data=dict(file=(jFile, 'temp.json')), content_type='multipart/form-data', follow_redirects=True)
    assert b"Unable to load data into database" in response.data

def test_load_from_empty (test_client, init_database):
    jFile = io.BytesIO(b"[]")
    response = test_client.post('/load/', data=dict(file=(jFile, 'temp.json')), content_type='multipart/form-data', follow_redirects=True)
    assert b"No Classes Added" in response.data

def test_load_not_even_json (test_client, init_database):
    jFile = io.BytesIO(b"")
    response = test_client.post('/load/', data=dict(file=(jFile, 'temp.json')), content_type='multipart/form-data', follow_redirects=True)
    assert b"Invalid JSON" in response.data

def test_load_quotes (test_client, init_database):
    jFile = io.BytesIO(b"""[
    {
        "class_attributes": [
            {
                "attr_type": "field",
                "attribute": "please help",
                "class_name": "Friendship ended with SQLALCHEMY-MARSHMALLOW",
                "date_created": "2020-04-03T03:10:40.883665"
            }
        ],
        "class_relationships": [
            {
                "from_name": "Friendship ended with SQLALCHEMY-MARSHMALLOW",
                "rel_type": "agg",
                "to_name": "Now DEPRESSION is my best friend"
            }
        ],
        "date_created": "2020-04-03T03:09:38.770317",
        "name": "Friendship ended with SQLALCHEMY-MARSHMALLOW",
        "x": 675,
        "y": 42
    },
    {
        "class_attributes": [
            {
                "attr_type": "method",
                "attribute": "seriously though",
                "class_name": "Now DEPRESSION is my best friend",
                "date_created": "2020-04-03T03:11:00.813333"
            }
        ],
        "class_relationships": [],
        "date_created": "2020-04-03T03:09:38.790341",
        "name": "Now DEPRESSION is my best friend'",
        "x": 100,
        "y": 74
    }
]""")
    response = test_client.post('/load/', data=dict(file=(jFile, 'temp.json')), content_type='multipart/form-data', follow_redirects=True)
    assert b"ERROR: Unable to load data into database" in response.data

    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert not b'{"from_name": "Friendship ended with SQLALCHEMY-MARSHMALLOW", "rel_type": "agg", "to_name": "Now DEPRESSION is my best friend"}' in response.data

################################ TEST SAVE ################################

def test_save(test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestAddToSave'), follow_redirects=True)
    assert response.status_code == 200
    assert b"TestAddToSave" in response.data

    response = test_client.post('/save/', data=dict(save_name='TestSave'), follow_redirects=True)

    assert b'"name": "TestAddToSave"' in response.data
    assert "filename=TestSave.json" in response.headers['Content-Disposition']

def test_save_no_name(test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestAddToSave'), follow_redirects=True)
    assert response.status_code == 200
    assert b"TestAddToSave" in response.data

    response = test_client.post('/save/', data=dict(save_name=None), follow_redirects=True)

    assert b"There was a problem saving. Try again." in response.data

################################ TEST ATTRIBUTE ################################

def test_add_attribute_to_class_no_existo(test_client, init_database):
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"ERROR: Unable to add attribute TestAttr to TestClass" in response.data

def test_add_one_attribute(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert b"TestAttr" in response.data

def test_add_duplicate_attribute(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert b"TestAttr" in response.data
    assert b"ERROR: Unable to add attribute TestAttr to TestClass" in response.data

def test_add_one_attribute_but_then_delete_that_attribute(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestAttr" in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttr", "field[TestAttr][action]":"Delete", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert not b"TestAttr" in response.data

def test_delete_attribute_no_existo (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestAttr" in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttrAAA", "field[TestAttr][action]":"Delete", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert b"TestAttr" in response.data
    assert b"Unable to remove attribute TestAttrAAA from TestClass"

def test_rename_attribute (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b'TestAttr' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttr", "field[TestAttr][action]":None, "field[ super ][class_name]":"TestClass", "field[TestAttr][new_attribute]":"TestUpdate"}, follow_redirects=True)
    assert not b'TestAttr' in response.data
    assert b'TestUpdate' in response.data

def test_rename_attribute_no_existo (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestAttr" in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttrAAA", "field[TestAttr][action]":None, "field[ super ][class_name]":"TestClass", "field[TestAttr][new_attribute]":"TestUpdate"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert b"TestAttr" in response.data
    assert b"Unable to update attribute TestAttrAAA in TestClass to TestUpdate"

def test_attribute_invalid_args (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b'TestAttr' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttr", "field[TestAttr][action]":None, "field[ super ][class_name]":"TestClass", "field[TestAttr][new_attribute]":None}, follow_redirects=True)
    assert b'TestAttr' in response.data
    assert b'Invalid arguments, try again' in response.data

def test_rename_attribute_auto_add_rel (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass, TestType'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b'TestAttr' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttr", "field[TestAttr][action]":None, "field[ super ][class_name]":"TestClass", "field[TestAttr][new_attribute]":"TestType yes"}, follow_redirects=True)
    assert not b'TestAttr' in response.data
    assert b'TestType yes' in response.data

    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass", "rel_type": "agg", "to_name": "TestType"}' in response.data

def test_add_attribute_auto_add_rel (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass, TestType'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestType yes", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b'TestType yes' in response.data

    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass", "rel_type": "agg", "to_name": "TestType"}' in response.data

################################ TEST RELATIONSHIPS ################################

def test_add_one_relationship(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    test_client.post('/addRelationship/', data=dict(class_name='TestClass1', to='TestClass2', rel_type='agg'), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass1", "rel_type": "agg", "to_name": "TestClass2"}' in response.data

def test_add_many_relationships(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    test_client.post('/addRelationship/', data=dict(class_name='TestClass1', to='TestClass2', rel_type='agg'), follow_redirects=True)
    test_client.post('/addRelationship/', data=dict(class_name='TestClass1', to='TestClass1', rel_type='agg'), follow_redirects=True)
    test_client.post('/addRelationship/', data=dict(class_name='TestClass2', to='TestClass1', rel_type='agg'), follow_redirects=True)
    test_client.post('/addRelationship/', data=dict(class_name='TestClass2', to='TestClass2', rel_type='agg'), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass1", "rel_type": "agg", "to_name": "TestClass2"}' in response.data
    assert b'{"from_name": "TestClass2", "rel_type": "agg", "to_name": "TestClass1"}' in response.data
    assert b'{"from_name": "TestClass1", "rel_type": "agg", "to_name": "TestClass1"}' in response.data
    assert b'{"from_name": "TestClass2", "rel_type": "agg", "to_name": "TestClass2"}' in response.data

def test_add_one_relationship_but_then_delete_that_relationship(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    test_client.post('/addRelationship/', data=dict(class_name='TestClass1', to='TestClass2', rel_type='agg'), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass1", "rel_type": "agg", "to_name": "TestClass2"}' in response.data

    test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]":"TestClass1", "field[ super ][action]":"RenameClass", "field[ super ][new_name]":"TestClass1", "field[TestClass2][action]":"DeleteRel", "field[TestClass2][to_name]":"TestClass2"}, follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert not b'{"from_name": "TestClass1", "rel_type": "agg", "to_name": "TestClass2"}' in response.data

def test_add_one_relationship_but_its_for_a_class_that_doesnt_exist(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    response = test_client.post('/addRelationship/', data=dict(class_name='TestClass2', to='TestClass69', rel_type='agg'), follow_redirects=True)
    assert b"ERROR: Unable to add relationship from" in response.data

    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert not b'{"from_name": "TestClass1", "to_name": "TestClass69"}' in response.data

def test_delete_a_relationship_that_didnt_exist_in_the_first_place(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]": "TestClass2", "field[ super ][action]":"RenameClass", "field[ super ][new_name]":"TestClass2", "field[TestClass69][action]": "DeleteRel", "field[TestClass69][to_name]": "TestClass69"}, follow_redirects=True)
    assert b"ERROR: Unable to delete relationship from TestClass2 to" in response.data

def test_add_relationship_invalid_args (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    response = test_client.post('/addRelationship/', data=dict(class_name=None, to='howdy', rel_type='agg'), follow_redirects=True)
    assert b"Invalid arguments, try again." in response.data

################################ TEST COORDINATES ################################

def test_update_coords (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1'), follow_redirects=True)
    response = test_client.post('/updateCoords/', data=dict(name='TestClass1', left=500, top=42), follow_redirects=True)
    assert b"Name: TestClass1\nX: 500\nY: 42" in response.data

    response = test_client.get('/', follow_redirects=True)
    assert b"left: 500px;" in response.data
    assert b"top: 42px;" in response.data
    
################################ TEST CLEAR ################################

def test_clear (test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestClass1'), follow_redirects=True)
    assert b"TestClass1" in response.data
    
    response = test_client.post('/clear/', follow_redirects=True)
    assert b"TestClass1" not in response.data
    assert b"No Classes Added" in response.data

################################ TEST UNDO/REDO ################################

def test_add_undo_redo (test_client, init_database):
    initialState = test_client.get('/')
    SecondState = test_client.post('/', data=dict(class_name='Test'), follow_redirects=True)
    
    response = test_client.post('/undo/', follow_redirects=True)
    assert initialState.data == response.data
    response = test_client.post('/redo/', follow_redirects=True)
    assert SecondState.data == response.data

def test_rename_undo_redo (test_client, init_database):
    initialState = test_client.post('/', data=dict(class_name='TestOriginal'), follow_redirects=True)
    SecondState = test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]":"TestOriginal", "field[ super ][new_name]":"TestUpdate", "field[ super ][action]":"RenameClass"}, follow_redirects=True)
    
    response = test_client.post('/undo/', follow_redirects=True)
    assert initialState.data == response.data
    response = test_client.post('/redo/', follow_redirects=True)
    assert SecondState.data == response.data
    
def test_delete_undo_redo (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    InitialState = test_client.post('/addRelationship/', data=dict(class_name='TestClass', to='TestClass', rel_type='agg'), follow_redirects=True)
    SecondState = test_client.post('/delete/', data=dict(delete='TestClass'), follow_redirects=True)
    
    response = test_client.post('/undo/', follow_redirects=True)
    assert InitialState.data == response.data
    response = test_client.post('/redo/', follow_redirects=True)
    assert SecondState.data == response.data
    
def test_addAttr_undo_redo (test_client, init_database):
    
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestAttr" in response.data
    
    response = test_client.post('/undo/', follow_redirects=True)
    assert not b"TestAttr" in response.data
    response = test_client.post('/redo/', follow_redirects=True)
    assert b"TestAttr" in response.data

def test_delAttr_undo_redo(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][attr_type]":"field", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestAttr" in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttr", "field[TestAttr][action]":"Delete", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert not b"TestAttr" in response.data
    
    response = test_client.post('/undo/', follow_redirects=True)
    assert b"TestAttr" in response.data
    response = test_client.post('/redo/', follow_redirects=True)
    assert not b"TestAttr" in response.data

def test_empty_undo_redo_stacks (test_client, init_database):
    initialState = test_client.get('/')
    
    response = test_client.post('/undo/', follow_redirects=True)
    assert initialState.data == response.data

    initialState = test_client.post('/', data=dict(class_name='TestOriginal'), follow_redirects=True)
    response = test_client.post('/redo/', follow_redirects=True)
    assert initialState.data == response.data