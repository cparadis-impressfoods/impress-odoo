/** @odoo-module **/

import {patch} from '@web/core/utils/patch';
import { MrpDisplayRecord } from '@mrp_workorder/mrp_display/mrp_display_record';

patch(MrpDisplayRecord.prototype,
    {

        async workorderValidation(skipRemoveFromStack = false) {
            const { resId, resModel } = this.props.record;
            const context = { no_start_next: true, mrp_display: true };
            if (this.validatingEmployee) {
                context.employee_id = this.validatingEmployee;
            }
            context.skip_backorder = true;
            await this.model.orm.call(resModel, "do_finish", [resId], { context });
            if (!skipRemoveFromStack){
                await this.props.removeFromValidationStack(this.props.record);
            }
            this.state.validated = true;
            await this.props.updateEmployees();
        }
    
});