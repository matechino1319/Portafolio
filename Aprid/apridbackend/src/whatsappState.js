let qrCode = null;
let status = 'INICIALIZANDO'; 

const setQrCode = (qr) => {
    qrCode = qr;
    status = 'QR_GENERADO';
    console.log(`[STATE] QR generado. Listo para escanear.`);
};

const setStatus = (newStatus) => {
    if (newStatus === 'CONECTADO') {
        qrCode = null;
    }
    status = newStatus;
    console.log(`[STATE] Estado: ${newStatus}`);
};

const getQrData = () => {
    return {
        qr: qrCode, 
        status: status
    };
};

module.exports = {
    setQrCode,
    setStatus,
    getQrData
};