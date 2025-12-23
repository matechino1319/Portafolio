const express = require('express');
const cors = require('cors');
//agrego esto del login
const authRoutes = require('./routes/authRoutes.js')
// const verificarToken = require('./middleware/authMiddleware');
//hasta aca <3
const whatsappRoutes = require('./routes/whatsappRoutes.js');
const reciboRoutes = require('./routes/reciboRoutes.js');
const alumnoRoutes = require('./routes/alumnoRoutes.js');
const usuarioRoutes = require('./routes/usuarioRoutes.js');
const app = express();
const PORT = 3000;


app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));


// Midware
app.use(express.json());

// Rutas
app.use('/usuario', usuarioRoutes);
app.use('/auth', authRoutes); 
app.use('/whatsapp', whatsappRoutes);
app.use('/recibos', reciboRoutes);
app.use('/alumnos', alumnoRoutes);


app.listen(PORT, () => {
  console.log(`Servidor funcionando en http://localhost:${PORT}`);
});
