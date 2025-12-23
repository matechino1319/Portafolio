// //Porfa el codigo de la conexion a la db
// const mysql = require('mysql2/promise');
// require('dotenv').config();

// const pool = mysql.createPool({
//     host: process.env.DB_HOST,
//     user: process.env.DB_USER,
//     password: process.env.DB_PASSWORD,
//     database: process.env.DB_DATABASE,
//     waitForConnections: true, 
//     conectionLimit: 20,
//     queueLimit: 0
// });

// module.exports = pool;

const mysql = require('mysql2/promise');

const db = mysql.createPool({
  host: "localhost",     // o 127.0.0.1
  user: "root",          // tu usuario de MySQL
  password: "root",          // tu contraseña (si tiene)
  database: "datos_aprid",   // nombre de tu base local
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

module.exports = db;
