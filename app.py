# run from shell with `python app.py`
if __name__ == "__main__":

    import os
    from pathlib import Path
    # pip install pyjnius
    import jnius_config

    # note - OpenPseudonymiserCryptoLib.jar should be in the dist dir of the project
    # note - you will need to have built (or downloaded) it there
    file_path = os.path.join(
        Path(__file__).parent.absolute(), "dist", "*"
    )
    jnius_config.set_classpath(".", file_path)
    from jnius import autoclass
    print(file_path)

    # import java code
    Crypto = autoclass("OpenPseudonymiser.Crypto")
    crypto = Crypto()

    # encrypt salt for extra security
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
