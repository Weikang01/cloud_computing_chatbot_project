import express from "express";
import { v4 as uuidv4 } from 'uuid';

const router = express.Router();

const users =[]
// all routes start with /users
router.get("/users", (req, res) => {

    console.log(users);
    res.send(users); // Send the users array as a JSON response
  });

router.post('/users', (req,res) => {
  

    const user = req.body;

    const user_ID = uuidv4(); // ⇨ '9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d'
    
    const userWithID = {...user, id:user_ID};

    users.push(userWithID);

    res.send('New user is added to the database' );
});

export default router;