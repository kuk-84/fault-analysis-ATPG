import { logicInput, logicOutput, gate, flipflop, logicClock, srLatch, wireMng } from "./simulator.js"
import { LogicInput } from "./LogicInput.js"
import { LogicOutput } from "./LogicOutput.js";
import { Clock } from "./Clock.js";
import { Gate } from "./Gate.js";
import { nodeList } from "./Node.js";

let eventHistory = [];

/**
 * @todo TODO
 */
export class FileManager {

    /**
     * @todo TODO
     */
    constructor()
    {
        this.isLoadingState = false;
    }

    /**
     * @todo TODO
     */
    saveState() {
        /* TODO
        if(this.isLoadingState)
            return;
        
        eventHistory.unshift(FileManager.getJSON_Workspace());
        if (eventHistory.length > 10) {
            delete eventHistory[10];
            eventHistory.length = 10;
        }
        console.log(eventHistory);*/
    }

    /**
     * @todo TODO
     */
    loadFile(e) {
        this.isLoadingState = true;

        flipflop.splice(0, flipflop.length);
        srLatch.splice(0, srLatch.length);
        gate.splice(0, gate.length);
        wireMng.wire.splice(0, wireMng.wire.length);
        logicClock.splice(0, logicClock.length);
        logicInput.splice(0, logicInput.length);
        logicOutput.splice(0, logicOutput.length);
        nodeList.splice(0, nodeList.length);

        //this.e = e;

        let file = e.target.files.item(0);

        let reader = new FileReader();
        reader.onload = function () {

            let contentFile = reader.result;
            //console.log(contentFile);

            // logic input
            if ("logicInput" in JSON.parse(contentFile)) {
                for (let i = 0; i < contentFile.length; i++) {
                    let objectParsed = JSON.parse(contentFile).logicInput[i];

                    if (objectParsed == undefined)
                        break;

                    console.log("lm",objectParsed);
                    logicInput.push(new LogicInput());
                    Object.assign(logicInput[i], objectParsed);
                    logicInput[i].refreshNodes();
                }
            }
            // logic output
            //console.log(logicOutput);
            if ("logicOutput" in JSON.parse(contentFile)) {
                for (let i = 0; i < contentFile.length; i++) {

                    let objectParsed = JSON.parse(contentFile).logicOutput[i];

                    if (objectParsed == undefined)
                        break;

                    console.log(objectParsed);
                    logicOutput.push(new LogicOutput());
                    Object.assign(logicOutput[i], objectParsed);
                    logicOutput[i].refreshNodes();
                }
            }

            if ("logicClock" in JSON.parse(contentFile)) {
                for (let i = 0; i < contentFile.length; i++) {

                    let objectParsed = JSON.parse(contentFile).logicClock[i];

                    if (objectParsed == undefined)
                        break;

                    console.log(objectParsed);
                    logicClock.push(new Clock());
                    Object.assign(logicClock[i], objectParsed);
                    logicClock[i].refreshNodes();
                }
            }

            if ("gate" in JSON.parse(contentFile)) {
                for (let i = 0; i < contentFile.length; i++) {

                    let objectParsed = JSON.parse(contentFile).gate[i];

                    if (objectParsed == undefined)
                        break;

                    console.log(objectParsed);
                    gate.push(new Gate(JSON.parse(contentFile).gate[i].strType));
                    Object.assign(gate[i], objectParsed);
                    gate[i].refreshNodes();
                }
            }

            

            if ("wire" in JSON.parse(contentFile)) {
                for (let i = 0; i < contentFile.length; i++) {
                    let objectParsed = JSON.parse(contentFile).wire[i];

                    if (objectParsed == undefined)
                        break;

                    console.log(objectParsed);

                    wireMng.addNode(nodeList[objectParsed.startID]);
                    wireMng.addNode(nodeList[objectParsed.endID]);
                    //Object.assign(gate[i], objectParsed);
                }
            }

        };
        reader.readAsText(file);
    }


    /**
     * @todo TODO
     */
    saveFile(e) {

        let jsonWorkspace = FileManager.getJSON_Workspace();
        let blob = new Blob([jsonWorkspace], { type: 'application/json' });
        saveProjectFile.href = URL.createObjectURL(blob);
        //console.log(jsonWorkspace);
    }

    /**
     * @todo TODO
     */
    static getJSON_Workspace() {
        let workspace = new Object();

        workspace["logicInput"] = logicInput;
        workspace["logicOutput"] = logicOutput;
        workspace["flipflop"] = flipflop;
        workspace["logicClock"] = logicClock;
        workspace["gate"] = gate;
        workspace["srLatch"] = srLatch;
        workspace["wire"] = wireMng.wire;

        let jsonWorkspace = JSON.stringify(workspace,
            function (key, value) {
                switch (key) {
                    case "output":
                    case "input":
                    case "nodeSet":
                    case "nodeReset":
                    case "nodeClock":
                    case "nodeD":
                    case "nodeT":
                    case "nodeJ":
                    case "nodeK":
                    case "nodeQ":
                    case "nodeNotQ":
                    case "andGate_NotQ":
                    case "andGate_Q":
                    case "ff_D":
                    case "orGate":
                    case "gateSet":
                    case "gateReset":
                    case "asyncLatch":
                    case "master":
                    case "slave":
                    case "srLatchSync":
                    case "startNode":
                    case "endNode":
                        return undefined;
                }

                // other things which is not possible to export on JSON
                //console.log("manya",value);
                return value;
            }, '\t');
        return jsonWorkspace;
    }
}
