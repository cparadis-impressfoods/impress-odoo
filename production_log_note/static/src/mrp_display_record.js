/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { MrpDisplayRecord } from "@mrp_workorder/mrp_display/mrp_display_record";
import { MrpLogNoteDialog } from "./dialog/mrp_log_note_dialog";
import { _t } from "@web/core/l10n/translation";

patch(MrpDisplayRecord.prototype, {
  editLogNote() {
    const title = _t("Log Note");
    const reload = () => this.env.reload();
    const params = { body: "", record: this.props.production, reload, title };
    this.dialog.add(MrpLogNoteDialog, params);
  },
  get logNote() {
    return this.props.production.data.log_note;
  },
});
