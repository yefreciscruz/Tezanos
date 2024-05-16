odoo.define('pos_dominicana_pay.PaymentScreen', function (require) {
    'use strict';
    var rpc = require('web.rpc')
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { onMounted } = owl;

    const PosPaymentReceiptExtend = PaymentScreen => class extends PaymentScreen {
        setup() {
        super.setup();

        }
         async validateOrder(isForceValidate) {
            var receipt_number = this.env.pos.selectedOrder.name
            var orders = this.env.pos.selectedOrder
            const receipt_order = await super.validateOrder(...arguments);
            const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter();
            var self= this;

            console.log("Dentro de... ")
            console.log("Recibo No.: " + receipt_number)

         rpc.query({
                model: 'pos.order',
                method: 'get_invoice_itp',
                args: [receipt_number]
                }).then(function(result){
                // const address = `${result.base_url}/my/invoices/${result.invoice_id}?`
                // const barcode = result.barcode
                // let qr_code_svg = new XMLSerializer().serializeToString(codeWriter.write(address, 150, 150));
                // self.env.pos.qr_image = "data:image/svg+xml;base64,"+ window.btoa(qr_code_svg);
                // let barcode_svg = new XMLSerializer().serializeToString(codeWriter.write(barcode, 150, 150));
                // self.env.pos.barcode_image = "data:image/svg+xml;base64,"+ window.btoa(barcode_svg);
                // self.env.pos.barcode = barcode
                self.env.pos.invoice  = result.invoice_name
                self.env.pos.nombre_diario = result.nombre_diario
                self.env.pos.direccion_tienda = result.direccion_tienda
                });
                return receipt_order
         }
         }


       Registries.Component.extend(PaymentScreen, PosPaymentReceiptExtend);

    return PaymentScreen;
       });

