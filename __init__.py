from flask import Flask, jsonify, request
import jwt
import psycopg2
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY']="secretkey123"

key = "secret"

conn = psycopg2.connect(database='postgres',user='postgres',password='postgres',host='192.168.253.190',port='5432')
mycursor = conn.cursor()


@app.route("/home")
def home():
 return "<h1>Hello world v42 </h1>"


@app.route('/receive/post',methods=['POST'])
def receive_post():
    id=request.json['id']
    bal=request.json['bal']
    bal=str(int(bal)+30)
    data={'id':id,'bal':bal}
    return jsonify(data)


@app.route('/post-gettoken',methods=['POST'])
def postlogin():
    auth_val = request.authorization
    uname= auth_val.username
    passwd = auth_val.password
    passwd = hashlib.md5(passwd.encode()).hexdigest()
    
    try:
        fetch_query = "select password from user_tbl where user_id=" + "'" + uname + "'";
        mycursor.execute(fetch_query)
        result = mycursor.fetchall()
        db_pass = result[0][0]
        if db_pass == passwd:
            data = {"uname": uname}
            jwt_encoded = jwt.encode(data, key, algorithm='HS256')
            jwt_token = {"token": jwt_encoded}
            ret_val = {"jwt_token": jwt_token, "uname": uname}
            return (jsonify(ret_val))
        else:
            return "Invalid username/password"
    except:
        return "Invalid username/password"



@app.route('/post-getdevice-info',methods=['POST'])
def postdata1():
        # return (str(request.headers))
    try:
       tok_val = request.headers['x-auth-token']
       data = jwt.decode(tok_val, key, algorithms="HS256")
       mgmt_ip = request.json['mgmt_ip']

       fetch_query = "select hostname,device_type,hosted_dc from deviceinfo_tbl where mgmt_ip=" + "'" + mgmt_ip + "'";
       mycursor.execute(fetch_query)
       result = mycursor.fetchall()
       
       hostname = result[0][0]
       device_type = result[0][1]
       hosted_dc = result[0][2]
       device_info = {"mgmt_ip":mgmt_ip,"hostname":hostname,"device_type":device_type,"hosted_dc":hosted_dc}
       return (jsonify(device_info))
    except:
       return "Invalid Token to access /post-getdevice-info"




if __name__ == "__main__":
   app.run(host='0.0.0.0')
