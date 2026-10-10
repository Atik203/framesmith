import { config } from "@remotion/eslint-config-flat";
import { createRequire } from 'module';

var require = createRequire(import.meta.url);
var module = { exports: {} };

export default config;
