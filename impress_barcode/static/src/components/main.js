/** @odoo-module **/

import MainComponent from "@stock_barcode/components/main";
import { patch } from "@web/core/utils/patch";
import MoveComponent from "./move";
import { Chatter } from "@mail/core/web/chatter";
import { View } from "@web/views/view";
import GroupedLineComponent from '@stock_barcode/components/grouped_line';
import LineComponent from '@stock_barcode/components/line';
import PackageLineComponent from '@stock_barcode/components/package_line';


patch(MainComponent.prototype, {

    get unreservedMoves() {
        return this.env.model.unreservedMoves;
    },

});

MainComponent.components = {
    Chatter,
    View,
    GroupedLineComponent,
    LineComponent,
    PackageLineComponent,
    MoveComponent
};


