import { Clock } from "./circuit_components/Clock.js";
import { FF_D_Single, FF_D_MasterSlave } from "./circuit_components/FF_D.js";
import { FF_JK } from "./circuit_components/FF_JK.js";
import { FF_T } from "./circuit_components/FF_T.js";
import { flipflop, logicInput, logicOutput, logicClock, gate, srLatch } from "./simulator.js";
import { Gate } from "./circuit_components/Gate.js";
import { LogicInput } from "./circuit_components/LogicInput.js";
import { LogicOutput } from "./circuit_components/LogicOutput.js";
import { MouseAction, syncType } from "./circuit_components/Enums.js"
import { SR_LatchSync, SR_LatchAsync, SR_Latch } from "./circuit_components/SR_Latch.js"

export let currMouseAction = MouseAction.EDIT;

/**
 * @todo TODO
 */
export function activeTool(elTool) {
    resetElements();
    if (elTool.getAttribute("isGate") != null) {
        gate.push(new Gate(elTool.getAttribute("tool")));
        return;
    }

    switch (elTool.getAttribute("tool")) {
        case "Edit":
            resetElements();
            break;


        case "Delete":
            currMouseAction = MouseAction.DELETE;
            break;

        case "LogicInput":
            logicInput.push(new LogicInput());
            console.log(JSON.stringify({ logicInput }, ['logicInput', 'posX', 'posY', 'value']));
            break;

        case "LogicOutput":
            logicOutput.push(new LogicOutput());
            break;

    }

    elTool.classList.add('active');

}

/**
 * @todo this doc
 */
function resetElements() {
    currMouseAction = MouseAction.EDIT;
    let activeElements = document.getElementsByClassName("active");

    for (let i = 0; i < activeElements.length; i++) {
        activeElements[i].classList.remove('active')
    }
    document.getElementById("canvas-sim").style.cursor = "default";
}

/**
 * Reset Element
 * then set current action to EDIT 
 */
export function backToEdit() {
    resetElements();
    document.getElementsByClassName("Edit")[0].classList.add("active");
    currMouseAction = MouseAction.EDIT;
}

/**
 * Save Option
 * Export All logic input and output on console
 */
export function save() {

    for (let i = 0; i < logicInput.length; i++) {
        console.log(logicInput[i].export());
    }
}