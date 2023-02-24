from flask import Flask, request, Response
import configparser

from mc_server import Server
from tg_command import TG_Bot


# read config
config = configparser.ConfigParser()
config.read('config.ini')
token = config["telegram"]["token"]


# init instance
app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_msg():
    try:
        msg = request.get_json()

    except:
        return "error"#Response('ok', status=200)
    
    # check msg received time
    if msg["message"]["date"] > bot.init_time:
        date, chat_id, nsername, text = bot.parse_massage(msg)
        
        # pass 
        if text in ["/run", "/status"]:
            if text == "/status":
                res = server.check_status()
            elif text == "/run":
                res = server.run()
                
            bot.send_message(chat_id, res)
            
    return Response('ok', status=200)
     
if __name__ == '__main__':
    server = Server()
    bot = TG_Bot()
    app.run(port=5001)
    server.stop()