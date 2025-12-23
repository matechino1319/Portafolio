const qrcode = require("qrcode-terminal");
const { Client, LocalAuth } = require("whatsapp-web.js");

let qrCodeData = null;
let isReady = false;

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: { headless: true },
});

client.on("qr", (qr) => {
  qrCodeData = qr;
  console.log("Nuevo QR generado (también visible en terminal):");
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  isReady = true;
  console.log("✅ Cliente WhatsApp conectado y listo.");
});

client.on("authenticated", () => {
  console.log("Cliente autenticado");
});

client.on("auth_failure", (msg) => {
  console.error("Error de autenticación:", msg);
});

client.on("disconnected", () => {
  console.log("Cliente desconectado, reiniciando...");
  isReady = false;
  client.initialize(); 
});

client.initialize();

module.exports = {
  client,   
  getQr: () => qrCodeData,
  getStatus: () => (isReady ? "CONNECTED" : "WAITING_QR"),
};
