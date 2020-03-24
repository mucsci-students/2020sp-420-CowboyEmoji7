"""Unit tests for core route functionality."""

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
    response = test_client.post('/', data=dict(class_name='TestAddDerp2, TestAddDerp3'), follow_redirects=True)
    assert response.status_code == 200
    assert b"TestAddDerp2" in response.data
    assert b"TestAddDerp3" in response.data

def test_add_no_name(test_client, init_database):
    response = test_client.post('/', data=dict(class_name=''), follow_redirects=True)
    assert not b'id=""' in response.data

################################ TEST UPDATE ################################
def test_update (test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestOriginal'), follow_redirects=True)
    assert b'TestOriginal' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[ super ][class_name]":"TestOriginal", "field[ super ][new_name]":"TestUpdate", "field[ super ][action]":"RenameClass"}, follow_redirects=True)
    assert b'TestUpdate' in response.data
    assert not b'TestOriginal' in response.data

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

################################ TEST LOAD ################################

def test_load_good (test_client, init_database):
    jFile = io.BytesIO(b"""[
    {
        "class_attributes": [],
        "class_relationships": [],
        "date_created": "2020-02-19T21:22:18.116981",
        "name": "Plane",
        "x": 542,
        "y": 514
    },
    {
        "class_attributes": [],
        "class_relationships": [],
        "date_created": "2020-02-19T21:22:18.116981",
        "name": "pardner",
        "x": 285,
        "y": 201
    },
    {
        "class_attributes": [
            {
                "attribute": "seven",
                "class_name": "Howdy"
            }
        ],
        "class_relationships": [
            {
                "from_name": "Howdy",
                "to_name": "Plane"
            }
        ],
        "date_created": "2020-02-19T21:22:18.116981",
        "name": "Howdy",
        "x": 305,
        "y": 413
    }
    ]""")
    response = test_client.post('/load/', data=dict(file=(jFile, 'temp.json')), content_type='multipart/form-data', follow_redirects=True)
    assert b"Howdy" in response.data
    assert b"pardner" in response.data
    assert b"Plane" in response.data

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

def test_add_one_attribute(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert b"TestAttr" in response.data

def test_add_duplicate_attribute(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert b"TestAttr" in response.data
    assert b"ERROR: Unable to add attribute TestAttr to TestClass" in response.data

def test_add_one_attribute_but_then_delete_that_attribute(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestAttr" in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttr", "field[TestAttr][action]":"Delete", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert not b"TestAttr" in response.data

def test_delete_attribute_no_existo (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestAttr" in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttrAAA", "field[TestAttr][action]":"Delete", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert b"TestAttr" in response.data
    assert b"Unable to remove attribute TestAttrAAA from TestClass"

def test_rename_attribute (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b'TestAttr' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttr", "field[TestAttr][action]":None, "field[ super ][class_name]":"TestClass", "field[TestAttr][new_attribute]":"TestUpdate"}, follow_redirects=True)
    assert not b'TestAttr' in response.data
    assert b'TestUpdate' in response.data

def test_rename_attribute_no_existo (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b"TestAttr" in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttrAAA", "field[TestAttr][action]":None, "field[ super ][class_name]":"TestClass", "field[TestAttr][new_attribute]":"TestUpdate"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"TestClass" in response.data
    assert b"TestAttr" in response.data
    assert b"Unable to update attribute TestAttrAAA in TestClass to TestUpdate"

def test_attribute_invalid_args (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass'), follow_redirects=True)
    response = test_client.post('/manipCharacteristics/', data={"field[ class ][attrs]":"TestAttr", "field[ class ][action]":"Add", "field[ super ][class_name]":"TestClass"}, follow_redirects=True)
    assert b'TestAttr' in response.data

    response = test_client.post('/manipCharacteristics/', data={"field[TestAttr][attribute]":"TestAttr", "field[TestAttr][action]":None, "field[ super ][class_name]":"TestClass", "field[TestAttr][new_attribute]":None}, follow_redirects=True)
    assert b'TestAttr' in response.data
    assert b'Invalid arguments, try again' in response.data

################################ TEST RELATIONSHIPS ################################

def test_add_one_relationship(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    test_client.post('/manipRelationship/', data=dict(class_name='TestClass1', relationship=['TestClass2'], action="add"), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass1", "to_name": "TestClass2"}' in response.data

def test_add_many_relationships(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    test_client.post('/manipRelationship/', data=dict(class_name='TestClass1', relationship=['TestClass2', 'TestClass1'], action="add"), follow_redirects=True)
    test_client.post('/manipRelationship/', data=dict(class_name='TestClass2', relationship=['TestClass1', 'TestClass2'], action="add"), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass1", "to_name": "TestClass2"}' in response.data
    assert b'{"from_name": "TestClass2", "to_name": "TestClass1"}' in response.data
    assert b'{"from_name": "TestClass1", "to_name": "TestClass1"}' in response.data
    assert b'{"from_name": "TestClass2", "to_name": "TestClass2"}' in response.data

def test_add_two_relationships(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    test_client.post('/manipRelationship/', data=dict(class_name='TestClass1', relationship=['TestClass2','TestClass1'], action="add"), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass1", "to_name": "TestClass2"}' in response.data
    assert b'{"from_name": "TestClass1", "to_name": "TestClass1"}' in response.data

def test_add_one_relationship_but_then_delete_that_relationship(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    test_client.post('/manipRelationship/', data=dict(class_name='TestClass1', relationship=['TestClass2'], action="add"), follow_redirects=True)
    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert b'{"from_name": "TestClass1", "to_name": "TestClass2"}' in response.data

    response = test_client.post('/manipRelationship/', data=dict(class_name='TestClass1', relationship=['TestClass2'], action="delete"), follow_redirects=True)
    assert response.status_code == 200
    assert not b'{"from_name": "TestClass1", "to_name": "TestClass2"}' in response.data

def test_add_one_relationship_but_its_for_a_class_that_doesnt_exist(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    response = test_client.post('/manipRelationship/', data=dict(class_name='TestClass2', relationship=['TestClass69'], action="add"), follow_redirects=True)
    assert b"ERROR: Unable to add relationship from" in response.data

    response = test_client.post('/getRelationships/', follow_redirects=True)
    assert response.status_code == 200
    assert not b'{"from_name": "TestClass1", "to_name": "TestClass69"}' in response.data

def test_delete_a_relationship_that_didnt_exist_in_the_first_place(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1 TestClass2'), follow_redirects=True)
    response = test_client.post('/manipRelationship/', data=dict(class_name='TestClass2', relationship=['TestClass69'], action="delete"), follow_redirects=True)
    assert b"ERROR: Unable to delete relationship from" in response.data

def test_manip_relationship_invalid_args (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1, TestClass2'), follow_redirects=True)
    response = test_client.post('/manipRelationship/', data=dict(class_name=None, relationship=[], action="add"), follow_redirects=True)
    assert b"Invalid arguments, try again." in response.data

################################ TEST COORDINATES ################################

def test_update_coords (test_client, init_database):
    test_client.post('/', data=dict(class_name='TestClass1'), follow_redirects=True)
    response = test_client.post('/updateCoords/', data=dict(name='TestClass1', left=500, top=42), follow_redirects=True)
    assert b"Name: TestClass1\nX: 500\nY: 42" in response.data

    response = test_client.get('/', follow_redirects=True)
    assert b"left: 500px;" in response.data
    assert b"top: 42px;" in response.data