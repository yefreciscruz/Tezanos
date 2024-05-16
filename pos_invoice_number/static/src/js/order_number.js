odoo.define("pos_order_number.receiptScreen", function (require) {
    "use strict";

    const OrderReceipt = require("point_of_sale.OrderReceipt");
    const Registries = require("point_of_sale.Registries");
    const rpc = require('web.rpc');
    const { onMounted } = owl;

    const PosResOrderReceipt = (OrderReceipt) =>
        class extends OrderReceipt {
            setup() {
                super.setup();
                var self = this;
                var order = self.props.order;
                if (order.is_to_invoice() && self.env.pos.config.pos_invoice_number) {
                    rpc.query({
                        model: "pos.order",
                        method: "search_read",
                        domain: [["pos_reference", "=", order["name"]]],
                        fields: ["account_move","multi_id"],
                    }).then(function (orders) {
                        if (orders.length > 0 && orders[0]["account_move"] && orders[0]["account_move"][1]) {
                            var invoice_number = orders[0]["account_move"][1].split(" ")[0];
                            var journal_name = orders[0]["multi_id"][1]

                            console.log("Valor account_move: " +orders[0]["account_move"][1].split(" "));
                            console.log("Valor multi_id: " +orders[0]["multi_id"][1]);
                            order["invoice_number"] = invoice_number;
                            order["journal_name"] = journal_name;
                        }
                        self.render();
                    });
                }
            }
        };

    Registries.Component.extend(OrderReceipt, PosResOrderReceipt);

    return PosResOrderReceipt
})
