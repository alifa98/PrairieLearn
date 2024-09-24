import csv
import json
from os import path

with open("./sharing_sets.csv", mode="r") as sharingSetsFile:
    csv_dict_reader = csv.DictReader(sharingSetsFile)

    with open("infoCourse.json", mode="r+") as infoCourseFile:
        infoCourse = json.loads(infoCourseFile.read())
        if "sharingSets" not in infoCourse:
            infoCourse["sharingSets"] = []

        existingSets = set(ss["name"] for ss in infoCourse["sharingSets"])
        for row in csv_dict_reader:
            sharingSet = row["name"]
            if sharingSet not in existingSets:
                infoCourse["sharingSets"].append(
                    {"name": sharingSet, "description": ""}
                )

        infoCourseFile.seek(0)
        infoCourseFile.truncate()
        infoCourseFile.write(json.dumps(infoCourse, indent="  "))



with open("./question_sharing_info.csv", mode="r") as sharingInfoFile:
    csv_dict_reader = csv.DictReader(sharingInfoFile)

    for row in csv_dict_reader:
        qid = row['qid']
        question_path = path.join('questions', qid, 'info.json')
        with open(question_path, mode="r+") as infoFile:
            infoQuestion = json.loads(infoFile.read())

            if row['shared_publicly'] == 't':
                infoQuestion['sharedPublicly'] = True

            if row['sharing_sets'] != '':
                if "sharingSets" not in infoQuestion:
                    infoQuestion["sharingSets"] = []

                sharingSets = json.loads(row['sharing_sets'])
                for sharingSet in sharingSets:
                    if sharingSet not in infoQuestion['sharingSets']:
                        infoQuestion["sharingSets"].append(sharingSet)

            infoFile.seek(0)
            infoFile.truncate()
            infoFile.write(json.dumps(infoQuestion, indent="  "))
