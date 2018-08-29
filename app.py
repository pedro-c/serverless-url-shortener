from chalice import Chalice, Response
import shortid
import boto3
import os

dynamodb = boto3.resource('dynamodb')
sid = shortid.ShortId()
app = Chalice(app_name=os.environ['DB_NAME'])

@app.route('/{code}', cors = True)
def get_original_url(code):
    table = dynamodb.Table(os.environ['DB_NAME'])
    try:
        response = table.get_item(
            Key={
                'code': code
            }
        )
    except Exception as e:
        return Response(
            body='',
            status_code=302,
            headers={
                'Location': os.environ['BASE_URL'] + '404'
            }
        )
    else:
        return Response(
            body='',
            status_code=302,
            headers={
                'Location': response['Item']['originalUrl']
            }
        )

@app.route('/shorten', cors = True, methods=['POST'])
def create_short_url():
    table = dynamodb.Table(os.environ['DB_NAME'])
    params = app.current_request.json_body
    try:
        response = table.get_item(
            Key={
                'code': params['code']
            }
        )
        return {
                'Error': 'Code is already in use to redirect to: ' + response['Item']['originalUrl'],
                'url': response['Item']['originalUrl']
            }
    except Exception as e:
        try:
            code = params['code']
        except Exception as e:
            code = sid.generate()

        try:            
            response = table.put_item(
                Item={
                        'code': code,
                        'originalUrl': params['originalUrl']
                    }
            )
            return{
                    'url': os.environ['BASE_URL'] + code,
                    'originalUrl': params['originalUrl']
                }
        except Exception as e:
            return(e)
