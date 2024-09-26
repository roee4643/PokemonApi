#! /bin/bash


###################creating vps with cidr-block 10.0.0.0/16################
create_vpc(){
	local vpc_name="roei vpc"
	local cidr_block=10.0.0.0/16
	local response=$(aws ec2 create-vpc --cidr-block $cidr_block --instance-tenancy default)

	# Extract the VPC ID using jq
	local vpc_id=$(echo "$response" | jq -r '.Vpc.VpcId')

	#assian vpc name to the subnet that created
	aws ec2 create-tags --resources "$vpc_id" --tags Key=Name,Value="$vpc_name"

	echo "$vpc_id"

}


###########################creating public subnet###################
create_public_subnet(){
	local subnet_name=$2
	local cidr_block=$3
	local availability_zone="us-west-2a"
	local vpc_id=$1
	local response=$(aws ec2 create-subnet --vpc-id $vpc_id --cidr-block $cidr_block --availability-zone $availability_zone)

	# Extract the Public subnet ID using jq
	local subnet_id=$(echo "$response" | jq -r '.Subnet.SubnetId')

	#assian subnet name to the subnet that created
	aws ec2 create-tags --resources "$subnet_id" --tags Key=Name,Value="$subnet_name"

	echo "$subnet_id"

}




################creating private subnet##################
create_private_subnet(){
	local subnet_name=$2
	local cidr_block=$3
	local availability_zone="us-west-2a"
	local vpc_id=$1
	local response=$(aws ec2 create-subnet --vpc-id $vpc_id --cidr-block $cidr_block --availability-zone $availability_zone)

# Extract the Private subnet ID using jq
	local subnet_id=$(echo "$response" | jq -r '.Subnet.SubnetId')

	#assian subnet name to the subnet that created
	aws ec2 create-tags --resources "$subnet_id" --tags Key=Name,Value="$subnet_name"

	echo "$subnet_id"

}

#################creating internet gateway#############
create_igw(){

	local igw_name="Public igw"
	local response=$(aws ec2 create-internet-gateway)

	# Extract the internet gateway ID using jq
	local igw_id=$(echo "$response" | jq -r '.InternetGateway.InternetGatewayId')

	#assian igw name to the subnet that created
	aws ec2 create-tags --resources "$igw_id" --tags Key=Name,Value="$igw_name"

	echo "$igw_id"

}

####################attach the internet gateway to the vpc################
attach_igw_to_vpc(){

	local vpc_id=$1
	local igw_id=$2

	aws ec2 attach-internet-gateway --vpc-id $vpc_id --internet-gateway-id $igw_id



}



#######allocate an Elastic IP address for the NAT Gateway############
allocate_elastic_ip(){

	local response=$(aws ec2 allocate-address --domain vpc)

	# Extract the allocation ID using jq
	local Allocation_id=$(echo "$response" | jq -r '.AllocationId')
	local Public_elastic_id=$(echo "$response" | jq -r '.PublicIp')

	echo "$Allocation_id;$Public_elastic_id"

}



###############create the NAT Gateway in the public subnet###########

create_NAT_gtw(){

	local public_subnet_id=$1
	local Allocation_id=$2
	local Nat_gtw_name="Public_subnet_NAT_Gateway"

	local response=$(aws ec2 create-nat-gateway --subnet-id $public_subnet_id --allocation-id $Allocation_id)

	# Extract the allocation ID using jq
	local Nat_gtw_id=$(echo "$response" | jq -r '.NatGateway.NatGatewayId')

	#assian name to the Nat gateway that created
	aws ec2 create-tags --resources "$Nat_gtw_id" --tags Key=Name,Value="$Nat_gtw_name"

	echo $Nat_gtw_id

}




##########creat public route table associated with public subnet 2 

create_public_route_table(){
	
	local vpc_id=$1
	local public_subnet_id2=$2
	
	#create private route table and store it in response variable that will contain the private route id 
	local response=$(aws ec2 create-route-table --vpc-id  $vpc_id \
	    --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=Public Route Table}]')
	    
	#get the public route id from json format    
	local public_route_id=$(echo "$response" | jq -r '.RouteTable.RouteTableId')
	 
	
	 
	  
	#################################    
	
	#Associate Public Subnet 2 with the Public Route Table
	local response2=$(aws ec2 associate-route-table \
	    --route-table-id $public_route_id\
	    --subnet-id $public_subnet_id2)

	
	local associate_state=$(echo "$response2" | jq -r '.AssociationState.State')
		
	echo "$public_route_id;$associate_state"

}

##########creat private route table associated with private subnet 2 
create_private_route_table(){

	local vpc_id=$1
	local private_subnet_id2=$2
	
	#create private route table and store it in response variable that will contain the private route id 
	local response=$(aws ec2 create-route-table --vpc-id  $vpc_id \
	    --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=Private Route Table}]')
	 
	#get the private route id from json format    
	local private_route_id=$(echo "$response" | jq -r '.RouteTable.RouteTableId')
 
	  
	################################# 
	#Associate Private Subnet 2 with the Private Route Table
	
	local response2=$(aws ec2 associate-route-table \
	    --route-table-id $private_route_id\
	    --subnet-id $private_subnet_id2)
	
	local associate_state=$(echo "$response2" | jq -r '.AssociationState.State')
	
	echo "$private_route_id;$associate_state"
}



