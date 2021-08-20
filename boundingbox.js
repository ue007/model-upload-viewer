var gltfBoundingBox = require('gltf-bounding-box');
let fs = require('fs');
const path = require('path');

const model = JSON.parse(fs.readFileSync('./out/convertor/ReductionOutput.gltf', 'utf8'));

const boundings = gltfBoundingBox.computeBoundings(model);
// console.log(boundings);
