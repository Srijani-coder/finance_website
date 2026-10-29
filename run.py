from app import app
if __name__ == '__main__':
 print('Local site: http://127.0.0.1:5000')
 print('Admin login: http://127.0.0.1:5000/admin/login')
 app.run(host='127.0.0.1',port=5000,debug=False)
