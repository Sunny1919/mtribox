# @title **[2]** Start server
# @markdown This cell will start the server, the first time that you run it will download the models, so it can take a while (2~4 minutes)

# @markdown If you want to use ngrok, please input your token in the option section below. If you encounter a 403 error with the colab proxy, using ngrok can sometimes help to work around it.
# @markdown https://dashboard.ngrok.com/


# @markdown ### Options:
ClearConsole = False  # @param {type:"boolean"}
Play_Notification = True  # @param {type:"boolean"}
NgrokToken = "2lim4sRTwmRvMsMXRmtaqj4Igol_DN1o9fRyFNSX3gZn3bdV"  # @param {type:"string"}

PORT=8003
NGROK_URL_FILE = "ngrok_url.txt"

LOG_FILE = f"/content/LOG_FILE_{PORT}.log"

from IPython.display import Audio, display
def play_notification_sound(url):
    display(Audio(url=url, autoplay=True))

from google.colab.output import eval_js




if mode == "elf":
  # !LD_LIBRARY_PATH=/usr/lib64-nvidia:/usr/lib/x86_64-linux-gnu ./vcclient_latest_for_colab cui --port {PORT} --no_cui true &
  if NgrokToken =="":
    get_ipython().system_raw(f'LD_LIBRARY_PATH=/usr/lib64-nvidia:/usr/lib/x86_64-linux-gnu ./vcclient_latest_for_colab cui --port {PORT} --no_cui true --https False >{LOG_FILE} 2>&1 &')
  else:
    get_ipython().system_raw(f'LD_LIBRARY_PATH=/usr/lib64-nvidia:/usr/lib/x86_64-linux-gnu ./vcclient_latest_for_colab cui --port {PORT} --no_cui true --https False --ngrok_token {NgrokToken} --ngrok_proxy_url_file {NGROK_URL_FILE} >{LOG_FILE} 2>&1 &')
elif mode == "zip":
  !LD_LIBRARY_PATH=/usr/lib64-nvidia:/usr/lib/x86_64-linux-gnu ./main cui --port {PORT} --no_cui true &


import socket
def wait_for_server():
  elapsed_time = 0
  start_time = time.time()


  while True:
      time.sleep(1)
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      result = sock.connect_ex(('127.0.0.1', PORT))
      if result == 0:
          break
      sock.close()
      # 時刻を出力
      current_time = time.time()
      elapsed_time = int(current_time - start_time)
      clear_output(wait=True)
      print(f"Waiting for server... elapsed: {elapsed_time}sec")
      try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()[-5:]
            for line in lines:
                print(line.strip())
      except:
        pass

  if ClearConsole:
      clear_output()
  print("--------- SERVER READY! ---------")
  print(f"Your server is available. elapsed: {elapsed_time}sec")
  proxy = eval_js( "google.colab.kernel.proxyPort(" + str(PORT) + ")" )
  print(f"colab proxy: {proxy}")
  if NgrokToken != "":
    with open(NGROK_URL_FILE, "r") as f:
      ngrok_url = f.read().strip()
    print(f"Ngrok URL: {ngrok_url}")
  print("---------------------------------")
  if Play_Notification==True:
    play_notification_sound('https://huggingface.co/wok000/voices/resolve/main/vcclient001_vctk229_gpt-sovits_vcclient-ready.wav')
wait_for_server()
