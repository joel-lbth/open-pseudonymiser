import os
from pathlib import Path
# pip install pyjnius
import jnius_config

def set_java_lib(jar_path):
  """set location of OpenPseudonymiserCryptoLib.jar 
  note - you will need to have built (or downloaded) it first

  Args:
      jar_path (string): path to lib jar

  Returns:
      string: location
  """  
  jnius_config.set_classpath(".", jar_path)
  return jar_path

def import_java_crypto():
  """import the crypto lib from java
  """
  from jnius import autoclass
  Crypto = autoclass("OpenPseudonymiser.Crypto")
  crypto = Crypto()
  return crypto

def set_encrypted_salt(salt_path, crypto):
  from jnius import autoclass
  File = autoclass("java.io.File")
  file = File(salt_path)
  crypto.SetEncryptedSalt(file)
  return crypto

def test_crypto(crypto):
  from jnius import autoclass
  Map = autoclass("java.util.Map")
  TreeMap = autoclass("java.util.TreeMap")
  treeMap = TreeMap()
  treeMap.put("DOB", "29.11.1973")
  treeMap.put("NHSNumber", "943 476 5919")

  # test encryption matches expected outcome
  try:
      assert "ED72F814B7905F3D3958749FA90FE657C101EC657402783DB68CBE3513E76087" == crypto.GetDigest(treeMap)
      print("test passed", crypto.GetDigest(treeMap))
  except(Exception):
      print(Exception)
      print("test failed")

# run from shell with `python app.py`
if __name__ == "__main__":

  # set crypto lib
  # this is probably better as it means relative to the file
  # sometimes however __file__ disappears, such as in interactive python
  jar_path = os.path.join(Path(__file__).parent.absolute(), "dist", "*")
  # this works, but only if the file is triggered from the right location
  # jar_path = os.'path.join(Path(os.getcwd()).absolute(), "dist", "*")

  set_java_lib(jar_path)
  print(jar_path)
    
  # get crypto class
  crypto = import_java_crypto()  

  # set salt
  salt_path = "./mackerel.EncryptedSalt"
  set_encrypted_salt(salt_path, crypto)

  # some test data
  test_crypto(crypto)
