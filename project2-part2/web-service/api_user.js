//
// app.put('/user', async (req, res) => {...});
//
// Inserts a new user into the database, or if the
// user already exists (based on email) then the
// user's data is updated (name and bucket folder).
// Returns the user's userid in the database.
//
const dbConnection = require('./database.js')

exports.put_user = async (req, res) => {

  console.log("call to /user...");

  try {

    var data = req.body;  // data => JS object

    console.log(data);

   

  



    dbConnection.query('SELECT userid FROM users WHERE email = ?', [data.email], (err, rows) => {
      if (err) {
        res.status(400).json({
          "message": "a some sort of error message",
          "userid": -1
        });
      }
      else{
        if (rows.length > 0) {
          // User already exists
          // Update the user's data
          dbConnection.query('UPDATE users SET lastname = ?, firstname = ?, bucketfolder = ? WHERE email = ?', [data.lastname, data.firstname, data.bucketfolder, data.email], (err, row) => {
            if (err) {
              res.status(400).json({
                "message": "b some sort of error message",
                "userid": -1
              });
            } else {
              res.status(200).json({
                "message": "updated",
                "userid": rows[0]["userid"],
                
              });
              
            }
          
      });}
        else {
            // User does not exist
            // Insert the user's data
            console.log("def");
            dbConnection.query('INSERT INTO users (email, lastname, firstname, bucketfolder) VALUES (?, ?, ?, ?)', [data.email, data.lastname, data.firstname, data.bucketfolder], (err, ro) => {
              if (err) {
                res.status(400).json({
                  "message": err.message,
                  "userid": -1
                });
              } else {
                res.status(200).json({
                  "message": "inserted",
                  "userid": ro.insertId
                });
              }
            });
        }
      }
        

});

    
 }//try
  catch (err) {
    console.log("**ERROR:", err.message);

    res.status(400).json({
      "message": err.message,
      "userid": -1
    });
  }//catch

}//put
