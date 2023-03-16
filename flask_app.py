from flask import Flask, request, render_template, json
import math
import time
import threading

app = Flask(__name__)
client_info = {}    
@app.route('/')
def index():
    return render_template('index_calculator.html')

def logClientInformation(data,result,ip_addr):
    ts = time.time()
    if data.get('num2') is not None:
      information = [ts,data['num'],data['operator'],data['num2'], result,ip_addr]
    else:
      information = [ts,data['num'],data['operator'], result,ip_addr]
    global client_info
    if ip_addr in client_info:
      client_info[ip_addr].append(information)
    else:
      client_info[ip_addr]= [information]

@app.route('/calculate', methods=['POST'])
def calculate():
    ip_addr = request.remote_addr
    data = request.get_json()
    num2=0
    num = float(data['num'])
    if data.get('num2') is not None:
      num2 = float(data['num2']) 
    operator = data['operator']
    if client_info.get(ip_addr) is not None:
        response=[]
        if len(client_info[ip_addr]) > 4:
          response = app.response_class(
            response=json.dumps(client_info[ip_addr]),
            status=403,
            mimetype='application/json'
          ) 
          def lockUser(**kwargs):
            ip_address = kwargs.get('ip', {})
            starttime = time.time()
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
            client_info.pop(ip_address)
            print("Ip address removed",client_info)

          thread = threading.Thread(target=lockUser, kwargs={
                    'ip': ip_addr})
          thread.start()
          return response

    if operator =='+':
      result = num + num2
      response = app.response_class(
      response=json.dumps(result),
      status=200,
      mimetype='application/json'
      )
      logClientInformation(data,result,ip_addr)
      return response
    if operator =='-':
      result = num - num2
      response = app.response_class(
      response=json.dumps(result),
      status=200,
      mimetype='application/json'
      )
      logClientInformation(data,result,ip_addr)
      return response
    if operator =='*':
      result = num * num2
      response = app.response_class(
      response=json.dumps(result),
      status=200,
      mimetype='application/json'
      )
      logClientInformation(data,result,ip_addr)
      return response
    if operator =='/':
      result = num / num2
      response = app.response_class(
      response=json.dumps(result),
      status=200,
      mimetype='application/json'
      )
      logClientInformation(data,result,ip_addr)
      return response
    if operator =='^':
      result = num ** num2
      response = app.response_class(
      response=json.dumps(result),
      status=200,
      mimetype='application/json'
      )
      logClientInformation(data,result,ip_addr)
      return response
    if operator =='Sin':
      result = math.sin(math.radians(num))
      response = app.response_class(
      response=json.dumps(result),
      status=200,
      mimetype='application/json'
      )
      logClientInformation(data,result,ip_addr)
      return response
    if operator =='Cos':
      result = math.cos(num)
      response = app.response_class(
      response=json.dumps(result),
      status=200,
      mimetype='application/json'
      )
      logClientInformation(data,result,ip_addr)
      return response
    if operator == '%':
      result = num/100
      response = app.response_class(
      response=json.dumps(result),
      status=200,
      mimetype='application/json'
      )
      logClientInformation(data,result,ip_addr)
      return response
    else:
        return "Invalid Input"

if __name__ == '__main__':
    app.run(debug=True)
