
from osvutils.core.collector import OSVDataCollector

collector = OSVDataCollector(verbose=True)
count = collector(['CRAN'])

print(f"Total records collected: {count}")
