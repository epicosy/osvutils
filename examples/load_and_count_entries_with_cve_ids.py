from osvutils.core.loader import OSVDataLoader


loader = OSVDataLoader()

loader(ecosystems=['GIT'])

cve_ids_osv = loader.get_osv_with_cve_ids()

print(f"CVE IDs: {len(cve_ids_osv)}")
