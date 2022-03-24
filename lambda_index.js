const AWS = require("aws-sdk");

// Make sure your Lambda has DynamoDbBasicExecution Policy added to perform DynamoDB operations
const docClient = new AWS.DynamoDB.DocumentClient({
    region: 'us-east-1'
});

const getAllContracts = async (pagesize, chain, channel) => {
    const scanResult = await docClient.scan({
        TableName: 'telegram_db',
        // ExpressionAttributeValues: {
        //     ':val1': {
        //         S: chain,
        //     },
        // },
        // FilterExpression: "chain = :val1",
        // Limit: parseInt(pagesize)
    }).promise();
    
    return scanResult;
}

exports.handler = async (event) => {
    
    const pagesize = event.queryStringParameters.pagesize || 100;
    const chain = event.queryStringParameters.chain || '';
    const channel = event.queryStringParameters.channel || '';
    
    let data;
    try {
        data = await getAllContracts(pagesize, chain, channel);
    } catch (e) {
        
    }
    
    // Used for logging puposes
    //data.event = event;
    
    const response = {
        statusCode: 200,
        body:JSON.stringify(data)
    };
    
    return response;
};
