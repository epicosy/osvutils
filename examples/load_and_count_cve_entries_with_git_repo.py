from osvutils.core.loader import OSVDataLoader


loader = OSVDataLoader()

loader()

cve_ids_osv = loader.get_osv_with_cve_ids(has_git_repo=True)

print(f"{len(cve_ids_osv)} CVE IDs with Git repository in {len(loader)} records")
