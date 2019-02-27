import os
for filename in os.listdir("F:\hiwi\\09september\\TextGrids_change_encoding_morphtag"):
    if filename.startswith("new_"):
        os.rename("F:\hiwi\\09september\\TextGrids_change_encoding_morphtag\\"+filename, "F:\hiwi\\09september\\TextGrids_change_encoding_morphtag\\"+"morphotagged_"+filename[4:])