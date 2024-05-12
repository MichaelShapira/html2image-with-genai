import json
import base64
import boto3
from urllib.parse import unquote
import os

def run_multi_modal_prompt(bedrock_runtime, model_id, messages, max_tokens):
    """
    Invokes a model with a multimodal prompt.
    Args:
        bedrock_runtime: The Amazon Bedrock boto3 client.
        model_id (str): The model ID to use.
        messages (JSON) : The messages to send to the model.
        max_tokens (int) : The maximum  number of tokens to generate.
    Returns:
        None.
    """



    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages
        }
    )

    response = bedrock_runtime.invoke_model(
        body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())

    return response_body


def lambda_handler(event, context):
    # Get the HTTP method and path from the event
    http_method = event['httpMethod']
    path = event['path']

    # Get the query string parameters
    query_params = event.get('queryStringParameters', {})

    # Get the body of the request
    body = event.get('body')
    if body:
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass

    # Define the response based on the HTTP method and path
    if http_method == 'GET':
        # Return the HTML form
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Interaction Notes</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/cerulean/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container my-5">
        <h1 class="text-center mb-4">Customer Interaction Notes</h1>
        <form id="notesForm">
            <div class="form-group">
                <label for="customerName">Customer Name</label>
                <input type="text" class="form-control" id="customerName" placeholder="Enter customer name">
            </div>
            <div class="form-group">
                <label for="orderNumber">Order Number</label>
                <input type="text" class="form-control" id="orderNumber" placeholder="Enter order number">
            </div>
            <div class="form-group">
                <label>Referenced Items</label>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Contact</th>
                            <th>Company Name</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><input type="text" class="form-control" value="Alice"></td>
                            <td><input type="text" class="form-control" value="alice@gmail.com"></td>
                            <td><input type="text" class="form-control" value="Microhard"></td>
                        </tr>
                        <tr>
                            <td><input type="text" class="form-control" value="Bob"></td>
                            <td><input type="text" class="form-control" value="bob@gmail.com"></td>
                            <td><input type="text" class="form-control" value="Abibas"></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="form-group">
                <label for="remarks">Remarks</label>
                <textarea class="form-control" id="remarks" rows="5">Referenced Item  = #657567567</textarea>
            </div>
            
            
        </form>
         <button type="button" class="btn btn-primary" onclick="sendFormData()">Submit</button>
         <button type="button" class="btn btn-primary" onclick="downloadImage()">Download Image</button>
        <div class="form-group mt-3">
                <label for="instructions">Instructions</label>
                <textarea class="form-control" id="instructions" name="instructions" rows="7" placeholder="Enter instructions here">
The following image represents the customer interaction form.
The fields from top to bottom should be: customer name, order number, reference items, and remarks.
Referenced Items is an editable table with 3 columns: Name, Contact, and Company Name.
Remarks is a text area with 5 rows.
The comment field should include a reference to the item. The form of the text should be "Referenced Item = #4456." The number after the # sign may vary. The case of the text may be lower or upper case.
If you don't identify this information in the picture, return the text "Referenced Item was not found." If you find this text, return "Referenced Item was found."

                </textarea>
            </div>
         <div class="card border-primary w-100" style="width: 18rem;">
              <div class="card-body">
                <h5 class="card-title">Response</h5>
                <div id="responseDiv"></div>
              </div>
         </div>
    </div>

    <script>
        function downloadImage()
        {
            html2canvas(document.querySelector("#notesForm")).then(canvas => {
                    let imgData = canvas.toDataURL('image/png');
                    const link = document.createElement('a');
                    link.download = 'myFormAsImage.png';
                    link.href = imgData
                    link.click();
                });
        }

        function sendFormData() {
            html2canvas(document.querySelector("#notesForm")).then(canvas => {
                let imgData = canvas.toDataURL('image/png');
                let instructions = document.getElementById("instructions").value;
                sendImageData(imgData,instructions);
            });
        }

        function sendImageData(imgData,instructions) {
            let xhr = new XMLHttpRequest();
            xhr.open('POST', '/demo/GenAIHtmlToImage');
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        displayResponse(xhr.responseText);
                    } else {
                        displayResponse('Error sending image data');
                    }
                }
            };
          let data = {
            imgData: imgData,
            instructions: instructions
          };

            xhr.send(JSON.stringify(data));
            
        }

        function displayResponse(response) {
            let responseDiv = document.getElementById('responseDiv');
            responseDiv.innerHTML = `<p class="card-text">${response}</p>`;
        }
    </script>
</body>
</html>
"""
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': html_content,
            'isBase64Encoded': False
        }

    elif http_method == 'POST':
        # Process the form submission
        base64_data = ""
       
        
        request_data = json.loads(event['body'])
        image_data = request_data['imgData']
       
        input_text = request_data['instructions']
       
        if image_data:
            # Decode the base64 image data
            try:
                #image_binary = unquote(base64.b64decode(image_data))
                
                comma_index = image_data.find(",")
                
                # Substring the string starting from the index after the comma
                base64_data = image_data[comma_index + 1:]
               
                # Do something with the image binary data (e.g., save it to a file or upload it to S3)
                response_message = f"Received image data with length {len(image_binary)} bytes"
            except Exception as e:
                response_message = f"Error decoding image data: {str(e)}"
        else:
            response_message = "No image data received"
        
        try:
            
            bedrock_runtime = boto3.client(service_name='bedrock-runtime')
            model_id = os.environ.get('MODEL_ID')
            #model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
            #model_id='anthropic.claude-3-haiku-20240307-v1:0'
            max_tokens = 1000
            
            message = {"role": "user",
                 "content": [
                    {"type": "image", "source": {"type": "base64",
                        "media_type": "image/png", "data": base64_data}},
                    {"type": "text", "text": input_text}
                    ]}
    
        
            messages = [message]
    
            gen_response_message = run_multi_modal_prompt(
                bedrock_runtime, model_id, messages, max_tokens)

            response_message = json.dumps(gen_response_message['content'][0]['text'], indent=4)
        except ClientError as err:
            response_message = err.response["Error"]["Message"]
            print(err)
            

        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': response_message,
            'isBase64Encoded': False
        }

    else:
        response = {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'Not found',
            'isBase64Encoded': False
        }

    return response