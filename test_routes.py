from db_config import mysql
import pymysql
from app import app
from dotenv import load_dotenv
load_dotenv()

# ========================== STATIC METHOD ======================= #
def insert_unittest_mahasiswa():
    query = "INSERT INTO Mahasiswa Values ('1122334455', 'Unit Test', 'Unit Test Jurusan')"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete_unittest_mahasiswa():
    query = "DELETE FROM Mahasiswa WHERE NIM = '1122334455'"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


# ============================ TEST ========================== #

def test_import_success():
    client = app.test_client()
    url = 'mahasiswa/insert'

    body = {
        "NIM": "1122334455",
        "NamaLengkap": "Unit Test",
        "Jurusan": "Teknik Informatika"
    }

    response = client.post(url, json=body)

    delete_unittest_mahasiswa()

    assert response.status_code == 200
    assert response.get_json()["insert_status"] == True

def test_import_failed():
    client = app.test_client()
    url = 'mahasiswa/insert'

    insert_unittest_mahasiswa()

    body = {
        "NIM": "1122334455",
        "NamaLengkap": "Unit Test",
        "Jurusan": "Teknik Informatika"
    }

    response = client.post(url, json=body)

    delete_unittest_mahasiswa()

    assert response.status_code == 200
    assert response.get_json()["insert_status"] == False

def test_edit_success():
    client = app.test_client()
    url = 'mahasiswa/edit'

    insert_unittest_mahasiswa()

    body = {
        "NIM": "1122334455",
        "NamaLengkap": "New Nama",
        "Jurusan": "New Jurusan"
    }

    response = client.put(url, json=body)

    delete_unittest_mahasiswa()

    assert response.status_code == 200
    assert response.get_json()["edit_status"] == True

def test_edit_failed():
    client = app.test_client()
    url = 'mahasiswa/edit'

    insert_unittest_mahasiswa()

    body = {
        "NIM": "1122334488",
        "NamaLengkap": "New Nama",
        "Jurusan": "New Jurusan"
    }

    response = client.put(url, json=body)

    delete_unittest_mahasiswa()

    assert response.status_code == 200
    assert response.get_json()["edit_status"] == False

def test_delete_success():
    client = app.test_client()
    url = 'mahasiswa/delete'

    insert_unittest_mahasiswa()

    body = {
        "NIM": "1122334455"
    }

    response = client.delete(url, json=body)

    assert response.status_code == 200
    assert response.get_json()["delete_status"] == True

def test_search_data_success():
    client = app.test_client()
    url = 'mahasiswa/search'

    insert_unittest_mahasiswa()

    body = {
        "NIM": "1122334455"
    }

    response = client.get(url, json=body)

    delete_unittest_mahasiswa()

    assert response.status_code == 200
    assert response.get_json()["search_status"] == True