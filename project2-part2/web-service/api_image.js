//
// app.post('/image/:userid', async (req, res) => {...});
//
// Uploads an image to the bucket and updates the database,
// returning the asset id assigned to this image.
//
const dbConnection = require('./database.js')
const { PutObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

const uuid = require('uuid');

exports.post_image = async (req, res) => {

  console.log("call to /image...");
  
  try {
    
    // var data = req.body;  // data => JS object

    // throw new Error("TODO: /image");
    // var S = req.body.data;
    // var bytes = Buffer.from(S, 'base64');

    

    // const client = new S3Client({});

    // export const main = async () => {
    //   const command = new PutObjectCommand({
    //     Bucket: "test-bucket",
    //     Key: "hello-s3.txt",
    //     Body: "Hello S3!",
    //   });

    //   try {
    //     const response = await client.send(command);
    //     console.log(response);
    //   } catch (err) {
    //     console.error(err);
    //   }
    // };

    // // generate a unique name for the asset:
    // let name = uuid.v4();
    
    const imageBase64 = req.body.data;
    const assetname=req.body.assetname;
    const userId = req.params.userid;
    //console.log(userId);
    // Check if the user ID exists in the database
    dbConnection.query('SELECT * FROM users WHERE userid = ?', [userId], (dbError, userRows) => {
      if (dbError) {
        res.status(400).json({
          "message": dbError.message,
          "assetid": -1
        });
      } else if (userRows.length === 0) {
        // User ID does not exist in the database
        res.status(400).json({
          "message": "no such user...",
          "assetid": -1
        });
      } else {
        // User ID exists in the database
        try {
          // Decode the base64-encoded image
          const bytes = Buffer.from(imageBase64, 'base64');

          // Generate a unique key for the asset
          const uniqueKey = `${userId}/${uuid.v4()}.jpg`;

          // Set up the parameters for the S3 PutObjectCommand
          const s3Params = {
            Bucket: s3_bucket_name,
            Key: uniqueKey,
            Body: bytes,
          };

          // Upload the image to S3
          s3.send(new PutObjectCommand(s3Params), async (s3Error) => {
            if (s3Error) {
              res.status(400).json({
                "message": s3Error.message,
                "assetid": -1
              });
            } else {
              // Insert the asset into the database
              dbConnection.query('INSERT INTO assets (userid, assetname, bucketkey) VALUES (?, ?, ?)', [userId, assetname,uniqueKey], (dbInsertError, result) => {
                if (dbInsertError) {
                  res.status(400).json({
                    "message": dbInsertError.message,
                    "assetid": -1
                  });
                } else {
                  res.status(200).json({
                    "message": "success",
                    "assetid": result.insertId
                  });
                }
              });
            }
          });
	
        }
        catch (err) {
            res.status(400).json({
              "message": err.message,
              "assetid": -1
            });
          }
        
      } 
    });
  
}//try
    
                      
  catch (err) {
    console.log("**ERROR:", err.message);

    res.status(400).json({
      "message": err.message,
      "assetid": -1
    });
  }//catch

}//post
     