import xml.etree.ElementTree as ET

xml_file = './reports/network_scan.xml'

dot_file = 'network_graph.dot'

tree = ET.parse(xml_file)
root = tree.getroot()

with open(dot_file, 'w') as f:
    f.write("digraph G {\n")
    
    for host in root.findall('host'):
        ip = host.find('address').get('addr')
        f.write(f'    "{ip}" [label="{ip}"];\n')

        for port in host.findall('ports/port'):
            port_id = port.get('portid')
            service = port.find('service').get('name') if port.find('service') is not None else 'unknown'
            f.write(f'    "{ip}" -> "{service}:{port_id}";\n')

    f.write("}\n")

print(f'DOT file generated: {dot_file}')

