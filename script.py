
import boto3
#Script to check if an S3 bucket in your aws account is having write access to public or any authenticated user
def check_access():
    # Create an S3 client
    s3 = boto3.client('s3')

    # List all buckets
    response = s3.list_buckets()

    # Initialize a list to store results
    results = []

    # Check each bucket for public or authenticated write access
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']

        # Get bucket ACL
        acl_response = s3.get_bucket_acl(Bucket=bucket_name)

        # Check for public write access
        public_write_access = False
        authenticated_write_access = False

        for grant in acl_response['Grants']:
            grantee = grant.get('Grantee', {})
            permission = grant.get('Permission')

            # Check for 'AllUsers' and 'AuthenticatedUsers' groups with 'WRITE' permission
            if grantee.get('Type') == 'Group' and grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers' and permission == 'WRITE':
                public_write_access = True
            elif grantee.get('Type') == 'Group' and grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers' and permission == 'WRITE':
                authenticated_write_access = True

        # Append the result to the list
        results.append({
            'BucketName': bucket_name,
            'PublicWriteAccess': 'Yes' if public_write_access else 'No',
            'AuthenticatedWriteAccess': 'Yes' if authenticated_write_access else 'No'
        })

    return results

if __name__ == "__main__":
    bucket_results = check_access()

    # Print the results in a tabular format
    print("Bucket Name\tPublic Write Access\tAuthenticated Write Access")
    for result in bucket_results:
        print(f"{result['BucketName']}\t{result['PublicWriteAccess']}\t{result['AuthenticatedWriteAccess']}")
