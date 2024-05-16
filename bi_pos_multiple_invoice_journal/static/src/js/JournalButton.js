odoo.define('bi_pos_multiple_invoice_journal.JournalButton', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require("@web/core/utils/hooks");

	class JournalButton extends PosComponent {
		setup() {
            super.setup();
			useListener('new-journalLine', this.addNewjournalLine);
        }

		addNewjournalLine({detail:journal}){
			var order = this.env.pos.get_order();
			order['invoice_journal_id'] = journal
		}

		click_set_invoicejournal(event){
			var self = this
			var on = parseInt(event.currentTarget.dataset['productId'])
			var order = this.env.pos.get_order();
			order['invoice_journal_id'] = on
			if(on){
				event.currentTarget[$('.journal-name').css({
					"background-color" : '#e2e2e2',
				    'color' : '#212529'
				})]
				event.currentTarget[$('#'+on).val(on).css({
					'color' : '#ffff',
					"background-color" : '"#017e84 !important'
				})]
			}
		}
	}

	JournalButton.template = 'JournalButton';
	Registries.Component.add(JournalButton);
	return JournalButton;
});