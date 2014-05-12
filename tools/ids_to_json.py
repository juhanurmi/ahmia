import re

#test is url correct onion url
#Must be like http://3g2upl4pq6kufc4m.onion/
def validate_onion_URL( url ):
    if len(url) != 30:
        return False
    if url[0:7] != 'http://':
        return False
    if url[-7:] != '.onion/':
        return False
    if not re.match( "[a-z2-7]{16}", url[7:-7] ):
        return False
    return True

file = "/home/juha/new_onions_uniq.txt"

domains = open( file, "r" )
for domain in domains:
	url = 'http://'+domain.rstrip('\n')+'.onion/'
	if validate_onion_URL(url):
		print('{"url":"'+url+'"}')
