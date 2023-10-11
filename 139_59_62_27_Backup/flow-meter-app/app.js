const express = require('express')
const mqtt = require('mqtt')
const date = require('date-and-time')
const app = express()

// Connect to the MQTT broker
const client = mqtt.connect('mqtt://localhost:1883')

// Subscribe to the flow meter topic
client.subscribe('flow-meter')

// Store the latest flow meter reading
let latestReading = null
const hexToDecimal = hex => parseInt(hex, 16);
// Handle incoming MQTT messages
client.on('message', function (topic, message) {
	console.log("Data received on topic, verifying topic");
  if (topic === 'flow-meter') {
    // Parse the message payload as a JSON object
    	console.log("Data received on flow-meter topic = " + message.toString());
	var data = message.toString();
    	var datasplit = data.split(",");
    	console.log("TimeStamp = " + datasplit[2]);
	console.log("Flow Data = " + datasplit[15]);
	var flowrate = datasplit[15].split("-");
    console.log("Flow Data in HEX= " + flowrate[2]);
    //const reading = JSON.parse(message.toString())
	const flow_rate = hexToDecimal(flowrate[2].toString());
	console.log("Flow Data in Dec= " + flow_rate);
	const now  =  new Date();
	const datetime = date.format(now,'YYYY-MM-DD HH:mm:ss');
	const reading = {
    //timestamp: datetime,
    timestamp: datasplit[2],
    flowRate: flow_rate
  }

  client.publish('flow-meter-data', JSON.stringify(reading))
    // Update the latest flow meter reading
    //latestReading.timestamp =  datasplit[2].toString();
    //latestReading.flowRate = flow_rate;
    //latestReading.totalVolume = 50;
	//const reading = JSON.parse(message.toString())
	//console.log("Data received on flow-meter topic");
    // Update the latest flow meter reading
    latestReading = reading
  }
})

// Serve the web page
app.get('/', function (req, res) {
  res.send(`
    <html>
      <head>
        <title>Flow Meter Data</title>
        <style>
          table {
            border-collapse: collapse;
            width: 100%;
          }
          th, td {
            text-align: left;
            padding: 8px;
            border-bottom: 1px solid #ddd;
          }
          th {
            background-color: #4CAF50;
            color: white;
          }
        </style>
      </head>
      <body>
        <h1>Flow Meter Data</h1>
        <table>
          <tr>
            <th>Timestamp</th>
            <th>Flow Rate (L/min)</th>
            <th>Total Volume (L)</th>
          </tr>
          ${latestReading ? `
            <tr>
              <td>${latestReading.timestamp}</td>
              <td>${latestReading.flowRate}</td>
              <td>${latestReading.totalVolume}</td>
            </tr>
          ` : `
            <tr>
              <td colspan="3">No data received yet</td>
            </tr>
          `}
        </table>
      </body>
    </html>
  `)
})

// Start the web server
app.listen(3000, function () {
  console.log('App listening on port 3000!')
})

