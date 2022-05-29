import requests , subprocess 
from tqdm import tqdm

def Ping(host:str):
    command = ['ping','-n','2',host,'-w','1']
    return subprocess.call(command,stdout=subprocess.DEVNULL) == 0

def Gost(host_port:str,cert:str,iat_mode:str):
    command = ['.\gost.exe','-L',':8888','-F','obfs4://'+host_port+'/?'+cert+'&'+iat_mode]
    p = subprocess.Popen(command,shell=False,stdout=subprocess.DEVNULL
        ,stderr=subprocess.DEVNULL)
    return p

for i in tqdm(requests.get("https://raw.githubusercontent.com/scriptzteam/Tor-Bridges-Collector/main/bridges-obfs4").text.split("\n")):
    i = i.split(" ")

    # Step1: Ping The Server
    if Ping(i[1].split(":")[0]) == False: continue

    # Save Ping
    open("./ping","a",encoding="utf-8").write(str(i)+"\n")
    # Step2: Transport The Traffic
    try:
        p = Gost(i[1],i[3].replace("+","%2B"),i[4])
        t = requests.get("https://ip.sb",proxies={"http":"socks5://127.0.0.1:8888","https":"socks5://127.0.0.1:8888"},timeout=2)
        assert t.status_code == 200 , "Error: Transport Failed"
    except Exception as E: pass
    else:
        open("./ok.txt","a",encoding="utf-8").write(str(i)+"\n")
    finally:
        p.kill()
