import logging, time
log_path_server = '/Public/tronPipelineScript/tron2.0/log/'
logging.basicConfig(filename=log_path_server + time.strftime("%Y%m%d") + '.log', level=logging.INFO,
					format="%(asctime)s - %(levelname)s - %(message)s")
log_path_client = '/Public/tronPipelineScript/tron2.0/log/client_'+ time.strftime("%Y%m%d") + '.log'
outputpath = '/Tron/%s/Vender/outgoing/%s'

All = "/Tron"
Post = "/Post"
Reference = "/Library/References"

port = 29401

server_ip = "192.168.100.247"
server_port = 19950
