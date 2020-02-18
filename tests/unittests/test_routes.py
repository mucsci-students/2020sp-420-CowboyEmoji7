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
    assert b"Unable to add Class" in response.data

def test_add_nondupes(test_client, init_database):
    test_client.post('/', data=dict(class_name='TestAddDerp0'), follow_redirects=True)
    response = test_client.post('/', data=dict(class_name='TestAddDerp1'), follow_redirects=True)
    assert response.status_code == 200
    assert b"TestAddDerp0" in response.data
    assert b"TestAddDerp1" in response.data

def test_add_no_name(test_client, init_database):
    response = test_client.post('/', data=dict(class_name=''), follow_redirects=True)
    assert not b'id=""' in response.data

################################ TEST DELETE ################################
def test_delete (test_client, init_database):
    response = test_client.post('/', data=dict(class_name='TestAddToDelete'), follow_redirects=True)
    assert b"TestAddToDelete" in response.data
    response = test_client.get('/delete/TestAddToDelete', follow_redirects=True)
    assert b"No Classes Added" in response.data

def test_delete_no_existo (test_client, init_database):
    response = test_client.get('/delete/TestDelete', follow_redirects=True)
    assert b"Unable to delete Class" in response.data

################################ TEST LOAD ################################

def test_load_good (test_client, init_database):
    jFile = io.BytesIO(b"""[
    {
        "date_created": "2020-02-13T15:36:32.536751",
        "name": "Howdy",
        "x": 2799,
        "y": 1595
    },
    {
        "date_created": "2020-02-13T15:36:36.205104",
        "name": "Plane",
        "x": 2542,
        "y": 1534
    },
    {
        "date_created": "2020-02-13T15:37:06.798737",
        "name": "pardner",
        "x": 3293,
        "y": 1540
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