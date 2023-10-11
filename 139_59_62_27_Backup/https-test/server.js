const https = require('https');
const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');

const options = {
  ca: fs.readFileSync('cacert.pem'),
  cert: fs.readFileSync('server-crt.pem'),
  key: fs.readFileSync('server-key.pem')
};

const app = express();

app.use(bodyParser.json());

app.post('/data', (req, res) => {
  // Process the incoming data
  console.log(req.body);

  // Send a response
  res.status(200).send('Data received');
});

const server = https.createServer(options, app);

server.listen(8080, () => {
  console.log('Server listening on port 8080');
});
