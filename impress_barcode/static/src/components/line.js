/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import LineComponent from "@stock_barcode/components/line";


patch(LineComponent.prototype, {

    get totalDemand() {
        return this.env.model.getTotalDemand(this.line.move_id);
    },

});
