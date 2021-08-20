# coding = utf8
import os, signal
os.path.abspath(".")
import subprocess
from multiprocessing import Process, Pipe
from time import sleep
import sys
import telnetlib

class SDK_test:
  
  def __init__(self, camera_1_ip="192.168.0.200", camera_2_ip=""):
    self.camera_1 = camera_1_ip
    self.camera_2 = camera_2_ip
  
  def run_terminal_ip(self, terminal_no=1,child_conn=""):
    process = subprocess.Popen("./svcam3dn_sim_tm {} {} >>./log/device_terminal_{}.log".format(self.camera_1, self.camera_2, terminal_no),shell = True)
    print("Current process {} id:{}".format(terminal_no, process.pid))
    child_conn.send(process.pid)
    child_conn.close()

  def case1_sdk_openclose(self, test_count=50):
    # Be care about Pipe() on and Process create pid will gap 2
    # try except for error to adjust this problem between pipe connection and Process pid
    # take care two process need gap some time in case the pid will not mixture
    parent_conn2, child_conn2 = Pipe()
    terminal_1_process = Process(target=self.run_terminal_ip, args=(1,child_conn2,))
    terminal_2_process = Process(target=self.run_terminal_ip, args=(2,child_conn2,))
    terminal_1_process.start()
    sleep(3)
    terminal_2_process.start()
    sleep(10)
    pid1 = parent_conn2.recv()
    pid2 = parent_conn2.recv()
    self.kill_process(pid2)
    terminal_2_process.terminate()
    for i in range(50):
      parent_conn3, child_conn3 = Pipe()
      sleep(1)
      p2 = Process(target=self.run_terminal_ip, args=("2_"+ str(i + 1),child_conn3,))
      p2.start()
      sleep(5)
      try:
        pid3 = parent_conn3.recv()
        self.kill_process(pid3)
        p2.terminate()
        print("Cycyle {}".format(i + 1))
      except ProcessLookupError as ex:
        print("cycle queue Happened pid abnormal so reduce it!")
        try:
          self.kill_process(pid3 + 1)
          p2.terminate()
        except ProcessLookupError as ex:
          continue
    try:
      # the first process if you need last close it, you should count -1 in it's pid
      self.kill_process(pid1 - 1)
      terminal_1_process.terminate()
    except ProcessLookupError as ex:
      print("Happened pid abnormal so reduce it!")
      try:
        self.kill_process(pid1 + 1)
        terminal_1_process.terminate()
      except ProcessLookupError as ex:
        print("Finish reduce!")
    print("Test done")

  def open_a_process(self):
    process = subprocess.Popen("./svcam3dn_sim_tm {} {}".format(self.camera_1, self.camera_2),shell = True)
    
  def kill_process(self, pid):
    os.kill(pid + 2, signal.SIGKILL)
    print("killed pid {}".format(pid + 2))
    
  
if __name__ == "__main__":
  sdk_test = SDK_test("192.168.0.200","192.168.0.201")
  sdk_test.case1_sdk_openclose()
  os._exit(0)
