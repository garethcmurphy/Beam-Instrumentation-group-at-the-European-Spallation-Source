// read in js object 

var fs = require('fs');
var filename = "x.json";
var obj = JSON.parse(fs.readFileSync(filename, 'utf8'));

console.log(JSON.stringify(obj, null,2 ));

