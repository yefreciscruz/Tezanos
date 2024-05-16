odoo.define('bi_pos_multiple_invoice_journal.PaymentScreen', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	const PaymentScreen = require('point_of_sale.PaymentScreen');

	const JournalpopupPaymentScreen = (PaymentScreen) =>
		class extends PaymentScreen {
			setup() {
            	super.setup();
			}

		async _finalizeValidation() {
			let self = this;
			if(this.currentOrder['invoice_journal_id']){
				super._finalizeValidation();
			}else{
				self.showPopup('ConfirmPopup', {
					title: self.env._t('Select any journal'),
					body: self.env._t('Please Select any one invoice journal to Validate Order'),
				});
			}
		}
	};

	Registries.Component.extend(PaymentScreen, JournalpopupPaymentScreen);
	return PaymentScreen;

});