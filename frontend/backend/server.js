const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');

require('dotenv').config();

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

const uri = process.env.COMPASS_URI;
mongoose.connect(uri, {useNewUrlParser: true, useCreateIndex: true, useUnifiedTopology: true});

const connection = mongoose.connection;
connection.once('open', () => {
    console.log("MOngoDB database connection established successfully.")
})

const userRoute = require('./routes/user');

app.use('/users', userRoute);

app.listen(port, () => {
    console.log(`Server is up and running on ${port}`);
});