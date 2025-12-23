const {client  }= require("../config/whatsappConfig");
const {MessageMedia}  = require("whatsapp-web.js");
const { getQr, getStatus } = require("../config/whatsappConfig");

async function sendMedia(number, pdfBuffer, message) {
  try {
const media = new MessageMedia('application/pdf', pdfBuffer.toString('base64'), 'recibo.pdf');


  const chatId = `${number}@c.us`;
  await client.sendMessage(chatId, media, {caption: message});

    console.log("Mensaje enviado:", message);
  } catch (error) {
    console.error("Error en envío:", error.message);
    throw error;
  }
}


async function sendMessage(number, message) {
  try {
    const chatId = `${number}@c.us`;
    await client.sendMessage(chatId, message);
    console.log("Mensaje enviado:", message);
  } catch (error) {
    console.error("Error en envío:", error.message);
    throw error;
  }
}



function getQrCode() {
  return getQr();
}

function getConnectionStatus() {
  return getStatus();
}

module.exports = { sendMessage, sendMedia, getQrCode, getConnectionStatus };
