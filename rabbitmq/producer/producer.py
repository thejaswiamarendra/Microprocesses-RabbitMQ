from flask import Flask, render_template
import pika, os, logging, time
logging.basicConfig()

url = os.environ.get('CLOUDAMQP_URL','amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue = 'one')
channel.queue_declare(queue = 'two')
channel.queue_declare(queue = 'three')
channel.queue_declare(queue = 'four')


# for x in range(1000):
#     bodys = 'data ke' + str(x+1)
#     channel.basic_publish(exchange='', routing_key='pdfprocess', body = bodys)
#     print("[x] message sent to consumer = "+bodys)
#     a = x%100
#     if a==0:
#         time.sleep(2)
# connection.close()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/one', methods=['GET'])
def healthcheck():
    bodys = "Consumer 1"
    channel.basic_publish(exchange='', routing_key='one', body = bodys)
    print("[x] message sent to consumer = "+bodys)
    return "healthcheck"

@app.route('/two')
def insert():
    bodys = "Consumer 2"
    channel.basic_publish(exchange='', routing_key='two', body = bodys)
    return "insert"
    

@app.route('/three')
def delete():
    bodys = "Consumer 3"
    channel.basic_publish(exchange='', routing_key='three', body = bodys)

    return "delete"

@app.route('/four')
def read():
    bodys = "Consumer 4"
    channel.basic_publish(exchange='', routing_key='four', body = bodys)

    return "read"

if __name__ =='__main__':
    app.run(debug = True)