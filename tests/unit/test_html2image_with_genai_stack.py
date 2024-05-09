import aws_cdk as core
import aws_cdk.assertions as assertions

from html2image_with_genai.html2image_with_genai_stack import Html2ImageWithGenaiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in html2image_with_genai/html2image_with_genai_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Html2ImageWithGenaiStack(app, "html2image-with-genai")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
