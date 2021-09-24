import sys
import zipfile
import time
def main():
    otazip = zipfile.ZipFile('update.zip', 'r')
    payload_info = otazip.getinfo('payload.bin')
    payload_offset = payload_info.header_offset + len(payload_info.FileHeader())
    payload_size = payload_info.file_size
    payload_location = '/data/ota_package/update.zip'
    headers = otazip.read('payload_properties.txt').decode('utf-8')
    print (('update_engine_client --update --follow --payload=file://{payload_location}'
    ' --offset={payload_offset} --size={payload_size}'
    ' --headers="{headers}"').format(**locals()))
    return 0
	
if __name__ == '__main__':
    sys.exit(main())