##########Create a VPC security group
create_vpc_security_group(){

	local vpc_id=$1
	
	
	###create the security group
	local response=$(aws ec2 create-security-group \
    --group-name "Web Security Group" \
    --description "Enable HTTP access" \
    --vpc-id $vpc_id)
    
    	local GroupId=$(echo "$response" | jq -r '.GroupId')
    	
    	###Add Inbound Rules: Add an HTTP Rule to Allow Access
	local response2=$(aws ec2 authorize-security-group-ingress \
    --group-id $GroupId \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0)
 		
    	
	echo $GroupId

}


########launch EC2 instance:
launch_instance(){
	
	#instance configure
	local path_of_user_data=/home/roei/instance_file.sh
	local linux_2_ami_id="ami-0ba84480150a07294"
	local instance_type="t3.micro"
	#local key_name="vockey"
	local instance_name="Web Server 1"
	local public_subnet2=$1
	local GroupId=$2

	#create instance 
	local response=$(aws ec2 run-instances \
	    --image-id $linux_2_ami_id \
	    --instance-type $instance_type \
	    --key-name vockey \
	    --subnet-id $public_subnet2 \
	    --associate-public-ip-address \
	    --security-group-ids $GroupId \
	    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$instance_name}]" \
	    --user-data file://$path_of_user_data)
	    
    	#finding our instance Id
   	local instance_Id=$(echo "$response" | jq -r '.Instances[0].InstanceId')
   	
   	
   	#finding our public ip 
   	local response2=$(aws ec2 describe-instances \
	  --instance-ids $instance_Id \
	  --query "Reservations[*].Instances[*].PublicIpAddress" \
	  --output text)
	  
	local public_instance_ip=$response2
	
	#returning public_instance_ip + instance_Id
	echo "$instance_Id;$public_instance_ip"


}



#####################################Main################################

#######define subnets configure###########
public_subnet_name1="Public_subnet1"
public_cidr_block1=10.0.0.0/24

public_subnet_name2="Public_subnet2"
public_cidr_block2=10.0.2.0/24

private_subnet_name1="Private_subnet1"
private_cidr_block1=10.0.1.0/24

private_subnet_name2="Private_subnet2"
private_cidr_block2=10.0.3.0/24
#################################


echo "processing..."

##########create_vpc#######
vpc_id=$(create_vpc)

######create public and private subnets 1 ######
public_subnet_id1=$(create_public_subnet $vpc_id $public_subnet_name1 $public_cidr_block1)
private_subnet_id1=$(create_private_subnet $vpc_id $private_subnet_name1 $private_cidr_block1)

######create public and private subnets 2 ######
public_subnet_id2=$(create_public_subnet $vpc_id $public_subnet_name2 $public_cidr_block2)
private_subnet_id2=$(create_private_subnet $vpc_id $private_subnet_name2 $private_cidr_block2)

#########create internet gateWay#####
igw_id=$(create_igw)

########attach internet gateway to vpc 
attach_igw_to_vpc $vpc_id $igw_id

#######create elastic ip and get the Public_elastic_id and Allocation_id values
#get Allocation_id + Public_elastic_id
allocate_resultes=$(allocate_elastic_ip)
IFS=';' read -r Allocation_id Public_elastic_id <<< "$allocate_resultes"

#######create NAT gateway
Nat_gtw_id=$(create_NAT_gtw $public_subnet_id1 $Allocation_id)


#create public and private route table and associate with public and private subnet 2

#get public_route_id + public_route_state
create_public_route_table_result=$(create_public_route_table $vpc_id $public_subnet_id2)
IFS=';' read -r public_route_id public_route_state <<< "$create_public_route_table_result"

#get private_route_id + private_route_state
create_private_route_table_result=$(create_private_route_table $vpc_id $private_subnet_id2)
IFS=';' read -r private_route_id private_route_state <<< "$create_private_route_table_result"

######create vpc security group
GroupId=$(create_vpc_security_group $vpc_id)

#####create instance Web server 1 

launch_instance_result=$(launch_instance $public_subnet_id2 $GroupId)
IFS=';' read -r instance_id public_instance_ip <<< "$launch_instance_result"






###resulets print##

echo
echo "The VPC ID is: $vpc_id"
echo
echo "The Public subnet 1 ID is: $public_subnet_id1"
echo
echo "The Private subnet 1 ID is: $private_subnet_id1"
echo
echo "The Public subnet 2 ID is: $public_subnet_id2"
echo
echo "The Private subnet 2 ID is: $private_subnet_id2"
echo
echo "The internet gateway ID is: $igw_id"
echo
echo "The internet gateway $igw_id attached succesfully to vpc: $vpc_id "
echo
echo "The elastic IP for the NAT gateway is $Allocation_id and the Public ip is $Public_elastic_id"
echo
echo "The NAT Gateway Id is: $Nat_gtw_id"
echo
echo "The public route id is: $public_route_id and the state is: $public_route_state to $public_subnet_id2"
echo
echo "The private route id is: $private_route_id and the state is: $private_route_state to $private_subnet_id2"
echo
echo "The security group id of $vpc_id is: $GroupId"
echo
echo "Instance Id is:$instance_id and the public ip of the instance is: $public_instance_ip"

