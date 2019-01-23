import sys
reload(sys)
sys.setdefaultencoding('utf-8')

All = "X:"
Dailies = "Y:"
Post = "J:"
Reference = "L:\\References"
OutCompany = "X:\\%s\\Vender\\outgoing\\%s"

ffmpeg = r'W:\tronPipelineScript\tron2.0\ffmpeg\win\ffmpeg.exe'

user_name = 'root'
db_name = 'new_tron'
clip_table_name = 'oa_shot'

ip = '192.168.100.247'
passwd = 'king9188YJQ@'
to_php_url = 'http://192.168.100.247/clips/set_progress'
dai_url = 'http://192.168.100.247/callback/dailies'
common_url = 'http://192.168.100.247/python/renewScriptStatus'
