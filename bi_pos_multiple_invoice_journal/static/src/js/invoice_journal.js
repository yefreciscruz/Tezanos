odoo.define('bi_pos_multiple_invoice_journal.invoice_journal', function(require) {
"use strict";

	var { PosGlobalState,Order } = require('point_of_sale.models');
	const Registries = require('point_of_sale.Registries');

	const PosHomePosGlobalState = (PosGlobalState) => class PosHomePosGlobalState extends PosGlobalState {
		//@override
	    async _processData(loadedData) {
	        await super._processData(...arguments);
            this.account_journal = loadedData['account.journal'];
	    }

	}
	Registries.Model.extend(PosGlobalState, PosHomePosGlobalState);

	const BiCustomOrder = (Order) => class BiCustomOrder extends Order{
		constructor(obj, options) {
        	super(...arguments);
			this.invoice_journal_id = this.invoice_journal_id || false;
		}

		set_invoice_journal_id(invoice_journal_id) {
			this.invoice_journal_id = invoice_journal_id;
		}

		export_as_JSON() {
			const json = super.export_as_JSON(...arguments);
			json.invoice_journal_id = this.invoice_journal_id || false;
			return json;
		}

		init_from_JSON(json){
			super.init_from_JSON(...arguments);
			this.invoice_journal_id = json.invoice_journal_id || false;
		}

	}
	Registries.Model.extend(Order, BiCustomOrder);

});