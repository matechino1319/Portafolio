import PDFDocument from "pdfkit";

export const generateReceipt = async (data) => {
  return new Promise((resolve, reject) => {
    try {
      const doc = new PDFDocument({ margin: 50 });
      const chunks = [];

      doc.on("data", (chunk) => chunks.push(chunk));
      doc.on("end", () => resolve(Buffer.concat(chunks)));
      doc.on("error", (err) => reject(new Error(`Error generando el PDF: ${err.message}`)));

      const safeAmount = parseFloat(data.amount) || 0;

      const reciboId = data.id_comprobante || 'PAG-' + Date.now().toString().slice(-6);
      const alumnoNombre = data.name || 'Alumno No Especificado';
      const alumnoDni = data.dni_alumno || '00000000';
      const fechaPago = data.fecha_pago || new Date().toISOString().slice(0, 10);
      console.log("GAAAAAAAAAAAAAAA");
      console.log(reciboId);
      console.log(data.id_comprobante);

      const primaryColor = '#4a4a4a';
      const accentColor = 'rgba(10, 134, 205, 1)';
      const lightGray = '#eee';
      const borderColor = '#ccc';
      const leftMargin = 50;
      const rightMargin = doc.page.width - 50;
      let currentY = 50;

      doc.font('Helvetica');

      // Cabecera
      doc.fontSize(16)
        .fillColor(accentColor)
        .text("APRID", leftMargin, currentY, { align: 'left' });

      doc.fontSize(10)
        .fillColor(primaryColor)
        .text("San Rafael, Mendoza", leftMargin, currentY + 18);

      doc.rect(rightMargin - 150, 50, 150, 45).fillAndStroke(lightGray, primaryColor);
      doc.fontSize(12).fillColor(primaryColor)
        .text(`RECIBO N°`, rightMargin - 145, 55, { width: 140, align: 'left' });

      doc.fontSize(14).fillColor(accentColor).font('Helvetica-Bold')
        .text(reciboId, rightMargin - 145, 75, { width: 140, align: 'left' }); // 💡 Campo corregido
      doc.font('Helvetica');

      currentY = 110;

      doc.strokeColor(primaryColor).lineWidth(1).moveTo(leftMargin, currentY).lineTo(rightMargin, currentY).stroke();
      currentY += 15;

      doc.fontSize(10).fillColor(primaryColor);
      doc.text("Recibí(mos) de:", leftMargin, currentY);
      doc.font('Helvetica-Bold').text(alumnoNombre, leftMargin + 80, currentY, { underline: true, width: 250 });

      doc.font('Helvetica').text("Fecha:", rightMargin - 180, currentY);
      doc.font('Helvetica-Bold').text(fechaPago, rightMargin - 140, currentY, { underline: true, width: 130 });
      currentY += 25;

      doc.font('Helvetica').text("Identificación (DNI/CUIT):", leftMargin, currentY);
      doc.font('Helvetica-Bold').text(alumnoDni, leftMargin + 130, currentY, { underline: true, width: 150 });
      currentY += 35;

      doc.rect(leftMargin, currentY, rightMargin - leftMargin, 20).fillAndStroke(accentColor, accentColor);
      doc.fontSize(10).fillColor('#ffffff').text("CONCEPTO", leftMargin + 10, currentY + 6);
      doc.text("IMPORTE", rightMargin - 60, currentY + 6, { align: 'right' });
      currentY += 20;

      doc.rect(leftMargin, currentY, rightMargin - leftMargin, 20).fillAndStroke('#ffffff', borderColor);
      doc.fontSize(10).fillColor(primaryColor);

      const conceptoDisplay = `PAGO DE CUOTA ${data.description ? '- ' + data.description.toUpperCase() : ''}`;
      doc.text(conceptoDisplay, leftMargin + 10, currentY + 6);

      doc.font('Helvetica-Bold').text(`$${safeAmount.toFixed(2)}`, rightMargin - 60, currentY + 6, { align: 'right' });
      currentY += 40;

      doc.fontSize(10).font('Helvetica').fillColor(primaryColor);
      doc.text("La suma de:", leftMargin, currentY);
      doc.font('Helvetica-Bold').text("CANTIDAD DE PESOS EN LETRAS (Simulado)", leftMargin + 60, currentY, { underline: true });
      currentY += 20;

      const boxWidth = 150;
      const boxX = rightMargin - boxWidth;
      doc.rect(boxX, currentY, boxWidth, 25).fillAndStroke(lightGray, primaryColor);
      doc.fontSize(12).fillColor(primaryColor).text("TOTAL", boxX + 10, currentY + 8);
      doc.fontSize(16).fillColor(accentColor).font('Helvetica-Bold')
        .text(`$${safeAmount.toFixed(2)}`, boxX, currentY + 5, { width: boxWidth - 5, align: 'right' });

      currentY += 50;

      doc.end();

    } catch (err) {

      reject(err);
    }
  });
};