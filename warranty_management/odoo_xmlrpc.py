
import xmlrpc.client

url = 'http://localhost:8069'

db = 'warranty_management'

username = 'admin'

password = 'admin'

# to use postman in xml_rpc you should write full_url
# full_url = base url + /xmlrpc/2/common
full_url = 'http://localhost:8069/xmlrpc/2/common'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# this is for authentication:
uid = common.authenticate(db, username, password, {})
# uid = common.login(db, username, password, {})

if uid:
 print("Authenticatation successful")


 # this for read and search from database here to know how much company in model res_partner
 models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

 # create record in model res.partner
 # vals = {
 #  'name': "Odoo Mates External API ",
 #  'email': "odoomates@gmail.com ",
 # }
 # # created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name':'demo'}])
 # created_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [vals])
 # print("Created_id is:", created_id)

 # create record in model product.product
 vals = {
  'name': "Odoo Mates External API ",
 }
 # product_id = models.execute_kw(db, uid, password, 'product.product', 'create', [{'name':'demo'}])
 product_id = models.execute_kw(db, uid, password, 'product.product', 'create', [vals])
 print("product_id is:", product_id)

