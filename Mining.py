import os
import sys
from collections import Counter
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

from github import Github
from github import Auth

#zephyrproject-rtos/zephyr
target = sys.argv[1]
name = sys.argv[2]
output = name + "_data"

#auth
load_dotenv()
auth = Auth.Token(os.environ.get("GITHUB_TOKEN"))
g = Github(auth=auth)
repo = g.get_repo(str(target))

allPulls = repo.get_pulls(state="all", sort="created", direction="desc")
prData = []
totalLables = Counter()
count = 0

#write each pr dictonary to a list
for pr in allPulls:
    labels = Counter()

    for label in pr.labels:
        totalLables[label.name] += 1
        labels[label.name] += 1

    prInfo = {
        "id": pr.id,
        "title": pr.title,
        "author": pr.user.login if pr.user else "unknown",
        "created_at": pr.created_at,
        "closed_at": pr.closed_at,
        "labels": dict(labels),
        "body": pr.body
    }

    prData.append(prInfo)
    count += 1
    print(f"Processed {count} PRs")

topLabels = totalLables.most_common()
totalNumLabels = sum(totalLables.values())
labelData = []
for label, count in topLabels:
    percent = (count / totalNumLabels) * 100
    labelData.append({
        "label": label,
        "frequency": count,
        "percent": percent,
    })


dfLabels = pd.DataFrame(labelData)
dfAll = pd.DataFrame(prData)

#write global and top five data
dfLabels.to_csv("output_data/" + name + "_labels.csv", index=False)
dfAll.to_csv("output_data/" + output + ".csv", index=False)