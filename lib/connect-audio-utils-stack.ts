import fs = require('fs')
import cdk = require('@aws-cdk/core');
import lambda = require('@aws-cdk/aws-lambda');
import { Duration } from '@aws-cdk/core';

export class ConnectAudioUtilsStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const layer = new lambda.LayerVersion(this, 'connect-audio-utils', {
      code: lambda.Code.fromAsset('resources/connect-audio-utils-layer/layer.zip'),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_8]
    });

    const redact_audio = new lambda.Function(this, 'redact_audio', {
      code: lambda.Code.fromAsset('resources/functions/'),
      handler: 'redact_audio.lambda_handler',
      runtime: lambda.Runtime.PYTHON_3_8,
      layers: [layer],
      memorySize: 1792,
      timeout: Duration.minutes(5),
      tracing: lambda.Tracing.ACTIVE
    });

    const overlay_audio = new lambda.Function(this, 'overlay_audio', {
      code: lambda.Code.fromAsset('resources/functions/'),
      handler: 'overlay_audio.lambda_handler',
      runtime: lambda.Runtime.PYTHON_3_8,
      layers: [layer],
      memorySize: 1792,
      timeout: Duration.minutes(5),
      tracing: lambda.Tracing.ACTIVE
    });
  }
}
