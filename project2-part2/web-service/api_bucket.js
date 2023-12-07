//
// app.get('/bucket?startafter=bucketkey', async (req, res) => {...});
//
// Retrieves the contents of the S3 bucket and returns the 
// information about each asset to the client. Note that it
// returns 12 at a time, use startafter query parameter to pass
// the last bucketkey and get the next set of 12, and so on.
//
const { ListObjectsV2Command } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

exports.get_bucket = async (req, res) => {

  console.log("call to /bucket...");

  try {

    
    //throw new Error("TODO: /bucket/?startafter=bucketkey");

    //
    // TODO: remember, 12 at a time...  Do not try to cache them here, instead 
    // request them 12 at a time from S3
    //
    // AWS:
    //   https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/javascript_s3_code_examples.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/classes/listobjectsv2command.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/
    //
    
    
    // Get the "startafter" parameter from the request query, if provided
    const startAfter = req.query.startafter;

    // Configure the ListObjectsV2Command with the desired parameters
    const params = {
      Bucket: s3_bucket_name,
      MaxKeys: 12, // You can adjust the page size here
      StartAfter: startAfter, // Optional, used for pagination
    };

    const data = await s3.send(new ListObjectsV2Command(params));

    // Check if KeyCount is 0, which indicates an empty response
    if (data.KeyCount === 0) {
      res.json({ "message": "Success", "data": [] });
    } else {
      // Extract the object data from the response Contents
      const objects = data.Contents;
      res.json({ "message": "Success", "data": objects });
    }

  }//try
  catch (err) {
    res.status(400).json({
      "message": err.message,
      "data": []
    });
  }//catch

}//get
