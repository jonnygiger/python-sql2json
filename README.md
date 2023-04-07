# python-sql2json

Simple Python server that serves an SQL table in JSON format.

It currently supports insert and search operations using `GET` requests.

## Usage

### Setup the Database

The Database used in the example is setup as follows:

* Database: inventory
    * Table: items
        * Field: itemid
        * Field: name
        * Field: active

### Configure the MariaDB parameters

Input the SQL username, password, hostname, port, database name, and table name in sqltoweb.py

### Start the server

`python sqltoweb.py`

### Search for an item by name

`$ curl -X GET 'http://localhost:3002/query' -G -d search=first`

### Search for an item by itemid

`$ curl -X GET 'http://localhost:3002/query' -G -d itemid=7`

### Insert an item

`$ curl -X GET 'http://localhost:3002/insert' -G -d 'itemid=7&name=seventh&active=1'`

## Example Usage

```
$ curl -X GET 'http://localhost:3002/query' -G -d search=first
[{"itemid": 1, "name": "first", "active": 1}]
$ curl -X GET 'http://localhost:3002/query' -G -d abc=123
No valid search queries received
$ curl -X GET 'http://localhost:3002/insert' -G -d 'itemid=7&name=seventh&active=1'
Insert operation completed
$ curl -X GET 'http://localhost:3002/query' -G -d search=seventh
[{"itemid": 7, "name": "seventh", "active": 1}]
$ curl -X GET 'http://localhost:3002/query' -G -d itemid=7
[{"itemid": 7, "name": "seventh", "active": 1}]
```
