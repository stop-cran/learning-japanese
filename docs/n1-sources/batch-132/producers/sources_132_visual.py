import sources_132 as source
from common_132 import HERE

source.OUT = HERE / "source-003"
source.CHARS = "墓"
source.CONTAINS = ["墓"]
source.READINGS = {"墓": source.READINGS["墓"]}
source.CURATED = set("暮募川")

if __name__ == "__main__":
    source.main()
