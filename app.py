#!/usr/bin/env python3
import os

import aws_cdk as cdk

from html2image_with_genai.html2image_with_genai_stack import Html2ImageWithGenaiStack


app = cdk.App()
Html2ImageWithGenaiStack(app, "Html2ImageWithGenaiStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

 

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */


    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
