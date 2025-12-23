const express = require("express");
const router = express.Router();
const { sendMessageController, sendReceiptController, getStatus } = require("../controllers/whatsappController.js");


router.post("/send", sendMessageController);
router.post("/sendPDF", sendReceiptController);
router.get("/status", getStatus);



module.exports = router;
