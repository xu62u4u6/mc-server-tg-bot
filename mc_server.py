import os
import subprocess
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class Server:
    def __init__(self):
        
        self.run_cmd = f'java -jar -Xms{config["minecraft"]["xms"]}G -Xmx{config["minecraft"]["xmx"]}G server.jar --nogui'
        self.status = "stop"
        self.pids = None
        self.process = None
        self.ip = config["minecraft"]["server-ip"]
        self.dir = config["minecraft"]["server-dir"]
        self.players = set()
        os.chdir(self.dir)
        
        
    def run(self):
        if self.status == "stop":
            self.status = "running"
            self.process = subprocess.Popen(self.run_cmd, 
                                            stdout=open('log.txt', 'w'), 
                                            stderr=subprocess.STDOUT, 
                                            shell=True)
            return f"伺服器啟動中，請稍候約20秒再進入遊戲。"
        
        else:
            return "伺服器已經在運行了"
     
     
    def stop(self):
        if self.status == "running":
            self.status = "stop"
            subprocess.Popen(f'pgrep -f "{self.run_cmd}" | xargs kill', shell=True)
            return "伺服器停止中，請稍候。"
        else:
            self.status = "stop"
            return "伺服器並未運行"
        
        
    def check_status(self):
        self.check_players()
        return f"""伺服器狀態:{self.status}\n伺服器位址:{self.ip}\n目前玩家:{", ".join(self.players)}\n"""
    
    
    def check_players(self):
        with open("log.txt") as f:
            for line in f.readlines(): 
                if "joined the game" in line:
                    player = line.split("[Server thread/INFO]: ")[1].replace(" joined the game", "")
                    self.players.add(player)
                    