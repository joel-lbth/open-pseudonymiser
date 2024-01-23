# run from shell with `python app.py`
if __name__ == "__main__":

    import os
    from pathlib import Path
    # pip install pyjnius
    import jnius_config

    file_path = os.path.join(
        Path(__file__).parent.absolute(), "java-lib", "*"
    )
    jnius_config.set_classpath(".", file_path)
    from jnius import autoclass
    print(file_path)

    # import java code
    Crypto = autoclass("OpenPseudonymiser.Crypto")
    crypto = Crypto()

    # read double encrypted file in as salt
    file_path = "./mackerel.EncryptedSalt"
    File = autoclass("java.io.File")
    file = File(file_path)
    crypto.SetEncryptedSalt(file)

    # create some test data
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
