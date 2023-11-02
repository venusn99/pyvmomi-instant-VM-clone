'''
# Original Script by [Author's Name] (GitHub: [GitHub Username])
# Original Script URL: https://github.com/Jangari-nTK/pyvmomi-instant-clone-sample/blob/master/instant_clone.py
# Modified by : VENU S N
# Date: 02-nov-2023
# Modified Script URL: 

'''

from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
from pyVim.task import WaitForTask
import ssl, atexit, getpass

def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)

    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break
    
    return obj
def instant_clone_vm(content, parent_vm, vm_name, datacenter_name, vm_folder, resource_pool ):

    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)
    if vm_folder:
        dst_folder = get_obj(content, [vim.Folder], vm_folder)
    else:
        dst_folder = datacenter.vmFolder

    resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)

    vm_relocate_spec = vim.vm.RelocateSpec()
    vm_relocate_spec.folder = dst_folder
    vm_relocate_spec.pool = resource_pool

    instant_clone_spec = vim.vm.InstantCloneSpec()
    instant_clone_spec.name = vm_name
    instant_clone_spec.location = vm_relocate_spec

    WaitForTask(parent_vm.InstantClone_Task(spec=instant_clone_spec))

def main():
    vcenter = input("Enter the vCenter IP/Hostname\n")
    vcenter_username = input("Enter the vCenter's username\n")
    vcenter_passwd = getpass.getpass(prompt='Enter password:')
    context = None
    if hasattr(ssl, "_create_unverified_context"):
        context = ssl._create_unverified_context()

    si = SmartConnect(
                    host= vcenter,
                    user=vcenter_username,
                    pwd=vcenter_passwd,
                    port='443',
                    sslContext=context)

    atexit.register(Disconnect, si)
    content = si.content
    parent_vm_name = input("Enter the name of parent VM \n")
    parent_vm = get_obj(content, [vim.VirtualMachine], parent_vm_name)  

    if parent_vm:
        number_of_clones = int(input("Enter the number of clones\n"))
        prefix_for_clone = input("Enter the prefix for the cloned VMs\n")
        new_datacenter = input("(optional) Enter the Datacenter name for new destination VM\n")
        new_vm_folder = input("(optional) Enter the VM folder name for new destination VM\n")
        new_cluster = input("(optional) Enter the cluster name for new destination VM\n")
        for num in range(1, number_of_clones + 1):
            new_vm = f"{prefix_for_clone}-{num}"
            instant_clone_vm(content, parent_vm, new_vm,
                new_datacenter, new_vm_folder, new_cluster)
    else:
        print("parent_vm not found")
        quit()
if __name__ == '__main__':
    main()
