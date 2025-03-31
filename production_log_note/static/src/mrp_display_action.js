/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { MrpDisplayAction } from "@mrp_workorder/mrp_display/mrp_display_action";

patch(MrpDisplayAction.prototype, {
  get fieldsStructure() {
    const fieldsStructure = super.fieldsStructure;
    fieldsStructure["mrp.production"].push("log_note");
    return fieldsStructure;
  },
});
