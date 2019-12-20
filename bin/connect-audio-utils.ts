#!/usr/bin/env node
import 'source-map-support/register';
import cdk = require('@aws-cdk/core');
import { ConnectAudioUtilsStack } from '../lib/connect-audio-utils-stack';

const app = new cdk.App();
new ConnectAudioUtilsStack(app, 'ConnectAudioUtilsStack');
