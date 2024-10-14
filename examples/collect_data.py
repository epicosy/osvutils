
from osvutils.core.collector import OSVDataCollector

collector = OSVDataCollector(verbose=True)
count = collector(['Wolfi'])

print(f"Total records collected: {count}")
