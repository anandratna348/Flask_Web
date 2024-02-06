1)import the following libraries flask,flask_sqlalchemy,flask_restful,flask_cors,json,os,werkzeug.exceptions
2)after installing the required libraries type python app.py in terminal.
3)now the server will run the program on url http://127.0.0.1:5000.
4)you can access it on the above link.
5)if you are a admin login in admin login or else you should login from login form.
6)admin can add edit and delete categories.
7)api for categories-------->  get,put,delete requests for category will be available at http://127.0.0.1:5000/api/category/<int:id>
                          post will be available at http://127.0.0.1:5000.api/category
8)api for product-------->  get,put,delete requests for product will be available at http://127.0.0.1:5000/api/product/<int:id>
                          post will be available at http://127.0.0.1:5000.api/product
9)you can test api through submitted yaml file.
10)if we get a error name none type then do db.__create__all().

---------Folder Tree Diagram------------
Folder PATH listing for volume OS
Volume serial number is 8467-E901
C:.
+---project files
+---static
+---templates
+---__pycache__