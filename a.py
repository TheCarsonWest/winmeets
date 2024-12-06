import hytek
import json
file = hytek.Hy3File("file.hy3")
file.read()


with open('result.json', 'w') as fp:
    json.dump(file.to_json(), fp)
