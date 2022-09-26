import subprocess
process=subprocess.Popen(['sh', './secret.sh'],stdout=subprocess.PIPE)
stdout = process.communicate()[0].decode('utf8')

