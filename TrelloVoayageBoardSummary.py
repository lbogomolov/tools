import urllib.request
import json
import datetime
import sys

key = ""
token = ""
voyage_board = ""
url_template = "https://api.trello.com/1/boards/%s/checklists?key=%s&token=%s"
categories = ('dev_new', 'dev', 'fun', 'bug')

url = url_template % (voyage_board, key, token)
response = urllib.request.urlopen(url)
str_response = response.readall().decode('utf-8')
checklists = json.loads(str_response)

def print_items(ctgr, items):
    for item in	items:
        print(ctgr, item['state'], item['name'])
	
def process_items(items):
    done = 0
    for item in items:
        if item['state'] == 'complete':
            done += 1
    return done, len(items)

cnt = {}
for ctgr in categories:
    cnt[ctgr] = {'done': 0, 'total': 0}

for checklist in checklists:
    for ctgr in categories:
        if checklist['name'][:len(ctgr)].lower( ) == ctgr:
            if len(sys.argv) == 2:
                if sys.argv[1] == "--all":
                    print_items(ctgr, checklist['checkItems'])
            done,total = process_items(checklist['checkItems'])
            cnt[ctgr]['done'] += done
            cnt[ctgr]['total'] += total
            break
    if checklist['name'][:3].lower() not in categories:
        print(checklist['name'])
        done,total = process_items(checklist['checkItems'])
        print('Items', done, '/', total)           


date = datetime.datetime.now().strftime('%Y-%m-%d')
print(date,cnt['dev']['done'],cnt['dev']['total'],cnt['dev_new']['done'],cnt['dev_new']['total'],cnt['fun']['done'],cnt['fun']['total'],cnt['bug']['done'],cnt['bug']['total'], sep='\t')
