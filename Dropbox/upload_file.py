import dropbox

access_token = 'gMLhtGxtfGAAAAAAAAAACDBrTIGSl3zNtH_TiZVuIl-IdchTWT4HCPXo_Z1s6D3q'
client = dropbox.client.DropboxClient(access_token)
#print 'linked account: ', client.account_info()

f = open('../Detected10.jpg', 'rb')
response = client.put_file('/Detected10.jpg', f)
print "uploaded:", response