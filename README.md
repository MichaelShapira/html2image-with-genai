
# AWS CDK project to validate HTML form input by converting it to an image and analyzing the image with Generative AI

The repository contains a ready-to-deploy demo of an HTML page with a simple form. The input of the form is being validated by Amazon Bedrock Generative AI models after it is converted to **image**

![image](https://github.com/MichaelShapira/html2image-with-genai/assets/135519473/b682736e-6fe8-497a-a438-ff3e6c30137f)

# Why is it relevant?

1. Organizations use SaaS web solutions, or off-the-shelf, complex tools based on HTML with limited ability for customization. 

   They need the ability to define custom rules for specific fields, which is not doable with those tools. However, you can customize the behavior of the buttons (like Submit button in this example).

2. Organizations have foolproof control over the web application, but the number of fields that you need to customize is not negligible and is hard to manage. In addition, the cycle of defining the validation rule, approving it, and implementing it is very time-consuming and, in most cases, requires some technical background.

3. Some fields just cannot be validated by using standard tools like regular expressions. For example, on the print screen above, the organization wants to force the person who fills out the remarks to summarize the interaction with the customer. There is no way to validate it without generative AI.

# Architecture
![image](https://github.com/MichaelShapira/html2image-with-genai/assets/135519473/9193cbe1-a751-4411-a426-145f621c1965)

We have one lambda function to handle all the logic. End users access the Lambda with a GET request that returns the HTML page (the same as you see above).
The user can modify the distractions or the default one (that validates the referenced number). Once the user clicks the submit button, the form is converted to an image and sent as a POST request to the same Lambda. Lambda passes the image and distractions to the model in Amazon Bedrock and returns the relevant result.

# Customization

You can control which model to use in the Lambda environment settings. The default value is Claude 3 Sonet. 

![image](https://github.com/MichaelShapira/html2image-with-genai/assets/135519473/b7396f14-8e5d-4c3a-ab4a-75abb6e4f43e)

# Deployment 

You need to install AWS CDK following this instructions https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html.
Checout the repository and run from the root folder
```
cdk deploy
```
You should define AWS credentials with relevant permissions for this command to work.



