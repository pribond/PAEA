# python server to handle POST request
import sys, json, hashlib
from flask import Flask, request
from orm import *

app = Flask(__name__)
app.debug = False

@app.route('/api', methods=['POST', 'GET'])
def post_signature():
	if request.method == 'POST':
		data = json.loads(request.data)
		genes = data['genes']
		coefs = data['coefs']
		desc = data['desc']
		hash_str = hashlib.md5(str(data)).hexdigest()
		## save into the db
		add_associations(hash_str, genes, coefs, session, desc=desc)
		return hash_str

	elif request.method == 'GET':
		hash_str = request.args.get('id', '')
		try:
			genes, coefs, desc = get_associations(hash_str, session)
			data = {'genes':genes, 'coefs':coefs, 'desc':desc}
			return json.dumps(data)
		except:
			return ('', 400, '')

if __name__ == '__main__':
	if len(sys.argv) > 1:
		port = int(sys.argv[1])
	else:
		port = 5050
	if len(sys.argv) > 2:
		host = sys.argv[2]
	else:
		host = '127.0.0.1'
	app.run(host=host, port=port)