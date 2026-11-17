import sources_133 as source
from common_133 import HERE

source.OUT = HERE / "source-002"
source.CHARS = "琴鉛滝"
source.SUPPORTS = {c: source.SUPPORTS[c] for c in source.CHARS}
source.CURATED = {c: source.CURATED[c] for c in source.CHARS}
source.READINGS = {c: source.READINGS[c] for c in source.CHARS}
source.CONTAINS = [*source.CHARS, "瀧"]

if __name__ == "__main__":
    source.main()
