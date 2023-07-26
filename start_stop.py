import sys
import boto3
import time
from cred import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME

INSTANCE_ID = 'Instance_ID'

ec2_client = boto3.client('ec2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME)

def get_instance_name(instance_id):
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    tags = response['Reservations'][0]['Instances'][0].get('Tags', [])
    for tag in tags:
        if tag['Key'] == 'Name':
            return tag['Value']
    return instance_id

def start_instance(instance_id):
    try:
        instance_name = get_instance_name(instance_id)
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        if state == 'running':
            print(f'{instance_name} instance is already running.')
        else:
            confirm = input(f'Do you really want to start instance {instance_name}? (yes/no): ')
            if confirm.lower() == 'yes':
                ec2_client.start_instances(InstanceIds=[instance_id])
                print(f'Starting instance {instance_name}...')
                waiter = ec2_client.get_waiter('instance_running')
                waiter.wait(InstanceIds=[instance_id])
                print(f'Instance {instance_name} has started.')

                # Wait for the public IP address to be available
                while True:
                    response = ec2_client.describe_instances(InstanceIds=[instance_id])
                    instance_info = response['Reservations'][0]['Instances'][0]
                    public_ip = instance_info.get('PublicIpAddress')
                    if public_ip:
                        print(f'Public IP address: {public_ip}')
                        break
                    time.sleep(5)  # Wait for 5 seconds before checking again
                return True
            else:
                print('Start instance operation cancelled.')
                return False
    except Exception as e:
        print(f'Error starting instance: {e}')
        return False

def stop_instance(instance_id):
    try:
        instance_name = get_instance_name(instance_id)
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        if state == 'stopped':
            print(f'{instance_name} instance is already stopped.')
        else:
            confirm = input(f'Do you really want to stop instance {instance_name}? (yes/no): ')
            if confirm.lower() == 'yes':
                ec2_client.stop_instances(InstanceIds=[instance_id])
                print(f'Stopping instance {instance_name}...')
                waiter = ec2_client.get_waiter('instance_stopped')
                waiter.wait(InstanceIds=[instance_id])
                print(f'Instance {instance_name} has stopped.')
                return True
            else:
                print('Stop instance operation cancelled.')
                return False
    except Exception as e:
        print(f'Error stopping instance: {e}')
        return False

def instance_status(instance_id):
    try:
        instance_name = get_instance_name(instance_id)
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        print(f'{instance_name} instance is currently {state}.')
    except Exception as e:
        print(f'Error getting instance status: {e}')

if __name__ == '__main__':
    print('Select an action:')
    print('1. Start Instance')
    print('2. Stop Instance')
    print('3. Instance Status')
    print('4. Display Public IP Address')

    choice = input('Enter your choice (1, 2, 3, or 4): ')

    if choice == '1':
        start_instance(INSTANCE_ID)
    elif choice == '2':
        stop_instance(INSTANCE_ID)
    elif choice == '3':
        instance_status(INSTANCE_ID)
    elif choice == '4':
        response = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])
        instance_info = response['Reservations'][0]['Instances'][0]
        public_ip = instance_info.get('PublicIpAddress')
        instance_name = get_instance_name(INSTANCE_ID)
        if public_ip:
            print(f'Public IP address: {public_ip} (Instance Name: {instance_name})')
        else:
            print(f'{instance_name} instance is in stopped state, Public IP address not available.')
    else:
        print('Invalid choice. Please enter a valid option (1, 2, 3, or 4).')
