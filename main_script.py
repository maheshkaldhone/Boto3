import sys
import boto3
from cred import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME


# EC2 instance ID of the instance you want to start and stop
INSTANCE_ID = 'i-0553d950d680175d2'

# Create a Boto3 EC2 client
ec2_client = boto3.client('ec2', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME)

def start_instance():
    try:
        response = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        if state == 'running':
            print(f'Instance {INSTANCE_ID} is already running.')
        else:
            ec2_client.start_instances(InstanceIds=[INSTANCE_ID])
            print(f'Starting instance {INSTANCE_ID}...')
            waiter = ec2_client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[INSTANCE_ID])
            print(f'Instance {INSTANCE_ID} has started.')
    except Exception as e:
        print(f'Error starting instance: {e}')

def stop_instance():
    try:
        response = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        if state == 'stopped':
            print(f'Instance {INSTANCE_ID} is already stopped.')
        else:
            ec2_client.stop_instances(InstanceIds=[INSTANCE_ID])
            print(f'Stopping instance {INSTANCE_ID}...')
            waiter = ec2_client.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[INSTANCE_ID])
            print(f'Instance {INSTANCE_ID} has stopped.')
    except Exception as e:
        print(f'Error stopping instance: {e}')

def instance_status():
    try:
        response = ec2_client.describe_instances(InstanceIds=[INSTANCE_ID])
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        print(f'Instance {INSTANCE_ID} is currently {state}.')
    except Exception as e:
        print(f'Error getting instance status: {e}')

if __name__ == '__main__':
    print('Select an action:')
    print('1. Start Instance')
    print('2. Stop Instance')
    print('3. Instance Status')

    choice = input('Enter your choice (1, 2, or 3): ')

    if choice == '1':
        start_instance()
    elif choice == '2':
        stop_instance()
    elif choice == '3':
        instance_status()
    else:
        print('Invalid choice. Please enter 1, 2, or 3 for the corresponding action.')

