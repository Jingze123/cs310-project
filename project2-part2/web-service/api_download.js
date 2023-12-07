//
// app.get('/download/:assetid', async (req, res) => {...});
//
// downloads an asset from S3 bucket and sends it back to the
// client as a base64-encoded string.
//
const dbConnection = require('./database.js')
const { GetObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');
const { resolve } = require('dns');

exports.get_download = async (req, res) => {

  console.log("call to /download...");

  try {


    //throw new Error("TODO: /download/:assetid");

    //
    // TODO
    //
    // MySQL in JS:
    //   https://expressjs.com/en/guide/database-integration.html#mysql
    //   https://github.com/mysqljs/mysql
    // AWS:
    //   https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/javascript_s3_code_examples.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/classes/getobjectcommand.html
    //   https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/
    //

    // Extract the asset ID from the URL path.
    const assetId = req.params.assetid;

    /// Fetch the asset's details (user_id, asset_name, and bucket_key) from the database.
    const assetDetails = await fetchAssetDetailsFromDatabase(assetId);
    // assetDetails.bucket_key = "6b0be043-1265-4c80-9719-fd8dbcda8fd4/0ad14d57-0ce0-464d-9be2-cfa33eee0e5e.jpg"

    if (assetDetails != null) {
      // console.log(assetDetails)
      // Create a command to get the object (asset) from S3 using the bucket key.
      const getObjectCommand = new GetObjectCommand({
        Bucket: s3_bucket_name,
        Key: assetDetails.bucket_key
      });
    
      // Use the AWS SDK to retrieve the object (asset) from S3.
      const result = await s3.send(getObjectCommand);
      // console.log(result);
      if (result.Body) {
        // Convert the object (asset) data to a base64-encoded string using transformToString.
        const datastr = await result.Body.transformToString("base64");

        // Send the base64-encoded data along with user_id and asset_name as a response to the client.
        res.status(200).json({
          "message": "success",
          "user_id": assetDetails["user_id"],
          "asset_name": assetDetails["asset_name"],
          "bucket_key": assetDetails["bucket_key"],
          "data": datastr,
        });
      }
      else {
        res.status(400).json({
          "message": "no such asset...",
          "user_id": -1,
          "asset_name": "?",
          "bucket_key": "?",
          "data": []
        });
      }
      return;
    }
    else{
        res.status(400).json({
        "message": "no such asset...",
        "user_id": -1,
        "asset_name": "?",
        "bucket_key": "?",
        "data": []
      });
    }
  }//try
  catch (err) {
    //
    // generally we end up here if we made a 
    // programming error, like undefined variable
    // or function:
    //
    res.status(400).json({
      "message": err.message, 
      "user_id": -1,
      "asset_name": "?",
      "bucket_key": "?",
      "data": []
    });
  }//catch

}//get

async function fetchAssetDetailsFromDatabase(assetId) {
  const sql = 'SELECT userid, assetname, bucketkey FROM assets WHERE assetid = ?';
  const results = await new Promise((resolve, reject) => {
    dbConnection.query(sql, [assetId], (err, results) => {
      if (err) {
        reject(err);
        return;
      } else {
        resolve(results);
      }
    });
  });
  if (results.length !== 0) {
    return {
      user_id: results[0]["userid"],
      asset_name: results[0]["assetname"],
      bucket_key: results[0]["bucketkey"]
    };
  } else {
  //   return res.status(400).json({
  //       "message": "no such asset...",
  //       "user_id": -1,
  //       "asset_name": "?",
  //       "bucket_key": "?",
  //       "data": []
  //     });;
  // }
    return null;
}
}





//   if (rows.length > 0) {
//     // If a matching row is found, return the asset details.
//     return {
//       user_id: rows[0].userid,
//       asset_name: rows[0].assetname,
//       bucket_key: rows[0].bucketkey,
//     };
//   } else {
//     // If no matching row is found, return null or an appropriate default value.
//     return err;
//   }
// }