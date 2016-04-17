def message(username,message):
	return requests.post(
		'https://api.kik.com/v1/message',
		auth=('shaanbot', 'a024ef5e-627c-4166-9fb1-2093cba4f544'),
		headers={
			'Content-Type': 'application/json'
		},
		data=json.dumps({
			'messages': [
				{
					'body':message, 
					'to': username, 
					'type': 'text'
				}
			]
		})
	)