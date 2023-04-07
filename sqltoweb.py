import json
import mariadb
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

sql_username = "jonny"
sql_password = "mysecretpassword"
sql_host = "127.0.0.1"
sql_port = 3306
sql_database_name = "inventory"
sql_table_name = "items"

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=sql_username,
        password=sql_password,
        host=sql_host,
        port=sql_port,
        database=sql_database_name
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path.startswith('/query?')):
            print("Query Operation")
            searchterm = ''
            query_components = parse_qs(urlparse(self.path).query)
            print("Query: ", query_components)
            cur = conn.cursor(dictionary=True)
            table_name_sql = conn.escape_string(sql_table_name)
            if "search" in query_components:
                print("Search keywords: ", query_components["search"])
                for word in query_components["search"]:
                    print("Keyword: ", word)
                    searchterm = "%" + word + "%"
                    cur.execute("SELECT * FROM " + table_name_sql + " WHERE name LIKE ?", (searchterm,))
            elif "itemid" in query_components:
                itemid_int = int(query_components["itemid"][0])
                print("Itemid: ", itemid_int)
                cur.execute("SELECT * FROM " + table_name_sql + " WHERE itemid = ?", (itemid_int,))
            else:
                print("No valid search queries")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("No valid search queries received".encode("utf-8"))
                return
            result = cur.fetchall()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        if (self.path.startswith('/insert')):
            print("Insert operation")
            query_components = parse_qs(urlparse(self.path).query)
            print("Insert operation contents: ", query_components)
            cur = conn.cursor(dictionary=True)
            table_name_sql = conn.escape_string(sql_table_name)
            if "itemid" in query_components and "name" in query_components and "active" in query_components:
                itemid_int = int(query_components["itemid"][0])
                print("Inserting itemid=", itemid_int, ",name=", query_components["name"][0], ",active=", query_components["active"][0])
                try:
                    cur.execute("INSERT INTO " + table_name_sql + " (itemid,name,active) VALUES (?, ?, ?)", (itemid_int, query_components["name"][0], query_components["active"][0]))
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write("Insert operation completed".encode("utf-8"))
                    print("Insert completed")
                except mariadb.Error as e:
                    print(f"MariDB Error: {e}")
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    error_string = "MariaDB Error: " + str(e)
                    self.wfile.write(error_string.encode("utf-8"))
            else:
                print("Insert operation: Parameters incomplete")
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("Insert: Parameters incomplete".encode("utf-8"))
        conn.commit()

if __name__ == "__main__":        
    webServer = HTTPServer(('localhost', 3002), MyServer)
    print("Server started")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

conn.close()

