import re

text = "********************************************************kf'k'k'k'k*****k*k'k*k*k*k**1:*************************kk'k'kk*******k******k**************"

regex = '\*\*\*\*'

res = re.search(regex, text)

print(res.group())