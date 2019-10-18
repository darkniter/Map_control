import pynetbox
import config
net_box = pynetbox.api(config.NETBOX_URL, config.TOKEN)

def get_ip_addresses():
    ip_list_tmp = net_box.ipam.ip_addresses.all()
    ip_list = []
    for ip in ip_list_tmp:
        ip_list.append(ip.address.split('/')[0])
    return ip_list

if __name__ == "__main__":
    get_ip_addresses()