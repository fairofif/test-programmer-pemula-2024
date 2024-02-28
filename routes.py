import pymysql
from flask import (
    jsonify,
    request
)
from db_config import mysql

def configure_routes(app):
# ================= STATIC METHOD =============== #
    def checkNIMIsNotExist(nim):
        query = "SELECT NIM FROM Mahasiswa WHERE NIM = '"+str(nim)+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        if cursor.rowcount == 0:
            status = True
        else:
            status = False

        cursor.close()
        conn.close()

        return status

# =============== ROUTES ================ #

    @app.route('/mahasiswa/insert', methods=['POST'])
    def insert_mahasiswa():
        data = request.json
        nim = data['NIM']
        nama_lengkap = data['NamaLengkap']
        jurusan = data['Jurusan']

        if checkNIMIsNotExist(nim) == True:
            query = "INSERT INTO Mahasiswa Values ('"+nim+"', '"+nama_lengkap+"', '"+jurusan+"')"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()

            query = "SELECT * FROM Mahasiswa"
            cursor.execute(query)
            read_row = cursor.fetchall()
            cursor.close()
            conn.close()

            response = {
                "insert_status": True,
                "message": "Insert new Mahasiswa successfully",
                "data": read_row
            }
        else:
            query = "SELECT * FROM Mahasiswa"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            read_row = cursor.fetchall()
            cursor.close()
            conn.close()

            response = {
                "insert_status": False,
                "message": "NIM cannot be duplicate",
                "data": read_row
            }

        return jsonify(response)

    @app.route('/mahasiswa/edit', methods=['PUT'])
    def edit_mahasiswa():
        data = request.json
        nim = data['NIM']
        nama_lengkap = data['NamaLengkap']
        jurusan = data['Jurusan']

        if checkNIMIsNotExist(nim) == True:
            query = "SELECT * FROM Mahasiswa"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            read_row = cursor.fetchall()
            cursor.close()
            conn.close()

            response = {
                "edit_status": False,
                "message": "NIM is not exists",
                "data": read_row
            }
        else:
            query = "UPDATE Mahasiswa SET NamaLengkap = '"+nama_lengkap+"', Jurusan = '"+jurusan+"' WHERE NIM = '"+nim+"'"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            conn.commit()

            query = "SELECT * FROM Mahasiswa"
            cursor.execute(query)
            read_row = cursor.fetchall()
            cursor.close()
            conn.close()

            response = {
                "edit_status": True,
                "message": "Edit Mahasiswa "+nim+ " success",
                "data": read_row
            }
        return jsonify(response)

    @app.route('/mahasiswa/delete', methods=['DELETE'])
    def delete_mahasiswa():
        data = request.json
        nim = data['NIM']
        query = "DELETE FROM Mahasiswa WHERE NIM = '"+nim+"'"
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query)
        conn.commit()

        query = "SELECT * FROM Mahasiswa"
        cursor.execute(query)
        read_row = cursor.fetchall()
        cursor.close()
        conn.close()

        response = {
            "delete_status": True,
            "message": "Mahasiswa with NIM = '"+nim+"' already deleted",
            "data": read_row
        }

        return jsonify(response)

    @app.route('/mahasiswa/search', methods=['GET'])
    def search_mahasiswa():
        data = request.json
        nim = data['NIM']

        if checkNIMIsNotExist(nim) == True:
            response = {
                "search_status": False,
                "message": "Mahasiswa not found",
                "data": None
            }
        else:
            query = "SELECT * FROM Mahasiswa WHERE NIM = '"+nim+"'"
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(query)
            read_row = cursor.fetchone()
            cursor.close()
            conn.close()
            response = {
                "search_status": True,
                "message": "Mahasiswa Found",
                "data": read_row
            }

        return jsonify(response)