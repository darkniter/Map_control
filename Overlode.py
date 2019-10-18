from lxml import etree
import json
import os
import config
from ip_list import get_ip_addresses as get_ip_list

def main(option=None):
    old_map = load_old_map(option)
    into_json(
        old_map,
        config.IPfiltration
        )


def into_json(old_map,fname):
    if (os.path.isfile(fname)):
        os.remove(fname)

    with open(fname, 'w', encoding='utf-8',newline='\n') as new_map_file:
        # json.dump(old_map,new_map_file)
        new_map = etree.tostring(old_map, encoding='unicode',)
        new_map_file.write(new_map)
    print ('done')



def load_old_map(option=None,old_map_file = config.OLDMAPFILE):
    old_map = None
    with open(old_map_file, 'r', encoding='utf-8') as xml_map_reader:
        xml_map = xml_map_reader.read()
        parser = etree.XMLParser(strip_cdata=False)
        old_map = etree.fromstring(xml_map, parser=parser)
        old_map = remove_map_object(old_map,option)
    return old_map

def remove_map_object(old_map,option = None):

    if (option == 'vlan' or option == None):
        vlans = vlan_upload()
        for object_group in old_map:
            if object_group.tag == 'Devices':
                for object_map in object_group:
                    address_mask = '.'.join(object_map.attrib['address'].split('.')[0:3:1])
                    if address_mask in vlans:
                        object_group.remove(object_map)

    if (option == 'ip' or option == None):
        ip_list = get_ip_list()
        for object_group in old_map:
            if object_group.tag == 'Devices':
                for object_map in object_group:
                    address = object_map.attrib['address']
                    if address in ip_list:
                        object_group.remove(object_map)

    # childs = old_map.getchildren()[0].getchildren()
    return old_map


def broken_flag(option = None):

    if option == 'cleared':

        with open(config.IPfiltration, 'r', encoding='utf-8') as xml_map_reader:
            xml_map = xml_map_reader.read()
            parser = etree.XMLParser(strip_cdata=False,)
            old_map = etree.fromstring(xml_map, parser=parser,)

        with open(config.OZ,'r', encoding='utf-8-sig') as result_broken:
            broken_list = json.load(result_broken)

        for object_group in old_map:
            if object_group.tag == 'Devices':
                for object_map in object_group:
                    address = object_map.attrib['address']
                    if address in broken_list:
                        object_group.remove(object_map)
        into_json(old_map,config.RESULT_CLEARED)

    elif option == 'named':
        with open(config.RESULT_CLEARED, 'r', encoding='utf-8') as xml_map_reader:
            xml_map = xml_map_reader.read()
            parser = etree.XMLParser(strip_cdata=False,)
            old_map = etree.fromstring(xml_map, parser=parser,)

        with open(config.BROKEN,'r', encoding='utf-8-sig') as result_broken:
            broken_list = json.load(result_broken)

        for object_group in old_map:
            if object_group.tag == 'Devices':
                for object_map in object_group:
                    address = object_map.attrib['address']
                    if address in broken_list:
                        object_map.attrib['name'] += '[!broken!]'
        into_json(old_map,config.BROKEN_RESULT_FLAG)

    elif option == 'cleared_broken':
        with open(config.RESULT_CLEARED, 'r', encoding='utf-8') as xml_map_reader:
            xml_map = xml_map_reader.read()
            parser = etree.XMLParser(strip_cdata=False,)
            old_map = etree.fromstring(xml_map, parser=parser,)

        with open(config.BROKEN,'r', encoding='utf-8-sig') as result_broken:
            broken_list = json.load(result_broken)

        for object_group in old_map:
            if object_group.tag == 'Devices':
                for object_map in object_group:
                    address = object_map.attrib['address']
                    if address in broken_list:
                        object_group.remove(object_map)
        into_json(old_map,config.BROKEN_RESULT_FLAG_CLEARED)


def vlan_upload():
    vlans_list = []
    with open(config.VLANSPATH, 'r', encoding='utf-8-sig') as vlans_file:
       vlans = json.load(vlans_file)
    for vlan_region in vlans:
        if not vlan_region in['Orehovo-Zuevo', 'description']:
            for vlan in vlans[vlan_region]:
                vlans_list.append('.'.join(vlan[4].split('.')[0:3:1]))
    return vlans_list


if __name__ == "__main__":
    main('ip')
    broken_flag_options = [
        'cleared',
        'named',
        'cleared_broken'
        ]
    for option in broken_flag_options:
        broken_flag(option)