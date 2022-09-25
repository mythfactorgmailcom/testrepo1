from flask import Flask, jsonify, request
import jwt
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY']="secretkey123"

key = "secret"

conn = psycopg2.connect(database='postgres',user='postgres',password='postgres',host='192.168.253.190',port='5432')
mycursor = conn.cursor()


@app.route("/home")
def home():
 return "<h1>Hello world v38 </h1>"


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


@app.route('/post-getdata',methods=['POST'])
def postdata():
        # return (str(request.headers))
    try:
       tok_val = request.headers['x-auth-token']
       data = jwt.decode(tok_val, key, algorithms="HS256")
       id = request.json['id']
       bal = request.json['bal']
       bal = str(int(bal) + 30)
       data1 = {'id': id, 'bal': bal,'token-val':data}
       return (jsonify(data1))
    except:
       return "Invalid Token"


if __name__ == "__main__":
   app.run(host='0.0.0.0')
