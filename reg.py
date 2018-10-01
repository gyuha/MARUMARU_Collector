#!/usr/bin/env python
import re

file = "자칭 F랭크인 오빠가 게임으로 평가되는 학원의 정점에 군림한다고 하던데요? 11화"
print(re.sub(r'(\d+)화', lambda m : m.group(0).zfill(4), file))