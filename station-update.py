'''
This script securely copies the Pi-hat network configuration file from the
Dosenet servers to a Pi-hat at a school of interest and updates the network ID
on the network configuration file for the Pi-hat, as well as handles static
IPs, netmasks, gateways, and DNS-server names.
'''

# Import the relevant modules and functions from the appropriate libraries for
# convenience.
import fileinput
import os
import sys

'''
Part 1: Securely copying the network configuration file from the Dosenet
servers to the Pi-hat.
'''

# Ask the user for the csv file name and output the raw input string as a
# variable.
name = raw_input('What is the csv file name?: ')

# Define the paths to the source and target .csv files as arguments for the scp
# linux command to be executed through the os.sytem function.
sourcePath = 'dosenet@dosenet.dhcp.lbl.gov:~/config-files/' + name
targetPath = '/home/pi/config/config.csv'

# Execute the scp linux command line to securely copy the file over the
# Internet using root user access.
os.system('sudo scp {} {}'.format(sourcePath, targetPath))

'''
Part 2: Updating the dosimeter ID on the network configuration file on the
Pi-hat once it has been copied securely over the Internet.
'''

# Backup the interfaces file through the cp linux command to make a backup copy
# of the interfaces file before any editing is done.
os.system('sudo cp /etc/network/interfaces /etc/network/interfaces_backup')

# Alert the user that a backup file has been made.
print('A backup of the network interfaces file has been made. If you make ' +
      'an error during the rest of the setup, a prompt at the end will ' +
      'ask if you would like to restore the backup.')

# Ask for the station ID and output the raw input string as a variable.
id = raw_input('What is the station ID?: ')

'''
Define a function to update the interfaces file by replacing the line
containing an indicated phrase with a new line.
'''


def interfaces_update(rep_phrase, new_line):
    # Store the normal standard input and output. This allows us to restore
    # them later to access the standard input and output for other uses
    # outside of this function, such as raw_input and print statements.
    temp_in = sys.stdin
    temp_out = sys.stdout

    # Open the interfaces file for reading and open up a temporary file for
    # writing using the standard input and output functions.
    sys.stdin = open('/etc/network/interfaces', 'r')
    sys.stdout = open('~interfaces_temp', 'w')

    """
    Loop through each line of the interfaces file to find the phrase of
    interest and replace it with the new line.
    """

    for line in fileinput.input('/etc/network/interfaces'):

        # Search and find the phrase of interest to indicate the place in the
        # code to replace the original line with the new line.
        if rep_phrase in line:

            # Create a handle for a new line with the updated phrase to input
            # into the interfaces file.
            line = new_line

        # Write the new line with the updated phrase in the temporary
        # interfaces file. Also copy all other lines.
        sys.stdout.write(line)

    # Move the updated interfaces file to replace the old interfaces file
    # using root access.
    os.system('sudo mv ~interfaces_temp /etc/network/interfaces')

    # Close the interfaces files for reading and writing
    sys.stdout.close()

    # Return the original standard input and output to normal.
    sys.stdin = temp_in
    sys.stdout = temp_out

# Update the station ID using the update function.
interfaces_update('wireless-essid RPiAdHocNetwork', '  wireless-essid ' +
                  'RPiAdHocNetwork{}'.format(id) + '\n')

# Ask the user if they would like to use a static IP.
setup_static_ip = raw_input('Do you want to set a static IP (y/n)?: ')

"""
If the response is a yes, update the interfaces file to include the static IP
and the relevant functionality.
"""
if setup_static_ip is 'y':

    # Ask for the static IP.
    ip_static = raw_input('What is your static IP?: ')

    # Update the interfaces file with the static IP by commenting out the
    # dynamic IP call and uncommenting out the static IP calls.
    interfaces_update('iface eth0 inet dhcp', '# replace for dynamic IP ' +
                      'configuration' + '\n' + '# iface eth0 inet dhcp' +
                      '\n')
    interfaces_update('# auto eth0', 'auto eth0' + '\n')
    interfaces_update('# iface eth0 inet static', 'iface eth0 inet static' +
                      '\n')
    interfaces_update('#   address', '  address {}'.format(ip_static) + '\n')

    # Ask the user if they have a netmask.
    setup_netmask = raw_input('Do you have a netmask (y/n)?: ')

    """
    If the response is a yes, update the interfaces file to include the netmask
    identifier and the relevant functionality.
    """
    if setup_netmask is 'y':

        # Ask for the netmask identifier.
        netmask_id = raw_input('What is your netmask identifier?: ')

        # Update the interfaces file with the netmask identifier by
        # uncommenting out the netmask call.
        interfaces_update('#   netmask', '  netmask {}'.format(netmask_id) +
                          '\n')

    # Ask the user if they have a gateway.
    setup_gateway = raw_input('Do you have a gateway (y/n)?: ')

    '''
    If the response is a yes, update the interfaces file to include the gateway
    identifier and the relevant functionality.
    '''
    if setup_gateway is 'y':

        # Ask for the gateway identifier.
        gateway_id = raw_input('What is your gateway identifier?: ')

        # Update the interfaces file with the gateway identifier by
        # uncommenting out the gateway call.
        interfaces_update('#   gateway', '  gateway {}'.format(gateway_id) +
                          '\n')

    # Ask the user if they have DNS servers connected.
    setup_dns_server = raw_input('Do you have DNS servers connected (y/n)?: ')

    '''
    If the response is a yes, update the interfaces file to include the DNS
    server names and the relevant functionality.
    '''
    if setup_dns_server is 'y':

        # Ask for the DNS server names.
        dns_server_1 = raw_input('What is the IP of the first DNS server?: ')
        dns_server_2 = raw_input('What is the IP of the second DNS server?: ')

        # Update the interfaces file with the DNS server names by uncommenting
        # out the DNS server names call.
        interfaces_update("#   dns-nameservers", "  dns-nameservers " +
                          '{} {}'.format(dns_server_1, dns_server_2) + '\n')

# Ask the user if they would like to restore the backup to the network
# interfaces file.
restore_backup = raw_input('Would you like to restore the backup of the ' +
                           'network interfaces update (y/n)?: ')

# If the response is a yes, copy the backup over the original file that has
# been modified.
if restore_backup is 'y':

    # Restore the backup interfaces file using the cp linux command with root
    # access.
    os.system('sudo cp /etc/network/interfaces_backup /etc/network/interfaces')

    # Alert the user that the backup interfaces file has been restored and to
    # rerun the script if they want to re-setup the network configuration.
    print('The network interfaces file has been restored from the backup. ' +
          'Run this Python script again to setup the network ' +
          'configuration again.')
