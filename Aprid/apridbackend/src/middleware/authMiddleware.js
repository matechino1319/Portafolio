const jwt = require('jsonwebtoken');
const SECRET_KEY = '8d7f2b1e5a3c9a6d0f4g2h8i1j7k3l5m9n';

function verificarToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) return res.status(401).json({ error: 'Acceso denegado' });

  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) return res.status(403).json({ error: 'Token inválido o expirado' });
    req.user = user;
    next();
  });
}

module.exports = verificarToken;
