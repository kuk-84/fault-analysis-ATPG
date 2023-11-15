import json
import subprocess
import os

def generate_netlist():
    def process_json_file(input_file, output_file, flag):
        # Load the JSON data from the file
        with open(input_file, 'r') as json_file:
            data = json.load(json_file)

        gate_data = data['gate']
        wire_data = data['wire']

        # Initialize a dictionary to store gate information
        gate_info = {}
        count = 1
        # Iterate through the gate data
        for gate in gate_data:
            gate_type = gate['strType']
            gate_start_id = gate['nodeStartID']
            input_wire_ids = []

            # Find wires connected to the gate's input pins
            for wire in wire_data:
                if (wire['endID'] == gate_start_id or wire['endID'] == gate_start_id+1):
                    # Check if f"n{wire['startID']}" matches an existing output_wire_id in gate_info
                    matching_output_id = None
                    for existing_gate_id, existing_info in gate_info.items():
                        if f"n{wire['startID']}" == existing_info['output_wire_id']:
                            matching_output_id = existing_info['output']
                            break

                    if matching_output_id:
                        input_wire_ids.append(matching_output_id)
                    else:
                        input_wire_ids.append(f"in{wire['startID'] + 1}")
            
            # Label the not gate's input and output pins
            if gate_type == 'NOT' or gate_type == 'sa1' or gate_type == 'sa0':
                output_wire_id = f'n{gate_start_id + 1}'
            else:
                output_wire_id = f'n{gate_start_id + 2}'

            
            # Store the gate information in the dictionary
            gate_info[gate_start_id] = {
                'gate_type': gate_type,
                'input_wire_ids': input_wire_ids,
                'output_wire_id': output_wire_id,
                'output': f"n{count}"
            }
            count+=1
        if(flag):
            with open(output_file, 'w') as txt_file:
                for gate_id, info in gate_info.items():
                    if info["gate_type"] == "sa1":
                        input_wire_ids_str = ' '.join(info["input_wire_ids"])
                        txt_file.write(f'value: 1 location: {input_wire_ids_str}\n')
                    if info["gate_type"] == "sa0":
                        input_wire_ids_str = ' '.join(info["input_wire_ids"])
                        txt_file.write(f'value: 0 location: {input_wire_ids_str}\n')
        else:
            gate_counts={}
            with open(output_file, 'w') as txt_file:
                for gate_id, info in gate_info.items():
                    count = gate_counts.get(info["gate_type"],1)
                    gate_type_format=info["gate_type"].lower()
                    if(info["gate_type"]=="NOT"):
                        gate_type_format = f'{gate_type_format}{count}'
                    else:
                        no_of_input_wires=len(info["input_wire_ids"])
                        gate_type_format = f'{gate_type_format}{no_of_input_wires}_{count}'
                    
                    count=count+1
                    gate_counts[info["gate_type"]]=count

                    # txt_file.write(f'Gate ID: {gate_id}\n')
                    # txt_file.write(f'Gate Type: {info["gate_type"]}\n')
                    # txt_file.write(f'Input Wire IDs: {info["input_wire_ids"]}\n')
                    # txt_file.write(f'Output Wire ID: {info["output_wire_id"]}\n')
                    # txt_file.write(f'Output: {info["output"]}\n')
                    # txt_file.write('\n')
                    input_wire_ids_str = ' '.join(info["input_wire_ids"])
                    
                    txt_file.write(f'{gate_type_format} {info["output"]} {input_wire_ids_str}')
                    txt_file.write('\n')

            lines=[]
            with open(output_file, 'r') as file:
                lines = file.readlines()
                last_line = lines[-1].strip()
                new_last_line = last_line.replace('n10', 'out1')
                lines[-1] = new_last_line + '\n'  # Add newline character back
            with open(output_file, 'w') as file:
                file.writelines(lines)




    # Run with the first file
    process_json_file('C:/Users/sakshi/OneDrive/Desktop/fault-analysis-ATPG/json/LogicCircuit00.json', 'C:/Users/sakshi/OneDrive/Desktop/fault-analysis-ATPG/netlist1.txt',0)

    # Run with the second file
    process_json_file('C:/Users/sakshi/OneDrive/Desktop/fault-analysis-ATPG/json/LogicCircuit1.json', 'C:/Users/sakshi/OneDrive/Desktop/fault-analysis-ATPG/fault.txt',1)
    print("generated")
    result = subprocess.run(["python", "podem.py"], capture_output=True, text=True).stdout.strip()
    print(f"Result from podem.py: {result}")
    return result
    #subprocess.run(["python", "podem.py"])
