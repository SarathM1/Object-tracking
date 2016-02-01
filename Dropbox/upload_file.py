import dropbox
import os,re

access_token = 'gMLhtGxtfGAAAAAAAAAACDBrTIGSl3zNtH_TiZVuIl-IdchTWT4HCPXo_Z1s6D3q'
client = dropbox.client.DropboxClient(access_token)
#print 'linked account: ', client.account_info()

while True:
    try:
        for f in os.listdir('../Detected/'):
            if re.search('.*\.jpg', f):
                fl = open('../Detected/'+f, 'rb')
                response = client.put_file('/'+ f, fl)
                print "uploaded file", response['path'].split('/')[1]
                os.remove('../Detected/'+f)
    except Exception, e:
        print e
