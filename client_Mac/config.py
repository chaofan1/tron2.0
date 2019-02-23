import sys
reload(sys)
sys.setdefaultencoding('utf-8')

All = "/Volumes/All"
Dailies = "/Volumes/Dailies"
Post = "/Volumes/Post"
Reference = "/Volumes/library/References"
OutCompany = "/Volumes/All/%s/Vender/outgoing/%s"

ffmpeg = '/Volumes/Public/tronPipelineScript/tron2.0/ffmpeg/mac/ffmpeg'

user_name = 'root'
db_name = 'new_tron'
clip_table_name = 'oa_shot'

ip = '192.168.100.247'
passwd = 'king9188YJQ@'
to_php_url = 'http://192.168.100.247/clips/set_progress'
dai_url = 'http://192.168.100.247/callback/dailies'
common_url = 'http://192.168.100.247/python/renewScriptStatus'

port = 29401
