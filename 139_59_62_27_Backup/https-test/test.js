const https = require('https');
const fs = require('fs');

const options = {
	  cert: fs.readFileSync('server-crt.pem'),
	  key: fs.readFileSync('server-key.pem')
};

const server = https.createServer(options, (req, res) => {
	  // Request handler logic
	   res.writeHead(200, {'Content-Type': 'text/plain'});
	     res.end('Hello, World!\n');
	     });
	
	     server.listen(8080, () => {
	       console.log('Server listening on port 8080');
	       });
	       
