from lxml import etree
import json
import os
import config

def main():
    old_map = load_old_map()
    into_json(old_map)


def into_json(old_map):
    if (os.path.isfile(config.NEWMAPFILE)):
        os.remove(config.NEWMAPFILE)

    with open(config.NEWMAPFILE, 'w', encoding='utf-8') as new_map_file:
        # json.dump(old_map,new_map_file)
        new_map = etree.tostring(old_map, encoding='unicode')
        new_map_file.write(new_map)
    print ('done')



def load_old_map(old_map_file = config.OLDMAPFILE):
    old_map = None
    with open(old_map_file, 'r', encoding='utf-8') as xml_map_reader:
        xml_map = xml_map_reader.read()
        parser = etree.XMLParser(strip_cdata=False)
        old_map = etree.fromstring(xml_map, parser=parser)
        old_map = load_map_object(old_map)
    return old_map

def load_map_object(old_map):
    vlans = vlan_upload()
    for object_group in old_map:
        if object_group.tag == 'Devices':
            for object_map in object_group:
                address_mask = '.'.join(object_map.attrib['address'].split('.')[0:3:1])
                if address_mask in vlans:
                    object_group.remove(object_map)
    childs = old_map.getchildren()[0].getchildren()
    return old_map


def vlan_upload():
    vlans_list = []
    with open(config.VLANSPATH, 'r', encoding='utf-8-sig') as vlans_file:
       vlans = json.load(vlans_file)
    for vlan_region in vlans:
        if not vlan_region in['Orehovo-Zuevo', 'description']:
            for vlan in vlans[vlan_region]:
                vlans_list.append('.'.join(vlan[4].split('.')[0:3:1]))
    return vlans_list


def filtration(xml_map, option):
    filtred_map = {}
    for name in xml_map:
        if name.tag == 'Devices':
            for dev in name:
                if {**dev.attrib}.get('type-id') == option:
                    filtred_map.update({dev.attrib['id']: {**dev.attrib}})
                    description = dev.getchildren()
                    filtred_map[dev.attrib['id']].update({
                        'description': description[0].text
                        })
    return filtred_map

if __name__ == "__main__":
    main()