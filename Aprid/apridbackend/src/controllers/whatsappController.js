const { sendMessage, sendMedia, getConnectionStatus, getQrCode } = require("../services/whatsappService");
const { generateReceipt } = require("../utils/pdfGenerator");

function dataTester(number, message){
  if (!number || !message) {
    return { valid: false, error: "Número y mensaje son requeridos" };
  } else{
    return { valid: true };
  }
}



async function sendReceiptController(req, res) {
  try {
    const data = req?.body ? req.body : req;
  const {
      number,
      message,
      name,
      dni_alumno,
      id_comprobante,
      amount,
      description,
      cuantity,
      fecha_pago
    } = data;

    console.log(
      `SendReceiptCtrl=${number}, ${message}, ${name},${dni_alumno} ${amount}, ${description}, ${cuantity}`
    );

    const result = dataTester(number, message);
    if (!result.valid) {
      if (res) return res.status(400).json({ error: result.error });
      else throw new Error(result.error);
    }

     const pdfBuffer = await generateReceipt({
      name,
      amount,
      id_comprobante,
      dni_alumno,
      description,
      cuantity,
      fecha_pago
    });
    console.log(pdfBuffer);

    await sendMedia(number, pdfBuffer, message);

    if (res) {
      res.json({ success: true, message: "Mensaje enviado correctamente" });
    } else {
      console.log("Mensaje enviado correctamente");
    }
  } catch (error) {
    console.error("Error al enviar mensaje:", error.message);
    if (res) {
      res.status(500).json({ error: "Error al enviar el mensaje", detail: error.message });
    } else {
      throw error;
    }
  }
}












async function sendMessageController(req, res) {
  const { number, message } = req.body;
  console.log(req.body);
  

  const result = dataTester(number, message)
  if(!result.valid) return res.status(400).json({error: result.error});

  try {
    await sendMessage(number, message);
    res.json({ success: true, message: "Mensaje enviado correctamente" });
  } catch (error) {
    res.status(500).json({ error: "Error al enviar el mensaje", detail: error.message });
  }
}



const getStatus = async (req, res) => {
  try {
    console.log("holaa");
    
      const status = getConnectionStatus();
    const qr = getQrCode();

    res.json({
      status,
      qr: status === "WAITING_QR" ? qr : null,
    });
  } catch (error) {
    res.status(500).json({ error: "Error al obtener estado de WhatsApp" });
  }
};




module.exports = { sendMessageController, sendReceiptController, getStatus };