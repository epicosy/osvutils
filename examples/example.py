from osvutils.core.loader import OSVDataLoader


loader = OSVDataLoader()

osv_is_cve_id_count = 0

loader(ecosystems=['GIT'])

for _, vals in loader:
    for _, record in vals.items():
        if record.is_cve_id():
            osv_is_cve_id_count += 1
        elif record.has_cve_id():
            osv_is_cve_id_count += 1

print(f"CVE IDs: {osv_is_cve_id_count}")
